from flask import Flask
app = Flask(__name__)

@app.route('/_parseMarkers')
def parseMarkers():
    # return list of lat/longitude 
    return 'Hello world!'

if __name__ == '__main__':
    app.run()
