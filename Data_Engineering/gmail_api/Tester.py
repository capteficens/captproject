from datetime import datetime, timedelta
from auth import authenticate_interactively, save_credentials
from gmail_fetcher import fetch_user_emails
import json

# Authenticate user (interactive browser login)
creds = authenticate_interactively()

# Optionally save token for reuse
save_credentials(creds)

# Set time range
since = datetime.utcnow() - timedelta(days=1)

# Fetch emails
emails = fetch_user_emails(creds, since_datetime=since)

# Save locally for validation
with open("filename = f"emails_{date_str}.json"", "w") as f:
    json.dump(emails, f, indent=2)

print(f" {len(emails)} emails fetched and saved to emails_test_output.json")
