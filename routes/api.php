<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\ChargilyPayController;
use App\Http\Controllers\UserController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

// Public routes
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// Protected routes (require authentication)
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/user', [AuthController::class, 'currentUser']);
 Route::post('chargilypay/redirect', [ChargilyPayController::class, "redirect"])->name("chargilypay.redirect");
Route::get('chargilypay/back', [ChargilyPayController::class, "back"])->name("chargilypay.back");
Route::post('chargilypay/webhook', [ChargilyPayController::class, "webhook"])->name("chargilypay.webhook_endpoint");
    

});

// Optional: Admin-only routes
Route::middleware(['auth:sanctum', 'role:admin'])->group(function () {

});

Route::middleware('auth:sanctum')->group(function () {
    Route::post('chargilypay/redirect', [ChargilyPayController::class, 'redirect'])->name('chargilypay.redirect');
    Route::get('chargilypay/back', [ChargilyPayController::class, 'back'])->name('chargilypay.back');
    Route::resource('/users', UserController::class);

});
Route::post('chargilypay/webhook', [ChargilyPayController::class, 'webhook'])->name('chargilypay.webhook');

Route::post('chargily/webhook/test', [ChargilyPayController::class, 'testWebhook']);

Route::middleware(['auth:sanctum', 'check.access'])->get('/dashboard', function () {
    return "Welcome to your paid dashboard!";
});

Route::options('chargilypay/webhook', [ChargilyPayController::class, 'handleOptions']);

Route::post('chargilypay/simulate-webhook', [ChargilyPayController::class, 'simulateWebhook']);