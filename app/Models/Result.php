<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Result extends Model
{
    //
protected $fillable = ['user_id', 'company', 'position', 'url'];


    public function user(){
            return $this->belongsTo(User::class);

    }

}
