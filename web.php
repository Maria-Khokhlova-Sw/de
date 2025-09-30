<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;

Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
Route::post('/login', [AuthController::class, 'login']);

Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

Route::get('/dashboard', function () {
    if (!Auth::check()) {
        return redirect('/login');
    }
    $user = auth()->user(); 
    return 'Добро пожаловать, ' . $user->name . '! <br><a href="/login">Вернуться к форме логина</a>';
})->middleware('auth');
