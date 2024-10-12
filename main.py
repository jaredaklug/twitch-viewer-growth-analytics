import os
from dotenv import load_dotenv
import requests
import json

# Data Ingestion Pipeline
## Objective: Set up script to be run every hour to pull and store data every hour from a specific twitch stream
## Target Stream: GamesDoneQuick
# Load environment variables
load_dotenv()

# Twitch API credentials from environment variables
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

# Load environment variables
load_dotenv()

# Twitch API credentials from environment variables
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

def get_oauth_token():
    # Set up oauth token
    #doc: https://dev.twitch.tv/docs/api/get-started/
    url = 'https://id.twitch.tv/oauth2/token'
    params = {'client_id':CLIENT_ID,
              'client_secret':CLIENT_SECRET,
              'grant_type':'client_credentials'
        }

    oauth = requests.post(url, params = params)
    return oauth.json()['access_token']

def get_stream_data(oauth_token, user_login='GamesDoneQuick'):
    # Set up get request for specific stream information
    url = 'https://api.twitch.tv/helix/streams'
    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Client-Id': CLIENT_ID
    }

    params = {'user_login':user_login}

    r = requests.get(url, headers=headers, params=params)
    # Return data if nothing available return None so downstream process can stop
    return r.json()

def process_stream_data(stream_data):
    if not stream_data:
        return None



if __name__ == "__main__":
    oauth = get_oauth_token()
    stream_data = get_stream_data(oauth_token=oauth)
    print(json.dumps(stream_data, indent=2))