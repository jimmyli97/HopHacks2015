from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/_processImage')
def processImage():
    # return food as json data
    return jsonify("Cookie")

@app.route('/')
def index():
    return render_template('uploadImage.html', name="uploadImage")

if __name__ == '__main__':
    #Turn this off in production
    app.run(debug=True)
