import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_interactively():
    """
    Interactive OAuth login using credentials.json.
    Returns a Credentials object.
    """
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def credentials_from_token_file(token_path='token.json'):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

def save_credentials(creds, path='token.json'):
    with open(path, 'w') as token:
        token.write(creds.to_json())
