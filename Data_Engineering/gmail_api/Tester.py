from auth import load_user_credentials
from gmail_fetcher import fetch_user_emails, upload_emails_to_s3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
import os

# ==== CONFIG ====
TOKEN_FILE = "tokens.json"
OUTPUT_DIR = "outputs"
BUCKET_NAME = "captprojectdata"
TIMEZONE = ZoneInfo("America/Denver")
SINCE = datetime.now(TIMEZONE) - timedelta(days=1)

# ==== Load All Saved Users ====
if not os.path.exists(TOKEN_FILE):
    print("No tokens found. Please authenticate at least one user first.")
    exit(1)

with open(TOKEN_FILE, "r") as f:
    tokens = json.load(f)

known_users = list(tokens.keys())
print(f"Found {len(known_users)} user(s): {', '.join(known_users)}")

# ==== Fetch Emails ====
emails = []

for user_email in known_users:
    print(f"\nFetching emails for: {user_email}")
    try:
        creds = load_user_credentials(user_email)
        user_emails = fetch_user_emails(creds, since_datetime=SINCE)

        # Tag user and append
        for email in user_emails:
            email["user"] = user_email

        emails.extend(user_emails)
        print(f"{len(user_emails)} emails fetched for {user_email}")
    except Exception as e:
        print(f"Failed to fetch emails for {user_email}: {e}")

# ==== Save Combined Output ====
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"emails_{date_str}.json"
local_path = os.path.join(OUTPUT_DIR, filename)

with open(local_path, "w") as f:
    json.dump(emails, f, indent=2)
print(f"\nEmails saved locally to: {local_path}")

# ==== Upload to S3 ====
bucket_name = "captprojectdata"
s3_uri = upload_emails_to_s3(emails, bucket_name)
print(f"Uploaded to S3: {s3_uri}")
