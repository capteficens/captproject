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

- Accepts a Google Credentials object and a datetime range
- Returns a list of parsed Gmail messages with:
  - subject, from, snippet, thread_id, full body, timestamp

---

### auth.py

Exports:

    authenticate_interactively()
    save_credentials(creds)
    credentials_from_token_file(token_path)

Used for local/manual login with Gmail via browser (development/testing only).  
Production login is expected to be handled by the backend team.

---

### Tester.py

A sample standalone script to:
- Authenticate via browser
- Fetch emails from the past 24 hours
- Save them to emails_test_output.json

Usage:

    cd Data_Engineering
    python gmail_api/Tester.py

---

## 🧪 Sample Output (emails_test_output.json)

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

---

## 🔁 Used By

- Data Parser Team — consumes cleaned output for ETL and job classification
- Backend Team — calls fetch_user_emails() for per-user Gmail data
- DevOps Team — deploys the modules and schedules them (if used with cron/jobs)

---

## 👥 Maintainer

Roop Sumanth Gundu  
This module is owned by the Data Engineering Team and is integration-ready for multi-user workflows.
