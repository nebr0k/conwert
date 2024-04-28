import sqlite3
from werkzeug.security import generate_password_hash

# Функція для створення підключення до бази даних SQLite
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('converter.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Функція для створення таблиці користувачів у базі даних
def create_users_table(conn):
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_users_table_query)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Функція для додавання нового користувача до бази даних
def add_user(conn, username, email, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    insert_user_query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
    try:
        conn.execute(insert_user_query, (username, email, hashed_password))
        conn.commit()
        print("Користувач успішно доданий до бази даних.")
    except sqlite3.Error as e:
        print("Помилка при додаванні користувача до бази даних:", e)

# Підключення до бази даних
conn = create_connection()

# Створення таблиці користувачів
if conn is not None:
    create_users_table(conn)
else:
    print("Помилка! Неможливо підключитися до бази даних.")

# Додавання нового користувача
add_user(conn, "example_user", "example@example.com", "example_password")

# Закриття з'єднання з базою даних
conn.close()
import secrets

secret_key = secrets.token_hex(16)
print(secret_key)
