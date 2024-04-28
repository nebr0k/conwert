from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Підключення до бази даних SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Функція для перевірки електронної адреси та пароля користувача
def authenticate(email, password):
    cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
    user = cursor.fetchone()
    return user is not None

# Головна сторінка для входу
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if authenticate(email, password):
            return f"Успішний вхід для {email}!"
        else:
            return "Невірна електронна адреса або пароль. Спробуйте ще раз."
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
