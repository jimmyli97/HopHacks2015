# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

#import SMTPlib
import smtplib
import threading 


#app global parameters
address="127.0.0.1"
port=8080
rootPath="http://"+address+":"+str(port)+"/"
staticPath=rootPath+"static"

#keys
google_api_key = "AIzaSyB256H69Gt9oBbtaXuYrPqvx8BBNiTZhmo" #Dangerous practice!

# Define the WSGI application object
app = Flask(__name__, static_folder='static')

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home/home.html",static_path=staticPath)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',static_path=staticPath), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_map.controllers import mod_map as map_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(map_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# Start SMTP email daemon:
def email ():

	#server = smtplib.SMTP('smtp.gmail.com:465')
	server = smtplib.SMTP('127.0.0.1:25')
	server.ehlo()
	#server.starttls()

	#server.login('noreply.foodaid@gmail.com', '1234567890#')

	sender = 'noreply.foodaid@gmail.com'
	receivers = ['jimmy.jiajian.li@gmail.com']
	message = """From: Expiration Date Reminders <reminders@foodaid.com>
	To: Jimmy Li <jimmy.jiajian.li@gmail.com>
	Subject: Food aid reminder test
	AHHHHHHH
	"""
	server.sendmail(sender, receivers, message)
	server.quit()
	

t = threading.Thread(target=email)
t.start()









