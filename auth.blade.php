<form method="POST" action="/public/login">
    @csrf
    <div>
        <label>Логин:</label>
        <input type="text" name="login">
    </div>
    <div>
        <label>Пароль:</label>
        <input type="password" name="password">
    </div>
    <button type="submit">Войти</button>
</form>

@if(Auth::check())
    <div style="color:green;">
        ✅ Авторизован: {{ Auth::user()->name }}
        <form method="POST" action="/logout">
            @csrf
            <button type="submit">Выйти</button>
        </form>
    </div>
@else
    <div style="color:red;">
        ❌ Не авторизован
    </div>
@endif
