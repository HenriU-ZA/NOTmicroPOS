from flask import Flask, render_template, session, redirect, request, url_for, g
from pyscripts.user import User
from pyscripts.database import Database
from pyscripts.functiondata import FunctionData

app = Flask(__name__)
app.secret_key ='1234jhghgahugsjn'

Database.initialise(database="NOTmicroPOS", host="localhost", user="postgres", password="1234")

@app.before_request
def load_user():
    g.user = None
    if 'user_code' in session:
        g.user = User.load_from_db_by_user_code(session['user_code'])


@app.route('/')
def index():
    if g.user:
        return render_template('index.html', pg_data=FunctionData.format_page_data('home', g.user.name))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()
        if User.login_user(request.form['user_code'], request.form['password']):
            session['user_code'] = request.form['user_code']
            return redirect(url_for('index'))
        return redirect(url_for('error', msg="Your login attempt failed!"))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



@app.route('/test')
def test():
    return render_template('test.html', user=g.user)

@app.route('/error')
def error():
    return render_template('error_page.html', pg_data=FunctionData.format_page_data('error', '-----', 'There was an error in your last request.'))


app.run(port=4995, debug=True)

