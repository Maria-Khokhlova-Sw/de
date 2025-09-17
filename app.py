from flask import Flask, request, jsonify, render_template
from db import get_user, increment_attempts, reset_attempts_and_block, reset_attempts

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    login = (data.get("login") or "").strip()
    password = (data.get("password") or "").strip()
    captcha_order = data.get("captcha_order", [])

    user = get_user(login)
    if not user:
        return jsonify({"status": "fail", "message": "Пользователь не найден"})

    user_id, db_login, db_password, isblocked, numberAttempts = user

    if isblocked:
        return jsonify({"status": "fail", "message": "Пользователь заблокирован, обратитесь к администрации"})

    # проверить капчу (ожидаем [1,2,3,4])
    try:
        captcha_order_ints = [int(x) for x in captcha_order]
    except Exception:
        captcha_order_ints = []

    # если капча неверна — засчитать попытку
    if captcha_order_ints != [1,2,3,4]:
        new_attempts = increment_attempts(login)
        if new_attempts is None:
            return jsonify({"status": "fail", "message": "Ошибка при обновлении попыток"}), 500
        if new_attempts >= 3:
            reset_attempts_and_block(login)
            return jsonify({"status": "fail", "message": "Пользователь заблокирован после 3 неверных попыток"})
        return jsonify({"status": "fail", "message": f"Неверная капча. Попытка {new_attempts}/3"})

    # капча ок — проверить пароль
    if password == db_password:
        reset_attempts(login)
        return jsonify({"status": "success", "message": "Вход выполнен"})
    else:
        new_attempts = increment_attempts(login)
        if new_attempts is None:
            return jsonify({"status": "fail", "message": "Ошибка при обновлении попыток"}), 500
        if new_attempts >= 3:
            reset_attempts_and_block(login)
            return jsonify({"status": "fail", "message": "Пользователь заблокирован после 3 неверных попыток"})
        return jsonify({"status": "fail", "message": f"Неверный пароль. Попытка {new_attempts}/3"})

if __name__ == "__main__":
    app.run(debug=True)
