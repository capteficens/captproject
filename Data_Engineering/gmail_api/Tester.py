from auth import authenticate_user_interactively, load_user_credentials
from gmail_fetcher import fetch_user_emails, upload_emails_to_s3
from datetime import datetime, timedelta, timezone
import json
import os

# Choose: authenticate a new user or load an existing one
mode = input("Type 'new' to authenticate a new Gmail user, or enter an existing Gmail address: ").strip()

if mode.lower() == 'new':
    creds, user_email = authenticate_user_interactively()
else:
    user_email = mode
    try:
        creds = load_user_credentials(user_email)
        print(f"Loaded saved token for {user_email}")
    except FileNotFoundError:
        print(f"No saved token found for {user_email}. Please run again and type 'new' to authenticate.")
        exit(1)

# Fetch emails from the past 24 hours
since = datetime.now(timezone.utc) - timedelta(days=1)
emails = fetch_user_emails(creds, since_datetime=since)

# Save test data locally (optional for data team testing)
filename = f"emails_test_output_{user_email.replace('@', '_')}.json"
with open(filename, "w") as f:
    json.dump(emails, f, indent=2)
print(f"Emails saved locally to: {filename}")

# Upload to S3 (optional)
bucket_name = "captprojectdata"  # Replace with your actual bucket
s3_uri = upload_emails_to_s3(emails, bucket_name)
print(f"Uploaded to S3: {s3_uri}")
