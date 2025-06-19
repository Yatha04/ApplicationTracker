from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import base64
import re

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def fetch_application_emails(service):
    results = service.users().messages().list(userId='me', q="subject:application", maxResults=10).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        subject = ''
        body = ''
        internalDate = msg_data.get('internalDate', '')
        for header in msg_data['payload']['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
        # Try to get plain text body
        if 'parts' in msg_data['payload']:
            for part in msg_data['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
        elif 'body' in msg_data['payload'] and 'data' in msg_data['payload']['body']:
            body = base64.urlsafe_b64decode(msg_data['payload']['body']['data']).decode('utf-8', errors='ignore')
        emails.append({'id': msg['id'], 'subject': subject, 'body': body, 'internalDate': internalDate})
    return emails


def filter_unprocessed_emails(emails, processed_ids):
    return [email for email in emails if email.get("id") not in processed_ids]


def parse_application_email(email):
    subject = email.get("subject", "")
    body = email.get("body", "")
    received = email.get("internalDate", "")

    patterns = [
        # application for [Job Title] at [Company]
        r"application for (.+?) at (.+?)(?:$|[.!?])",
        # thank you for your application to [Company]
        r"application to ([\w\s&.,'-]+)",
        # your application to [Company] for [Job Title]
        r"application to ([\w\s&.,'-]+) for ([\w\s&.,'-]+)",
        # we received your application for [Job Title]
        r"application for ([\w\s&.,'-]+)"
    ]

    # Try all patterns in subject and body
    for pattern in patterns:
        match = re.search(pattern, subject, re.IGNORECASE)
        if match:
            if pattern == patterns[0] and len(match.groups()) >= 2:
                return {"title": match.group(1).strip(), "company": match.group(2).strip(), "applied_date": received}
            elif pattern == patterns[1]:
                return {"title": "Unknown", "company": match.group(1).strip(), "applied_date": received}
            elif pattern == patterns[2] and len(match.groups()) >= 2:
                return {"title": match.group(2).strip(), "company": match.group(1).strip(), "applied_date": received}
            elif pattern == patterns[3]:
                return {"title": match.group(1).strip(), "company": "Unknown", "applied_date": received}
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            if pattern == patterns[0] and len(match.groups()) >= 2:
                return {"title": match.group(1).strip(), "company": match.group(2).strip(), "applied_date": received}
            elif pattern == patterns[1]:
                return {"title": "Unknown", "company": match.group(1).strip(), "applied_date": received}
            elif pattern == patterns[2] and len(match.groups()) >= 2:
                return {"title": match.group(2).strip(), "company": match.group(1).strip(), "applied_date": received}
            elif pattern == patterns[3]:
                return {"title": match.group(1).strip(), "company": "Unknown", "applied_date": received}

    # Fallback: if 'application' is present, create a generic entry
    if "application" in subject.lower() or "application" in body.lower():
        return {"title": "Unknown", "company": "Unknown", "applied_date": received}
    return None 