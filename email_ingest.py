from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import base64
import re
import datetime
from llm_extract import extract_fields_with_llm

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
    internal_date = email.get("internalDate", "")
    if internal_date:
        dt = datetime.datetime.utcfromtimestamp(int(internal_date) / 1000)
        received = dt.date().isoformat()
    else:
        received = ""
    llm_result = extract_fields_with_llm(subject, body)
    if llm_result:
        llm_result["applied_date"] = received
        return llm_result
    return None


def filter_application_emails(emails, processed_ids):
    return [email for email in emails if email.get("id") not in processed_ids] 