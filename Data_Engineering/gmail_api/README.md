# 📬 Gmail API Module — CAPT Project

This module provides functionality to fetch and parse emails from any Gmail account using OAuth2, intended for use in the Candidate Analysis and Performance Tracker (CAPT) system.

It supports:
- Secure user authentication
- Clean parsing of Gmail content (subject, sender, body, etc.)
- Integration with backend systems or other data pipelines

---

## 📁 Folder Contents

gmail_api/
├── auth.py                  # Auth helper: login, token handling
├── gmail_fetcher.py         # Fetches and cleans emails
├── Tester.py                # Local test runner using the modules
├── credentials.json         # Google OAuth client secret (ignored)
├── token.json               # User session (ignored)
├── emails_test_output.json  # Sample output from local run (ignored)
├── README.md                # You're here

---

## 🔐 Security Notes

- DO NOT COMMIT:
  - credentials.json (OAuth client ID and secret)
  - token.json (OAuth refresh and access tokens)
  - emails_test_output.json (contains real user email content)
- These files are included in the root .gitignore.

---

## 🧠 Module Overview

### gmail_fetcher.py

Exports:

    fetch_user_emails(creds, since_datetime, until_datetime=None)
    upload_emails_to_s3(data, bucket_name, key_prefix="capt/")

- Accepts a Google Credentials object and a datetime range
- Returns a list of parsed Gmail messages with:
  - subject, from, snippet, thread_id, full body, timestamp
- Optionally uploads parsed emails to an S3 bucket

---

### auth.py

Exports:

    authenticate_user_interactively()
    load_user_credentials(user_email)

- Handles per-user Gmail OAuth and token refresh
- Stores tokens securely as: tokens/token_<email>.json

---

### Tester.py

A sample standalone script to:
- Authenticate a new user or load an existing one
- Fetch emails from the past 24 hours
- Save them to emails_test_output_<email>.json
- Upload them to S3 for downstream use

Usage:

    cd Data_Engineering
    python gmail_api/Tester.py

---

## 🧪 Sample Output (emails_test_output_<email>.json)

[
  {
    "id": "msg123",
    "subject": "Interview Invitation",
    "from": "recruiter@company.com",
    "snippet": "Thank you for applying...",
    "thread_id": "thread_001",
    "body": "Hi Roop,\nWe would like to invite you...",
    "timestamp": "2025-06-22T16:00:00Z"
  }
]

---

## 🛠 Requirements

Install all dependencies from the project root:

    pip install -r requirements.txt

Required packages:
- google-api-python-client
- google-auth
- google-auth-oauthlib
- beautifulsoup4
- boto3

---

## 🔁 Used By

- Data Parser Team — consumes cleaned output for ETL and job classification
- Backend Team — calls fetch_user_emails() for per-user Gmail data
- DevOps Team — deploys the modules and schedules them (if used with cron/jobs)

---

## 👥 Maintainer

Roop Sumanth Gundu  
This module is owned by the Data Engineering Team and is integration-ready for multi-user workflows.
