from __future__ import with_statement

import os
import simplejson
import time
# import sqlite3
import MySQLdb
import MySQLdb.cursors
import twilio

from flask import Flask, render_template, redirect, url_for, escape, request, make_response, session, abort, g, flash, _app_ctx_stack
from flask_mail import Mail, Message
from werkzeug import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config.update(
    DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='oxmail.registrar-servers.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'info@hfpaginfo.com',
	MAIL_PASSWORD = 'trust1god'
	)

mail=Mail(app)

skey = os.urandom(24)
app.secret_key = skey

# DATABASE = '/home/brucegne/dbs/mytest.sqlite'

@app.route('/initdb')
def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = MySQLdb.connect('mysql.server','brucegne','ye110wsn0w','brucegne$test101')
        with app.open_resource('schema.sql') as f:
            db.cursor().execute(f.read())
        db.commit()
    return "DB created"

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

@app.route('/')
def index():
    fList = []
    for filename in os.listdir('/home/brucegne/mysite/static/uploads'):
        fList.append( filename )
    dbh = MySQLdb.connect('mysql.server','brucegne','ye110wsn0w','brucegne$test101')
    curr = dbh.cursor(MySQLdb.cursors.DictCursor)
    curr.execute('SELECT * FROM users ORDER BY id;')
    dta = curr.fetchall()
    dLen = str(len(dta))
    curr.close()
    prms = {
        'dta': dta,
        'dLen': dLen,
        'fList': fList,
    }

    resp = make_response( render_template('index.html',**prms), 200 )
    resp.set_cookie('foo','bar')
    return resp

@app.route('/list')
def dir_list():
	oHTML = []
	for filename in os.listdir('/home/brucegne/mysite/static/uploads'):
		oHTML.append( filename )
	return "<br />".join( oHTML )

@app.route('/new', methods=['POST'])
def new_post():
    ckvalue = request.cookies.get('foo','')
#    dbh = sqlite3.connect(DATABASE)
    dbh = MySQLdb.connect('mysql.server','brucegne','ye110wsn0w','brucegne$test101')
    curr = dbh.cursor()
#    id = request.args.get('id','0')
#    fn = request.args.get('fn','')
    id = request.form['id']
    fn = request.form['fn']
    sql = "INSERT INTO users (fullname) VALUES ('%s');" % (fn)
    curr.execute(sql)
    dbh.commit()
    curr.close()

    return redirect(url_for('index'))

@app.route('/test')
def testing():

    msg = Message(
           'Hello from PA and NameCheap',
           sender='info@hfpaginfo.com',
           recipients=
           ['brucegne@gmail.com'])
#    msg.body = "This is the email body"
    msg.html = render_template('error.html')
    with app.open_resource("/home/brucegne/mysite/static/uploads/pugshame.jpg") as fp:
        msg.attach("image.jpg", "image/jpg", fp.read())
    mail.send(msg)
    return "Sent"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/home/brucegne/mysite/static/uploads/' + f.filename)


    return redirect(url_for('index'))


