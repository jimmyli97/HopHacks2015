from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/parseMarkers')
def parseMarkers():
    return render_template("parseMarkers.html")

if __name__ == '__main__':
    app.run()
