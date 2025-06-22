import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# === Settings ===
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_PATH = "credentials.json"
TOKEN_DIR = Path("tokens")  # Folder to store tokens per user
TOKEN_DIR.mkdir(exist_ok=True)

def authenticate_user_interactively():
    """
    Run once per user. Authenticates and stores token as token_<email>.json
    """
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Get the user email from the token info
    service = build('gmail', 'v1', credentials=creds)
    profile = service.users().getProfile(userId='me').execute()
    user_email = profile['emailAddress']
    
    token_path = TOKEN_DIR / f"token_{user_email}.json"
    with open(token_path, "w") as f:
        f.write(creds.to_json())
    
    print(f"Auth complete. Token saved for: {user_email}")
    return creds, user_email

def load_user_credentials(user_email):
    """
    Load and refresh user credentials from stored token_<email>.json
    """
    token_path = TOKEN_DIR / f"token_{user_email}.json"
    if not token_path.exists():
        raise FileNotFoundError(f"No token found for {user_email}. Please authenticate first.")
    
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return creds
