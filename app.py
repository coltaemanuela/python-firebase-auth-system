from flask import Flask
from flask import current_app
from flask import render_template
import pyrebase
from firebase_token_generator import create_token
import os
import json
from flask_restful import Resource, Api
from flask import request

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')
app = Flask('myapp', template_folder = tmpl_dir)

config = {  
	"apiKey": "yourApiKey",
	"authDomain":"yourprojectId.firebaseapp.com",
	"databaseURL":"https://yourprojectId.firebaseio.com",
	"storageBucket":   "yourstorageBucket",
	"serviceAccount":"./yourprojectId.json"
} 

firebase = pyrebase.initialize_app(config)

@app.route('/')
def hello():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def sign_in():
	email = request.form['email']
	password = request.form['password']
	auth = firebase.auth()
	user = auth.sign_in_with_email_and_password(email, password)
	user = auth.refresh(user['refreshToken'])
	user_data = auth.get_account_info(user['idToken'])
	return json.dumps (user_data)		

@app.route('/signup', methods=['POST'])
def sign_up():
	db = firebase.database()
	auth = firebase.auth()

	email = request.form['email']
	password = request.form['password']
	confirm_password = request.form['confirm_password']

	user_details = {
		"email": request.form['email'],		
		"telephone": request.form['telephone'],
		"username": request.form['username'],
		"street": request.form['street'],
		"city": request.form['city'],
		"postal_code": request.form['postal_code']
	}

	if password == confirm_password:
		db.child("users").push(user_details)
		auth.create_user_with_email_and_password(email, password)
		user = auth.sign_in_with_email_and_password(email, password)
		auth.send_email_verification(user['idToken'])

	return json.dumps(user_details)

if __name__ == '__main__':
	app.run()