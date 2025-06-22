import base64
from bs4 import BeautifulSoup
from datetime import datetime
from googleapiclient.discovery import build

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

def fetch_user_emails(creds, since_datetime=None, until_datetime=None):
    service = build('gmail', 'v1', credentials=creds)
    query = ""

    if since_datetime:
        query += f"after:{int(since_datetime.timestamp())} "
    if until_datetime:
        query += f"before:{int(until_datetime.timestamp())}"

    result = service.users().messages().list(userId='me', q=query.strip(), maxResults=1000).execute()
    messages = result.get('messages', [])
    emails = []

    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_detail.get("payload", {})
        headers = payload.get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        from_email = next((h["value"] for h in headers if h["name"] == "From"), "")
        snippet = msg_detail.get("snippet", "")
        thread_id = msg_detail.get("threadId", "")
        full_body = extract_body(payload)
        internal_ts = int(msg_detail.get("internalDate", 0)) / 1000.0

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "from": from_email,
            "snippet": snippet,
            "thread_id": thread_id,
            "body": full_body,
            "timestamp": datetime.utcfromtimestamp(internal_ts).isoformat() + "Z"
        })

    return emails
