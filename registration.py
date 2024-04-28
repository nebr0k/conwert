from flask import Flask, request

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Виведення даних в консоль для перевірки
    print("Прийнято дані:")
    print("Нікнейм:", username)
    print("Email:", email)
    print("Пароль:", password)

    # Повернення відповіді на успішний запит
    return f"Реєстрація успішна! Нікнейм: {username}, Email: {email}, Пароль: {password}"

if __name__ == '__main__':
    app.run(debug=True)
