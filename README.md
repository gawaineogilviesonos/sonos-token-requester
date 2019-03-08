# sonos-token-requester
Request Sonos Web API Tokens for Integration
### Uses:
- Request access & refresh token for a Sonos user
- Allows a integration app to control a Sonos user's household

Source: https://developer.sonos.com/reference/authorization-api/

# Installation
1. Clone Git repo :`git clone https://github.com/gawaineogilviesonos/sonos-token-requester.git`
2. Change directory: `cd sonos-token-requester`
3. Create a python virtual environment: `virtualenv venv`
4. Activate python virtual environment: `source venv/bin/activate`
5. Install required libraries via PIP: `pip install -r requirements.txt`

# Configure Token-requester to use your CLIENT ID & CLIENT SECRET
1. Update `settings.py` with your client key and secret as well as extra configs to your liking (ex. REDIRECT_URI):
```
# OAuth Credentials
CLIENT_ID = "2330236c-0000-555c-cccb-ert449407d1e"
CLIENT_SECRET = "0000-d8d7-hyh78-bcda-91905f044bfd"
REDIRECT_URI = "https://0.0.0.0:5000/callback"
SCOPES_STR = "playback-control-all"

# Sonos Muse API Auth and Token Urls
OAUTH_URL = "https://api.sonos.com/login/v3/oauth"
TOKEN_URL = "https://api.sonos.com/login/v3/oauth/access"
```

# Run the application
1. Follow installation instructions above
2. Run via command line: `python token_fetcher/oauth_app.py`
