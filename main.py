from flask import Flask, session, render_template, request, redirect, g, url_for
import pymongo
import hashlib
import os
import random
from settings import return_pass

# secret_token = os.getenv("TOKEN")
secret_token = return_pass()
# Connect to mongodb
mdb_str = f"mongodb+srv://henriupos:{secret_token}@henriu-pos-dab-try-56zuz.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(mdb_str)
db = client.posDB
collection_users = db.users  # Open the collection

app = Flask(__name__)
# app.secret_key = os.urandom(24)
app.secret_key = "jhdwfiheoiihf39"

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']



# @app.route('/')
# def index():
#     if g.user:
#         userdata = collection_users.find_one({"emp_nr": session['user']})
#         return render_template('index.html', user=session['user'], data=userdata)
#     return redirect(url_for('login'))
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)  # <- - Will drop the session if there is one.and
        check_db_for_user = collection_users.find_one({"emp_nr": request.form['uname']})
        if check_db_for_user:
            passme = hashlib.md5(request.form['password'].encode())
            passmef = passme.hexdigest()
            if passmef == check_db_for_user['password']:
                session['user'] = request.form['uname']
                return redirect(url_for('index'))
        return redirect(url_for('loginerror'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html')


@app.route('/loginerror')
def loginerror():
    data = {'errmsg': 'Invalid username or password.'}
    return render_template('loginerror.html', data=data)


if __name__ == "__main__":
    app.run(  # Starts the site
        host='0.0.0.0',  # Establishes the host, required for repl to detect the site
        port='2888',  # Randomly select the port the machine hosts on.
        debug=True
    )
