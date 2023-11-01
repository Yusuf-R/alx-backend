#!/usr/bin/env python3
""" Basic Flask app with Babel"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from datetime import datetime


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
    return render_template('index.html')


@babel.localeselector
def get_locale() -> str:
    """ get_locale function """
    # Implement locale from URL parameters
    # check if 'locale' parameter is in the request args
    if 'locale' in request.args:
        requested_locale = request.args.get('locale')
        # check if the requested locale is in the supported languages
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale
    # Locale from user settings
    # extract the user_id from the request headers
    user_id = request.headers.get('login_as')
    if user_id:
        # get the local_lang from the users dictionary
        local_lang = users[int(user_id)]['locale']
        if local_lang in app.config['LANGUAGES']:
            return local_lang
    # Locale from request header
    # extract the locale from the request headers
    local_lang = request.headers.get('locale')
    if local_lang in app.config['LANGUAGES']:
        return local_lang
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
    # display the current time on the home page
    # in the default format. For example:
    # Jan 21, 2020, 5:55:39 AM or 21 janv. 2020 à 05:56:28
    curr_utc = pytz.utc.localize(datetime.utcnow())
    time_zone = curr_utc.astimezone(pytz.timezone(get_timezone()))
    print(time_zone)


@babel.timezoneselector
def get_timezone():
    """ get_timezone function """
    # Implement timezone from URL parameters
    # check if 'timezone' parameter is in the request args
    if 'timezone' in request.args:
        req_tmz = request.args.get('timezone')
        # check if the requested timezone is in the supported timezones
        if req_tmz in pytz.all_timezones:
            return req_tmz
        else:
            raise pytz.exceptions.UnknownTimeZoneError
    # Implement timezone from user settings
    if 'login_as' in request.args:
        # get the local_timezone from the users dictionary
        user_id = request.args.get('login_as')
        print(user_id)
        if user_id:
            lc_tmz = users[int(user_id)].get('timezone')
            print(lc_tmz)
            if lc_tmz in pytz.all_timezones:
                return lc_tmz
        else:
            raise pytz.exceptions.UnknownTimeZoneError
    # Implement default behavior
    return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == '__main__':
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
