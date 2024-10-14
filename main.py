import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# Data Ingestion Pipeline
## Objective: Set up script to be run every hour to pull and store data every hour from a specific twitch stream
## Target Stream: GamesDoneQuick
# Load environment variables
load_dotenv()

# Twitch API credentials from environment variables
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

# Set target stream and file to save out data
target_stream = 'GamesDoneQuick'
data_file = f'{target_stream}_stream_data.json'

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

def get_stream_data(oauth_token, user_login=target_stream):
    # Set up get request for specific stream information
    url = 'https://api.twitch.tv/helix/streams'
    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Client-Id': CLIENT_ID
    }
    params = {'user_login':user_login}

    r = requests.get(url, headers=headers, params=params)

    # Return data if nothing available return None so downstream process can stop
    if r.json()["data"]:
        return r.json()["data"][0]  # Return only the data field
    return None


def append_data(new_data):
    # Append timestamp to data and set up write pipeline
    # Will run every 30 minutes using Task Scheduler
    file_path = os.path.join(os.path.dirname(__file__), data_file)

    # Add timestamp to the new data
    timestamped_data = {
        "timestamp": datetime.now().isoformat(),
        "stream_data": new_data
    }

    # Check if file exists, if not write new file
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new data
    data.append(timestamped_data)

    # Write updated data back to file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Data appended to {file_path}")

def main():
    oauth = get_oauth_token()
    stream_data = get_stream_data(oauth_token=oauth)
    if stream_data:
        append_data(stream_data)
    else:
        print("No stream data available")

if __name__ == "__main__":
    main()