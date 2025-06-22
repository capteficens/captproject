import os
import json
import base64
import boto3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# SETTINGS
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
RAW_DATA_DIR = 'data/raw/'
S3_BUCKET = 'captprojectdata'  

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        #  Save new or refreshed token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def extract_body(payload):
    parts = payload.get("parts")
    if parts:
        for part in parts:
            mime_type = part.get("mimeType")
            body_data = part.get("body", {}).get("data")
            if mime_type == "text/html" and body_data:
                decoded = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
                return BeautifulSoup(decoded, "html.parser").get_text(separator="\n")
            if mime_type == "text/plain" and body_data:
                return base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")

    body_data = payload.get("body", {}).get("data")
    if body_data:
        decoded = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
        return BeautifulSoup(decoded, "html.parser").get_text(separator="\n")
    return ""

def fetch_new_emails(service):
    since = datetime.utcnow() - timedelta(days=1)
    query = f"after:{int(since.timestamp())}"
    result = service.users().messages().list(userId='me', q=query, maxResults=10000).execute()
    messages = result.get('messages', [])
    new_emails = []

    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_detail.get("payload", {})
        headers = payload.get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        from_email = next((h["value"] for h in headers if h["name"] == "From"), "")
        snippet = msg_detail.get("snippet", "")
        thread_id = msg_detail.get("threadId", "")
        full_body = extract_body(payload)

        email_data = {
            "id": msg["id"],
            "subject": subject,
            "from": from_email,
            "snippet": snippet,
            "thread_id": thread_id,
            "body": full_body
        }
        new_emails.append(email_data)

    return new_emails

def save_and_upload_to_s3(data, date_str):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    filename = f"emails_{date_str}.json"
    filepath = os.path.join(RAW_DATA_DIR, filename)

    # Save locally
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f" Saved {len(data)} emails to {filepath}")

    # Upload to S3
    s3 = boto3.client('s3')
    try:
        s3.upload_file(filepath, S3_BUCKET, f"capt/{filename}")
        print(f" Uploaded to S3: s3://{S3_BUCKET}/capt/{filename}")
    except Exception as e:
        print(f" S3 Upload failed: {e}")

def main():
    print(" Authenticating...")
    service = authenticate()
    print("Fetching new emails...")
    new_emails = fetch_new_emails(service)

    if new_emails:
        date_str = datetime.now().strftime('%Y-%m-%d')
        save_and_upload_to_s3(new_emails, date_str)
    else:
        print(" No new emails found in the past 24 hours.")

if __name__ == "__main__":
    main()
