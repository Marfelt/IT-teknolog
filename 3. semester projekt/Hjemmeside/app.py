from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Remove the previous basicConfig
app = Flask(__name__)
app.logger.removeHandler(default_handler)

# Create a rotating file handler to write logs to both file and console
file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

# Add the file handler to the Flask app logger
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG

# Rest of your code...

db_file = 'fald_loc.db'

app.config['SECRET_KEY'] = secrets.token_hex(32)
app.permanent_session_lifetime = 5

# Define valid credentials
valid_username = 'user'
valid_password = 'password'

# Rate Limiting Configuration
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# Apply the rate limit decorator to specific routes
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == valid_username and password == valid_password:
            session['username'] = username
            session.permanent = False
            return redirect(url_for('index'))
        else:
            app.logger.warning('Failed login attempt for user: %s', username)
            return render_template('login.html', message='Invalid credentials')

    return render_template('login.html', message='')

# SQLite Database Setup
def get_fall_status():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT payload FROM fald_loc ORDER BY timestamp DESC LIMIT 1')
        result = cursor.fetchone()
    return result[0] if result else None

@app.route('/get_fall')
def get_fall():
    fall_status = get_fall_status()
    return jsonify({'fallen': fall_status})

@app.route('/')
def index():
    if 'username' in session:
        fall_status = get_fall_status()
        return render_template('index.html', username=session['username'], fall_status=fall_status)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        app.logger.info('User logged out: %s', session['username'])
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Provide the paths to your SSL certificate and key files
    ssl_certificate = 'C:/Users/T14s/Desktop/SIDSTE IOT/Programmering/HJEMMESIDE/openssl/OpenSSL-Win64/bin/cert.crt'
    ssl_private_key = 'C:/Users/T14s/Desktop/SIDSTE IOT/Programmering/HJEMMESIDE/openssl/OpenSSL-Win64/bin/private.key'
    
    # Use the provided paths in the ssl_context parameter
    ssl_context = (ssl_certificate, ssl_private_key)
    
    # Enforce HTTPS by setting the 'strict_slashes' and 'ssl_context' parameters
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', debug=True, port=8080, ssl_context=ssl_context)
