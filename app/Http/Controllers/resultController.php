<?php

namespace App\Http\Controllers;

use App\Models\ChargilyPayment;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use App\Models\Result;
use App\Models\User;
use Illuminate\Support\Facades\Auth;

class ResultController extends Controller
{
    public function processPdf(Request $request)
    {
        // 1. Validate the PDF file
        $request->validate([
            'file' => 'required|file|mimes:pdf|max:5120', // 5MB max
        ]);

        try {
            // 2. Get the PDF file
            $pdfFile = $request->file('file');
            
            // 3. Make the API request
            $response = Http::asMultipart()
                ->attach(
                    'file', 
                    file_get_contents($pdfFile->getRealPath()),
                    $pdfFile->getClientOriginalName(),
                    ['Content-Type' => 'application/pdf']
                )
                ->timeout(500)
                ->post('https://oppmatchcode-2.onrender.com/process-pdf');

            // 4. Handle API response
            if ($response->status() === 400) {
                throw new \Exception("API rejected the file: " . $response->body());
            }

            if (!$response->successful()) {
                throw new \Exception("API request failed with status: " . $response->status());
            }

            $responseData = $response->json();
            
            // 5. Store results in database (only if API was successful)
            if ($responseData['success'] && isset($responseData['internships'])) {
                $user = Auth::user(); // Get authenticated user
                
                foreach ($responseData['internships'] as $internship) {
                    Result::create([
                        'user_id' => $user->id,
                        'company' => $internship['company'],
                        'position' => $internship['position'],
                        'url' => $internship['url']
                    ]);
                }
            }

            // 6. Return successful response
            return response()->json([
                'success' => true,
                'data' => $responseData
            ]);

        } catch (\Exception $e) {
            Log::error('PDF Processing Error: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Failed to process PDF',
                'error' => $e->getMessage()
            ], 500);
        }
    }

public function getHistory()
{
    $user = Auth::user();
    
    $history = Result::where('user_id', $user->id)
        ->orderBy('created_at', 'desc')
        ->paginate(10);

    return response()->json([
        'success' => true,
        'data' => $history,
        'message' => 'History retrieved successfully'
    ]);
}

// In your Laravel Controller (e.g., StatsController.php)

public function getStat()
{
    // Total number of users
    $numberOfUsers = User::count();
    
    // Total payment amount (sum of all successful payments)
    $paymentTotal = ChargilyPayment::where('status', 'paid')->sum('amount');
    
    // Total number of tests (assuming each test has 3 results)
    $numberOfTests = ceil(Result::count() / 3);
    
    // Total number of result links
    $numberOfLinks = Result::count();
    
    // Monthly payment data for the chart
    $monthlyPayments = ChargilyPayment::where('status', 'paid')
        ->selectRaw('SUM(amount) as total, MONTH(created_at) as month')
        ->groupBy('month')
        ->orderBy('month')
        ->get();
    
    // Format monthly data for chart
    $paymentChartData = [];
    $months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    foreach ($months as $index => $month) {
        $payment = $monthlyPayments->firstWhere('month', $index + 1);
        $paymentChartData[$month] = $payment ? $payment->total : 0;
    }
    
    return response()->json([
        'success' => true,
        'data' => [
            'totalUsers' => $numberOfUsers,
            'totalPayments' => $paymentTotal,
            'totalTests' => $numberOfTests,
            'totalLinks' => $numberOfLinks,
            'paymentChartData' => $paymentChartData
        ]
    ]);
}
}