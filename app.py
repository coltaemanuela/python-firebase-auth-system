
from flask import Flask
from flask import current_app
from flask import render_template
import pyrebase

config = {  
	"apiKey": "yourApiKey",
	"authDomain":"yourprojectId.firebaseapp.com",
	"databaseURL":"https://yourprojectId.firebaseio.com",
	"storageBucket":   "yourstorageBucket"
} 

firebase = pyrebase.initialize_app(config)
# Get a reference to the database service
db = firebase.database()
data = {
    "name": "emma",
	"email":"coltaemanuela@gmail.com"
}
#db.child("users").push(data)
users = db.child("users").get()
print(users.val())


app = Flask(__name__)

@app.route('/')
def hello():
    # return 'Hello, World!'
	 return render_template('index.html')

if __name__ == '__main__':
	app.run()
