#!/usr/bin/env python3
""" Basic Flask app """

from flask import Flask, render_template

# First you will setup a basic Flask app in 0-app.py.
# Create a single / route and an index.html template
# It will simply outputs “Welcome to Holberton” as page title (<title>)
# and “Hello world” as header (<h1>).


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Index route """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
