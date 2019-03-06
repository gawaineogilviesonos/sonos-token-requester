"""
A one time use tool, that allows you to get a access and refresh token from
once you login with your Spotify account information. Be sure to copy and paste
the access and refresh tokens into settings.py or set them as linux ENV variables.

Flask web app for retrieving Authentication Tokens for Sonos Inc Web API.

The Authorization Code flow first gets a code then exchanges it for an access
token and a refresh token. Since the exchange uses your client secret key,
you should make that request server-side to keep the integrity of the key.
An advantage of this flow is that you can use refresh tokens to extend the
validity of the access token.
Source: https://developer.spotify.com/web-api/authorization-guide/#authorization-code-flow
"""

# For Python 2 and 3 import compatibility
try:
    # python 2
    from urllib import urlencode
except ImportError as e:
    # python 3
    from urllib.parse import urlencode

from base64 import b64encode
import json
import os

from flask import Flask, request, redirect, render_template, flash, url_for
from forms import AuthCodeForm
from settings import (
    TOKEN_URL,
    OAUTH_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI
)
import requests

# Initalizing Flask App
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a' # remember to update

def generate_headers():
    b64_encoded = b64encode((CLIENT_ID + ':'  + CLIENT_SECRET).encode())
    return  {'Authorization': 'Basic {}'.format(b64_encoded.decode()),
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get-auth-code', methods=['GET', 'POST'])
def get_auth_code():
    # To-Do: add feature to switch between environments
    form = AuthCodeForm()
    if form.validate_on_submit():
        state = b64encode(os.urandom(12))
        auth_query = {
            'client_id': CLIENT_ID,
            'response_type': form.response_type.data,
            'redirect_uri': REDIRECT_URI,
            'state': state,
            'scope': form.scope.data
        }
        full_url =  OAUTH_URL + "?" + urlencode(auth_query, doseq=True)
        return redirect(full_url)
    else:
        if form.errors:
            print(form.errors)
        flash('Error: All Fields are Required')
    return render_template('auth_code.html', form=form)

@app.route('/callback', methods=['GET'])
def callback():
    error = request.args.get('error', None)
    code = request.args.get('code', None)
    state = request.args.get('state', None)

    print(code, state)
    if code and state:
        request_body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        # request first time access_token and refresh_token for user
        res = requests.post(TOKEN_URL, data = request_body,
                            headers = generate_headers())
        if res.status_code == 200:
            res_json = json.loads(res.text)
            return render_template('token.html', success=res_json)
        else:
            return """{}""".format(res.text)
    return render_template('token.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc', debug=True)
