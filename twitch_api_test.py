import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Twitch API credentials from environment variables
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

def get_oauth_token():
    #https://dev.twitch.tv/docs/api/get-started/
    url = 'https://id.twitch.tv/oauth2/token'
    params = {'client_id':CLIENT_ID,
              'client_secret':CLIENT_SECRET,
              'grant_type':'client_credentials'
        }

    oauth = requests.post(url, params = params)
    return oauth.json()['access_token']

def get_top_games():
    oauth_token = get_oauth_token()
    headers = {
        'Authorization':f'Bearer {oauth_token}',
        'Client-Id':CLIENT_ID
    }

    #API call for top games
    url = 'https://api.twitch.tv/helix/games/top'
    r = requests.get(url, headers=headers)

    top_games = r.json()['data'][:9]

    top_game_names = [x['name'] for x in top_games]

    print(top_game_names)
    return

if __name__ == "__main__":
   get_top_games()