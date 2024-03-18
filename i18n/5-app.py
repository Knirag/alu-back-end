#!/usr/bin/env python3
"""
This Flask application demonstrates basic setup with Babel for internationalization.

Key features include:

- Retrieving user locale from request arguments
- Using parameterized templates for dynamic content
- Forcing a specific locale through a URL parameter
"""

from typing import Union
from flask import Flask, render_template, request, g
from os import getenv
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration for the application"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object('5-app.Config')


@app.before_request
def before_request():
    """
    This function is called before each request.
    Sets the current user based on login arguments.
    """
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """
    Selects the best locale based on user preferences and supported languages.
    - Checks for a 'locale' parameter in the URL.
    - If valid, uses that locale.
    - Otherwise, falls back on the user's preferred language from browser settings,
      matching it with the application's supported languages.
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/", methods=["GET"], strict_slashes=False)
def hello_world() -> str:
    """
    Renders the main template (5-index.html).
    """
    return render_template('5-index.html')


def get_user() -> Union[dict, None]:
    """
    Retrieves user information based on login arguments.
    - Checks for a 'login_as' parameter in the URL.
    - If present, tries to find the corresponding user in the user dictionary.
    - Returns the user dictionary if found, otherwise returns None.
    """
    if request.args.get('login_as'):
        user = int(request.args.get('login_as'))
        if user in users:
            return users.get(user)
    else:
        return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")

