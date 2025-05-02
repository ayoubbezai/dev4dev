<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ChargilyPayment extends Model
{
    // Add constants for cleaner status management
    const STATUS_PENDING = 'pending';
    const STATUS_PAID = 'paid';
    const STATUS_FAILED = 'failed';

    protected $fillable = [
        'user_id',
        'status',
        'currency',
        'amount',
    ];
            public function user()
{
    return $this->belongsTo(User::class);
}
}


