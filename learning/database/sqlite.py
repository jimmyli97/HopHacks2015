import random
import string
import sqlite3
from flask import Flask, current_app, g, render_template, jsonify, request, Response
from flask.json import JSONEncoder

app = Flask(__name__)

# Replace with SCRIPT_ROOT
DATABASE='test.db'

# Custom json encoder for handling YYYY-MM-DD
class DateJSONEncoder(JSONEncoder):
    def default(o):
        if isinstance(o, date):
            return date.strftime("%Y-%m-%d")
        else:
            super(DateJSONEncoder, self).default(o)

app.json_encoder = DateJSONEncoder

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Helpful DB functions
# Get row as dictionary: sqlite3.Row
# query: SQL query, args: args for execute(), one: if you only want first entry
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

# Route for viewing food database of a user
# TODO: SECURE THIS
@app.route('/_viewfoodtable/<foodtable_id>', methods=['GET'])
def view_foodtable(foodtable_id):
    # TODO: do user auth
    # TODO: THIS NEEDS TO BE SANITIZED
    try: 
        #cur = get_db().execute("SELECT * FROM users;")
        cur = get_db().execute("SELECT * FROM " + foodtable_id + ";")
        return jsonify(rows = cur.fetchall())
    except (KeyboardInterrupt, SystemExit): 
        print 'Keyboard interrupt or system exit'
        raise
    except:
        e = sys.exc_info()[0]
        print "Exception: %s" % e


# Route for adding a food to a user's food database 
# TODO: SECURE THIS
@app.route('/_addfood', methods=['POST'])
def add_food():
    # TODO: do user auth
    # TODO: THIS NEEDS TO BE SANITIZED
    data = request.form
    foodtable_id = data['foodtable_id']
    foodname = data['foodname']
    barcode = data.get('barcode')
    expiration = data['expiration']
    if barcode:
        query = "INSERT INTO " + foodtable_id + "(Name, Barcode, Expiration)" + " VALUES('" + foodname + "'," + barcode + ",'" + expiration + "');"
    else:
        query = "INSERT INTO " + foodtable_id + "(Name, Expiration)" + " VALUES('" + foodname + "', '" + expiration + "');"
        
    cur = get_db().execute(query)
    get_db().commit()
    return "Food successfully added!"

# Route for viewing the user table
# TODO: SECURE THIS
@app.route('/_viewusertable', methods=['GET'])
def view_usertable():
    cur = get_db().execute("SELECT * FROM users;")
    return jsonify(rows = cur.fetchall())

# Route for adding a new user to the user table
# TODO: SECURE THIS
@app.route('/_adduser', methods=['POST'])
def add_user():
    try: 
        print request.form
        user_id = request.form['user_id']
        # TODO: NOT GUARANTEED AGAINST COLLISIONS
        foodtable_id = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        cur = get_db().execute("INSERT INTO users(Username, FoodtableId) VALUES('" + user_id + "', '" +  foodtable_id + "');")
        cur = get_db().execute("CREATE TABLE " + foodtable_id + "(Id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Barcode INTEGER, Expiration TEXT NOT NULL);")
        get_db().commit()
    except (KeyboardInterrupt, SystemExit): 
        print 'Keyboard interrupt or system exit'
        raise
    except:
        e = sys.exc_info()[0]
        print "Exception: %s" % e
    return "User successfully added!" 

# Index page for creating new users and the table of all users and foodtable_id
# TODO: SECURE THIS
@app.route('/_admin', methods=['GET'])
def admin():
    # Create user table if it doesn't exist
    cur = get_db().execute("CREATE TABLE IF NOT EXISTS users(Username TEXT PRIMARY KEY, FoodtableId TEXT);")
    cur = get_db().execute("SELECT sqlite_version();")
    print "SQLite version: %s" % cur.fetchone()
    get_db().commit()
    return render_template("admin.html")

# User page for showing their food database and maintaining it
# TODO: SECURE THIS
@app.route('/user/<username>', methods=['GET'])
def show_database(username):
    cur = get_db().execute("SELECT foodtableid FROM users WHERE username='" + username + "';")
    data = cur.fetchone()
    data = "%s" % data
    return render_template("userDb.html", username=username, foodtableid=data)


@app.route('/map/shelter/', methods=['GET', 'POST'])
def shelter():

        #TODO: get user location
            #TODO: show the map around the user
                #TODO: get shelter geo data
                    #TODO: mark the shelters

    return render_template("shelter.html", api_key="AIzaSyB256H69Gt9oBbtaXuYrPqvx8BBNiTZhmo")

# Construct application context to start database
# with app.app_context():

if (__name__=='__main__'):
    app.run()


