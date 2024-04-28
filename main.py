from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, session
from PIL import Image
import os
import zipfile
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = '002e6377f3d01535bc5991194a0f0fba'



# Function to initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()


# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


from flask import Flask, request, jsonify
import sqlite3

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_username = c.fetchone()

    if existing_username:
        conn.close()
        return jsonify({'message': 'Username already exists'})

    c.execute("SELECT * FROM users WHERE email=?", (email,))
    existing_email = c.fetchone()

    if existing_email:
        conn.close()
        return jsonify({'message': 'Email already exists'})

    if len(password) < 8:
        conn.close()
        return jsonify({'message': 'Password must be at least 8 characters long'})

    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)

    if not (has_uppercase and has_lowercase and has_digit):
        conn.close()
        return jsonify({'message': 'Password must contain at least one uppercase letter, one lowercase letter, and one digit'})

    hashed_password = hash_password(password)

    # Insert new user into the database
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()

    # Automatically login the user after successful registration
    session['username'] = username

    conn.close()

    # Return a JSON response indicating successful registration
    return jsonify({'message': 'Registration successful', 'username': username})
    flash('Registration successful!', 'success')

    return render_template('/')
    window.location.href = "/";


def redirect_with_delay(location, delay):
    """Redirect to a given location after a delay."""
    return f"""
    <script>
        setTimeout(function() {{
            window.location.href = "{location}";
        }}, {delay} * 1000);
    </script>
    """



from flask import render_template

@app.route('/login', methods=['POST'])
def login_user():
    # Get username/email and password from the request
    username_or_email = request.form['username_or_email']
    password = request.form['password']

    # Hash the password to match with the database
    hashed_password = hash_password(password)

    # Check if the user exists in the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? OR email=?", (username_or_email, username_or_email))
    user = c.fetchone()

    if user:
        # Check if the password matches
        if user[3] == hashed_password:
            # Set the user session
            session['username'] = user[1]
            conn.close()
            # Redirect to index.html after successful login
            return redirect(url_for('index'))
        else:
            conn.close()
            return render_template('login.html', error_message='Invalid username/email or password', alert=True)
    else:
        conn.close()
        return render_template('login.html', error_message='User does not exist', alert=True)


# Route for file conversion
@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        # Check if files were uploaded
        if 'files[]' not in request.files:
            return jsonify(message="Файли не були завантажені")

        # Get uploaded files from the form
        uploaded_files = request.files.getlist('files[]')

        # Get chosen conversion format
        format = request.form['format']

        try:
            # Create a folder to save converted files
            os.makedirs('converted', exist_ok=True)

            # Process uploaded files
            converted_files = []
            for uploaded_file in uploaded_files:
                if uploaded_file.filename != '':
                    # Read the file as an image
                    img = Image.open(uploaded_file)

                    # Generate a new filename
                    new_filename = f"converted/{os.path.splitext(uploaded_file.filename)[0]}_converted.{format.lower()}"
                    # Save the image in the chosen format
                    img.save(new_filename)
                    converted_files.append(new_filename)

            # If only one file was uploaded, return it without creating a zip archive
            if len(converted_files) == 1:
                return send_file(converted_files[0], as_attachment=True)

            # If more than one file was uploaded, create a zip archive with all converted files
            zip_filename = 'converted_files.zip'
            with zipfile.ZipFile(zip_filename, 'w') as zip:
                for file in converted_files:
                    zip.write(file, os.path.basename(file))

            # Return the archive with all converted files
            return send_file(zip_filename, as_attachment=True)
        except Exception as e:
            return f"<script>alert('Помилка конвертації фотографій: {str(e)}');</script>"

# Маршрут для виходу з аккаунту
@app.route('/logout', methods=['POST'])
def logout():
    # Видалення даних сесії
    session.pop('username', None)
    # Перенаправлення на головну сторінку або куди вам потрібно
    return redirect(url_for('index'))

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Сторінка реєстрації
@app.route('/registration')
def registration():
    return render_template('registration.html')

# HTML login form
@app.route('/login')
def login_form():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
