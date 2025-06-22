import base64
import json
import tempfile
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
from googleapiclient.discovery import build
import boto3

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
    # Build query string
    query = "in:anywhere"
    if since_datetime:
        query += f" after:{int(since_datetime.timestamp())}"
    if until_datetime:
        query += f" before:{int(until_datetime.timestamp())}"

    # Gmail API paginated fetch
    messages = []
    page_token = None

    while True:
        response = service.users().messages().list(
            userId='me',
            q=query.strip(),
            maxResults=500,
            pageToken=page_token
        ).execute()

        messages.extend(response.get('messages', []))
        page_token = response.get('nextPageToken')
        if not page_token:
            break

    # Parse message details
    emails = []

    for msg in messages:
        msg_detail = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()

        payload = msg_detail.get("payload", {})
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        from_email = next((h["value"] for h in headers if h["name"] == "From"), "")
        to_email = next((h["value"] for h in headers if h["name"] == "To"), "")
        snippet = msg_detail.get("snippet", "")
        thread_id = msg_detail.get("threadId", "")
        full_body = extract_body(payload)  

        # Convert Gmail internal timestamp to readable format (localized)
        internal_ts = int(msg_detail.get("internalDate", 0)) / 1000.0
        denver_tz = ZoneInfo("America/Denver")
        local_time = datetime.fromtimestamp(internal_ts, tz=denver_tz)

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "from": from_email,
            "to": to_email,
            "snippet": snippet,
            "thread_id": thread_id,
            "body": full_body,
            "timestamp": local_time.isoformat()
        })

    return emails


def upload_emails_to_s3(data, bucket_name):
    """
    Saves the email data to a temporary .json file and uploads it to S3.
    
    :param data: List of emails (from fetch_user_emails)
    :param bucket_name: Name of the S3 bucket
    :param key_prefix: S3 key prefix/folder (default: "capt/")
    :return: Full S3 URI (s3://bucket/prefix/file.json)
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"emails_{timestamp}.json"
    s3_key = f"capt/{filename}"

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
        json.dump(data, tmp, indent=2)
        tmp_path = tmp.name

    s3 = boto3.client("s3")
    s3.upload_file(tmp_path, bucket_name, s3_key)

    return f"s3://{bucket_name}/{s3_key}"
