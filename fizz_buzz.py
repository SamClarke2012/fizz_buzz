from flask import Flask, flash, render_template, request, redirect, session, g, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from datetime import datetime
from sqlite3 import dbapi2 as sqlite3
import config

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)

app.secret_key = 'abrakadabra'
app.config['DEBUG'] = True

DATABASE = 'fizz_buzz.db'

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(DATABASE)
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
	db = get_db()
	cur = db.execute('select * from Posts')
	posts = cur.fetchall()
	return render_template('index.html', posts=posts)

@app.route('/secret')
def secret():
	try:
		if session['logged_in']: 
			return render_template('secret.html')
	except:
		pass
	flash('You must be logged in to view this page!','danger')
	return redirect(url_for('login'))

@app.route('/logout')
def logout():
	if session['logged_in']:
		session['logged_in'] = False
		flash('You have been logged out','success')
	return redirect(url_for('index'))

def alpha_num(input_string):
		# Strip off non alpha-numeric chars
		import re, string 
		pattern = re.compile('[\W_]+')
		return pattern.sub('', input_string)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('/login.html')
	if request.method == 'POST':
		db = get_db()
		username = request.form['login-username']
		password = request.form['login-password']
		# Strip off non alpha-numeric chars
		username = alpha_num(username.decode('ascii', 'ignore'))
		password = alpha_num(password.decode('ascii', 'ignore'))
		cur = db.execute('select hash from Users where username=?',(username,)) 
		user_hash = cur.fetchone()
		if user_hash is not None:
			user_hash = user_hash[0]
			if check_password_hash(user_hash, password):
				flash("Logged in!", 'success')
				session['logged_in'] = True
				return redirect(url_for('index'))
		flash("Error, user not found or password invalid, dickhead.\n", 'danger')
		session['logged_in'] = False
		return redirect(url_for('login'))


def make_shell_context():
	return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
	manager.run()
