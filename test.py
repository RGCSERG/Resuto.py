import requests

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1056928736294993961'
CLIENT_SECRET = 'xXm5FfQ31esDcBDJz8Q18XGSDZHzKbg_'
REDIRECT_URI = 'http://localhost:5000/oauth/callback'

def exchange_code(code):
    data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    r.raise_for_status()
    return r.json()

