<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class CheckUserAccess
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
public function handle($request, Closure $next)
{
    $user = $request->user();

    if (!$user || !$user->is_active || now()->greaterThan($user->access_expires_at)) {
        return response()->json(['error' => 'Your access has expired or is not allowed'], 403);
    }

    return $next($request);
}
}
