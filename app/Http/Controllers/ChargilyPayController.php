<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ChargilyPayment;
use App\Models\User;
use Chargily\ChargilyPay\ChargilyPay;
use Chargily\ChargilyPay\Auth\Credentials;
use Illuminate\Support\Facades\Auth;
use Carbon\Carbon;

class ChargilyPayController extends Controller
{
    public function redirect()
    {
                    $userId = Auth::id();

        $currency = 'dzd';
        $amount = '25000'; 

        $payment = ChargilyPayment::create([
            'user_id'  => $userId,
            'status'   => 'pending',
            'currency' => $currency,
            'amount'   => $amount,
        ]);

   
        
        $checkout = $this->chargilyPayInstance()->checkouts()->create([
            'metadata' => [
                'payment_id' => $payment->id,
            ],
            'locale' => 'ar',
            'amount' => $payment->amount,
            'currency' => $payment->currency,
            'description' => "Payment ID={$payment->id}",
            'success_url' => route('chargilypay.back'),
            'failure_url' => route('chargilypay.back'),
            
        ]);

             $user = User::FindOrFail($userId);

$user->access_expires_at = Carbon::now()->addDays(30);


        $user->save();
        return response()->json(["url"=>$checkout->getUrl()]);

    }

    public function back(Request $request)
    {
        $checkout_id = $request->input('checkout_id');
        $checkout = $this->chargilyPayInstance()->checkouts()->get($checkout_id);

        if ($checkout) {
            $metadata = $checkout->getMetadata();
            $payment = ChargilyPayment::find($metadata['payment_id']);

            // Simulate webhook result locally
            if ($checkout->getStatus() === 'paid') {
                $payment->status = 'paid';
            } else {
                $payment->status = 'failed';
            }
            $payment->save();

            return response()->json([
                'message' => 'Payment completed locally.',
                'status' => $payment->status,
                'amount' => $payment->amount,
            ]);
        }

        return response()->json(['error' => 'Checkout not found'], 404);
    }

    public function webhook(Request $request)
    {
        $webhook = $this->chargilyPayInstance()->webhook()->get();

        if ($webhook) {
            $checkout = $webhook->getData();
            if ($checkout && $checkout instanceof \Chargily\ChargilyPay\Elements\CheckoutElement) {
                $metadata = $checkout->getMetadata();
                $payment = ChargilyPayment::find($metadata['payment_id']);

                if ($payment) {
                    if ($checkout->getStatus() === 'paid') {
                        $payment->status = 'paid';
                    } else {
                        $payment->status = 'failed';
                    }
                    $payment->save();

                    return response()->json(['status' => true, 'message' => 'Updated from webhook']);
                }
            }
        }

        return response()->json(['status' => false, 'message' => 'Invalid Webhook'], 403);
    }

    protected function chargilyPayInstance()
    {
        return new ChargilyPay(new Credentials([
            'mode' => 'test',
            'public' => env('CHARGILY_PAY_PUBLIC', 'test_pk_********************'),
            'secret' => env('CHARGILY_PAY_SECRET', 'test_sk_********************'),
        ]));
    }
}
