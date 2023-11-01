#!/usr/bin/env python3
""" Basic Flask app with Babel"""

from flask import Flask, render_template, request, g
from flask_babel import Babel

# ==============Task 0================================
# First you will setup a basic Flask app in 0-app.py.
# Create a single / route and an index.html template
# It will simply outputs “Welcome to Holberton” as page title (<title>)
# and “Hello world” as header (<h1>).
# ====================================================

# ==============Task 1================================
# Instantiate the Babel object in your app.
# Store it in a module-level variable named babel.
# In order to configure available languages in our app,
# you will create a Config class that has a LANGUAGES class
# attribute equal to ["en", "fr"].
# Use Config to set Babel’s default locale ("en") and timezone ("UTC").
# Use that class as config for your Flask app.
# ====================================================

# ==============Task 2================================
# Create a get_locale function with the babel.localeselector decorator.
# Use request.accept_languages to determine the best match
# with our supported languages.
# ====================================================

# ==============Task 3================================
# Use the _ or gettext function to parametrize your templates.
# Use the message IDs home_title and home_header.
# ====================================================

# ==============Task 4================================
# In this task, you will implement a way to force a particular
# locale by passing the locale=fr parameter to your app’s URLs.
# In your get_locale function, detect if the incoming request
# contains locale argument and ifs value is a supported locale,
# return it. If not or if the parameter is not present,
# resort to the previous default behavior.
# Now you should be able to test different translations
# by visiting http://127.0.0.1:5000?locale=[fr|en].
# ====================================================

# babel.init_app(app, locale_selector=get_locale)

# ==============Task 5================================
# Define a get_user function that returns a user dictionary
# or None if the ID cannot be found or if login_as was not passed.
# Define a before_request function and use the app.before_request
# decorator to make it be executed before all other functions.
# before_request should use get_user to find a user if any,
# and set it as a global on flask.g.user.
# In your HTML template, if a user is logged in, in a paragraph tag,
# display a welcome message otherwise display a default message
# as shown in the table below.
# ====================================================


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Config class """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)

app.config.from_object(Config)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ Index route """
    return render_template('5-index.html')


@babel.localeselector
def get_locale():
    """ get_locale function """
    # check if 'locale' parameter is in the request args
    if 'locale' in request.args:
        requested_locale = request.args.get('locale')
        # check if the requested locale is in the supported languages
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale
    else:
        # if not, use the default behavior
        return request.accept_languages.best_match(app.config['LANGUAGES'])
# babel.init_app(app, locale_selector=get_locale)


def get_user():
    """
    Returns a user dictionary if the ID can be found
    in the users dictionary and login_as was passed,
    git aotherwise returns None.

    :return: A dictionary containing user data or None.
    """
    try:
        user_id = request.args.get('login_as')
    # if so, get the data from the users dictionary
        return users[int(user_id)]
    except Exception:
        return None


@app.before_request
def before_request():
    """ set flask.g.user by calling get_user """
    g.user = get_user()


if __name__ == '__main__':
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
