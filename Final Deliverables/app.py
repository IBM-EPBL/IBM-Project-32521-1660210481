from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import re
import os
import tensorflow as tf
import ibm_db
app = Flask(__name__)
model = tf.keras.models.load_model('ckd.h5')

app.secret_key = 'my secret key'

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLSererCertificate=DigiCertGlobalRootCA.crt;UID=ygj69932;PWD=680oBgIoFrkRZTuc",'','')
picFolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
	if request.method=='POST':
		age = int(request.form['age'])
		bp  = float(request.form['bp'])
		sp  = float(request.form['sp'])
		al  = float(request.form['al'])
		su  = float(request.form['su'])
		rbc = float(request.form['rbc'])
		pc  = float(request.form['pc'])
		pcc = float(request.form['pcc'])
		bgr = float(request.form['bgr'])
		bu = float(request.form['bu'])
		sc = float(request.form['sc'])
		sod = float(request.form['sod'])
		pot = float(request.form['pot'])
		hemo = float(request.form['hemo'])
		pcv = float(request.form['pcv'])
		wc = float(request.form['wc'])
		htn = float(request.form['htn'])
		dm = float(request.form['dm'])
		cad = float(request.form['cad'])
		appet = float(request.form['appet'])
		pe = float(request.form['pe'])
		ane = float(request.form['ane'])
		ba = float(request.form['ba'])
		prediction=model.predict([[age, bp, sp, al, su, rbc, pc, pcc, bgr, bu, sc, sod, pot, hemo, pcv, wc, htn, dm, cad, appet, pe, ane, ba]])
		output = np.round(prediction)
		if output==0:
			return render_template('dash.html',prediction_text="Sorry! You have Chronic Kidney Disese...")
		return render_template('dash.html',prediction_text="Congrats!! You don't have Chronic Kidney Disease...")
	return render_template('dashboard.html')
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ' '
	loginPic = os.path.join(app.config['UPLOAD_FOLDER'],'login.png')
	if request.method == 'POST' and 'user' in request.form and 'password' in request.form:
		username = request.form['user']
		password = request.form['password']
		sql = "SELECT * FROM signup WHERE username = '"+username+"' AND password = '"+password+"'"
		stmt = ibm_db.exec_immediate(conn, sql)
		account = ibm_db.fetch_both(stmt)
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[1]
			msg = 'Logged in successfully !'
			return redirect(url_for('dashboard',text = msg))

		else:
			msg = '                  Incorrect username / password !'
	return render_template('log_in.html', errorMsg = msg,loginpic = loginPic)

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	registerImg = os.path.join(app.config['UPLOAD_FOLDER'],'login.png')
	if request.method == 'POST' and 'username' in request.form and 'pswd' in request.form and 'mail' in request.form :
		username = request.form['username']
		password = request.form['pswd']
		email = request.form['mail']
		sql = "SELECT * FROM signup WHERE username = '"+username+"'"
		stmt = ibm_db.exec_immediate(conn, sql)
		account = ibm_db.fetch_both(stmt)
		print(username)
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			print("Insert")
			ins = "INSERT INTO signup VALUES ('"+username+"','"+email+"','"+password+"')"
			prep_stmt = ibm_db.prepare(conn, ins)
			print("exec stmnt")
			ibm_db.execute(prep_stmt)
			msg = 'You have successfully registered !'

			return redirect(url_for('login'))

	elif request.method == 'POST':
		msg = 'Please fill out form !'
	# return redirect(url_for('register'))
	return render_template('signup.html', errorMsg = msg,registerImg=registerImg)


if __name__=="__main__":
    app.run(debug=True)


    
