#!/usr/bin/env python3
""" Basic Flask app """

from flask import Flask, render_template, request
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


class Config:
    """ Config class """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)


app.config.from_object(Config)


@app.route('/', methods=['GET'])
def index():
    """ Index route """

    return render_template('4-index.html')


@babel.localeselector
def get_locale():
    """ get_locale function """
    # check if 'locale' parameter is in the request args
    if 'locale' in request.args:
        requested_locale = request.args.get('locale')
        # check if the requested locale is in the supported languages
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale
    # if not, use the default behavior
    return request.accept_languages.best_match(app.config['LANGUAGES'])

# babel.init_app(app, locale_selector=get_locale)


if __name__ == '__main__':
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
