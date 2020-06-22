from flask import Flask, render_template, session, redirect, request, url_for, g
from pyscripts.user import User
from pyscripts.database import Database
from pyscripts.functiondata import FunctionData

app = Flask(__name__)
app.secret_key = '1234jhghgahugsjn'

Database.initialise(database="NOTmicroPOS", host="localhost", user="postgres", password="1234")


@app.before_request
def load_user():
    g.user = None
    if 'user_code' in session:
        g.user = User.load_from_db_by_user_code(session['user_code'])


@app.errorhandler(404)
def invalid_route(e):
    if g.user:
        return render_template('errors/notfound.html',
                               pg_data=FunctionData.format_page_data('notfound', g.user.name))
    return redirect(url_for('login'))


@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if g.user:
        if g.user.account_type == 'super':
            more = ""
            if request.method == 'POST':
                more = User.create_new_user(request.form['user_code'], request.form['user_name'])
            return render_template('users/adduser.html',
                                   pg_data=FunctionData.format_page_data('adduser', g.user.name),
                                   user=g.user,
                                   more=more)
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/')
def index():
    if g.user:
        return render_template('index.html',
                               pg_data=FunctionData.format_page_data('home', g.user.name),
                               user=g.user)
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


@app.route('/passreset', methods=['GET', 'POST'])
def passreset():
    if g.user:
        if g.user.account_type == 'super':
            if request.method == 'POST':
                return render_template('users/passreset.html',
                                       pg_data=FunctionData.format_page_data('viewuser', g.user.name), ##########################
                                       user=g.user,
                                       message=User.view_all_users())
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/viewuser')
def viewuser():
    if g.user:
        if g.user.account_type == 'super':
            users = ""
            return render_template('users/viewuser.html',
                                   pg_data=FunctionData.format_page_data('viewuser', g.user.name),
                                   user=g.user,
                                   users=User.view_all_users())
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/test')
def test():
    return render_template('test.html', pg_data=FunctionData.format_page_data('home', g.user.name),
                           user=User.view_all_users())


@app.route('/error/<ptl>')
def error(ptl):
    return render_template('errors/error_page.html', pg_data=FunctionData.format_page_data(ptl, '-----'))


app.run(port=4995, debug=True)
