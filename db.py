import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="root",
        port=5432
    )

def get_user(login):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, login, password, isblocked, numberAttempts
        FROM users WHERE login=%s;
    """, (login,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def increment_attempts(login):
    conn = get_connection()
    cur = conn.cursor()
    # увеличиваем и сразу получаем новое значение
    cur.execute("UPDATE users SET numberAttempts = numberAttempts + 1 WHERE login=%s RETURNING numberAttempts;", (login,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row[0] if row else None

def reset_attempts_and_block(login):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET numberAttempts=0, isblocked=TRUE WHERE login=%s;", (login,))
    conn.commit()
    cur.close()
    conn.close()

def reset_attempts(login):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET numberAttempts=0 WHERE login=%s;", (login,))
    conn.commit()
    cur.close()
    conn.close()
