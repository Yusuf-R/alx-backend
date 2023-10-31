#!/usr/bin/env python3
""" Basic Flask app """

from flask import Flask, render_template
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


class Config:
    """ Config class """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__, static_url_path='')
babel = Babel(app)

app.config.from_object(Config)


@app.route('/', methods=['GET'])
def index():
    """ Index route """
    return render_template('0-index.html')


if __name__ == '__main__':
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
