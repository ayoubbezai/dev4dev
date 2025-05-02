<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\Http\Response;

class AuthController extends Controller
{
    public function register(Request $request)
    {
        $data = $request->validate([
            "name" => "required|string",
            "email" => "required|string|email|unique:users",
            "password" => "required|min:6",
            "role" => "nullable|string|in:admin,user,moderator" 
        ]);

        // Create the user
        try {
            $user = User::create([
                "name" => $data["name"],
                "email" => $data["email"],
                "password" => $data["password"],
                "role" => $data["role"] ?? 'user' 
            ]);

            // Generate a token for the user
            $token = $user->createToken("auth_token")->plainTextToken;

            // Return success response
            return response()->json([
                "user" => $user,
                "token" => $token,
                "user_role" => $user->role
            ], 201);

        } catch (\Exception $e) {
            Log::error('Failed to register user: ' . $e->getMessage());
            return response()->json([
                "success" => false,
                "message" => "Failed to register user",
                "error" => $e->getMessage(),
            ], 500);
        }
    }

    public function login(Request $request)
    {
        $data = $request->validate([
            "email" => "required|email|exists:users,email",
            "password" => "required|min:6",
        ]);

        $user = User::where("email", $data["email"])->first();

        if (!$user) {
            return response()->json([
                "success" => false,
                "message" => "User not found."
            ], 404);
        }

        if (!Hash::check($data["password"], $user->password)) {
            return response()->json([
                "success" => false,
                "message" => "The provided credentials are incorrect."
            ], 401);
        }

        $token = $user->createToken("auth_token")->plainTextToken;

        return response()->json([
            "success" => true,
            "message" => "User logged in successfully.",
            "user" => [
                "id" => $user->id,
                "name" => $user->name,
                "email" => $user->email,
                "role" => $user->role,
            ],
            "token" => $token
        ], 200);
    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();
        return response()->json([
            "success" => true,
            "message" => "Logged out successfully"
        ], 200);
    }

    public function currentUser(Request $request)
    {
        try {
            $currentUser = $request->user();

            
            if (!$currentUser) {
                return response()->json([
                    'success' => false,
                    'message' => 'User not authenticated',
                ], Response::HTTP_UNAUTHORIZED);
            }

            return response()->json([
                "success" => true,
                "message" => "User retrieved successfully.",
                "user" => [
                    "id" => $currentUser->id,
                    "name" => $currentUser->name,
                    "email" => $currentUser->email,
                    "role" => $currentUser->role,
                    "hasPaied"=> $currentUser->payment,
                ],
            ], 200);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Failed to get the current user',
                'error' => $e->getMessage(),
            ], Response::HTTP_INTERNAL_SERVER_ERROR);
        }
    }
}