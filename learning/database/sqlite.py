import sqlite3
from flask import Flask, current_app, g, render_template

app = Flask(__name__)

# Replace with SCRIPT_ROOT
DATABASE='/test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('DATABASE')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Helpful DB functions
# Get row as dictionary: sqlite3.Row
# query: SQL query, args: args for execute(), one: if you only want first entry
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Index page for creating databases for new users and listing all user tables
@app.route('/')
def index():
    # In application context
    cur = get_db().cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print current_app.name
    print 'Sqlite version %s' % data
    return render_template("index.html")

# User page for showing their database and maintaining it
@app.route('/user/<username>')
def show_database(username):
    # TODO: access database, print out user databaes
    return render_template("userDb.html")


# Construct application context to start database
# with app.app_context():

if (__name__=='__main__'):
    app.run()



