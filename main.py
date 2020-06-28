from flask import Flask, render_template, session, redirect, request, url_for, g
from pyscripts.user import User
from pyscripts.details import Details
from pyscripts.database import Database
from pyscripts.functiondata import FunctionData
import pyscripts.pageformats as pageformats

app = Flask(__name__)
app.secret_key = '1234jhghgahugsjn'

Database.initialise(database="NOTmicroPOS", host="localhost", user="postgres", password="1234")


@app.before_request
def load_user():
    g.user = None
    if 'user_code' in session:
        g.user = User.load_from_db_by_user_code(session['user_code'])
    g.details = Details.load_details_from_db()


@app.errorhandler(404)
def invalid_route(e):
    if g.user:
        return render_template('errors/notfound.html',
                               pg_data=FunctionData.format_page_data('notfound', g.user.name))
    return redirect(url_for('login'))


@app.route('/')
def index():
    if g.user:
        return render_template('index.html',
                               pg_data=FunctionData.format_page_data('home', g.user.name))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()
        if User.login_user(request.form['user_code'], request.form['password']):
            session['user_code'] = request.form['user_code']
            return redirect(url_for('index'))
        return redirect(url_for('error', ptl='loginerror'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if g.user:
        for_display = None
        if request.method == 'POST':
            for_display = pageformats.dashboard_page_formats(request.form)
        return render_template('users/dashboard.html',
                               pg_data=FunctionData.format_page_data('dashboard', g.user.name),
                               for_display=for_display)
    return redirect(url_for('login'))


@app.route('/superuser', methods=['GET', 'POST'])
def superuser():
    if g.user:
        if g.user.account_type == FunctionData.load_from_db_by_name('superuser').access:
            for_display = None
            if request.method == 'POST':
                for_display = pageformats.superuser_page_formats(request.form)
            return render_template('users/superuser.html',
                                   pg_data=FunctionData.format_page_data('superuser', g.user.name),
                                   for_display=for_display)
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/test')
def test():
    return render_template('test.html', pg_data=FunctionData.format_page_data('home', g.user.name),
                           user=User.view_all_users())


@app.route('/error/<ptl>')
def error(ptl):
    return render_template('errors/error_page.html', pg_data=FunctionData.format_page_data(ptl, '-----'))


app.run(
    port=4995,
    debug=True,
    host='0.0.0.0'
)
