# Import flask dependencies
from flask import Blueprint, render_template

from app import google_api_key

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_map = Blueprint('map', __name__, url_prefix='/map')

# Set the route and accepted methods
@mod_map.route('/shelter/', methods=['GET', 'POST'])
def shelter():

    #TODO: get user location
    #TODO: show the map around the user
    #TODO: get shelter geo data
    #TODO: mark the shelters

    return render_template("map/shelter.html", api_key=google_api_key)