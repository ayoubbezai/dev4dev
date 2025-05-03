<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Cache;

class SimpleRateLimiter
{
    public function handle($request, Closure $next)
    {
        $key = 'simple_rate_limit'; // Use IP-specific: 'rate_limit_' . $request->ip()
        $maxRequests = 10;
        $decaySeconds = 60;

        $requests = Cache::get($key, 0);

        if ($requests >= $maxRequests) {
            return response('Rate limit exceeded. Try again later.', 429);
        }

        Cache::put($key, $requests + 1, $decaySeconds);

        return $next($request);
    }
}
