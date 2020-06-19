from flask import Flask, render_template, session, redirect, request, url_for, g
from user import User
from database import Database

app = Flask(__name__)
app.secret_key ='1234jhghgahugsjn'

Database.initialise(database="NOTmicroPOS", host="localhost", user="postgres", password="1234")

@app.before_request
def load_user():
    if 'user_code' in session:
        g.user = User.load_from_db_by_user_code(session['user_code'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)


app.run(port=4995, debug=True)

