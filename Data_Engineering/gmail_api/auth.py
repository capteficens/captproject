import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "tokens.json"


def save_token(email, creds):
    """Save credentials for a user into the combined tokens.json store."""
    tokens = {}
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            tokens = json.load(f)

    tokens[email] = json.loads(creds.to_json())

    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f, indent=2)


def load_user_credentials(email):
    """Load stored credentials for a user from tokens.json."""
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError("tokens.json not found.")

    with open(TOKEN_FILE, "r") as f:
        tokens = json.load(f)

    if email not in tokens:
        raise FileNotFoundError(f"No token found for {email}")

    creds = Credentials.from_authorized_user_info(tokens[email], SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        save_token(email, creds)

    return creds


def authenticate_user_interactively():
    """Run first-time Gmail OAuth and store the user's token."""
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)
    profile = service.users().getProfile(userId='me').execute()
    email = profile["emailAddress"]

    save_token(email, creds)
    print(f"✅ Authenticated and saved token for: {email}")
    return creds, email
