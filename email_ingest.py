import msal
import requests
import re


def authenticate_msal(client_id, tenant_id):
    """
    Authenticate to Microsoft Graph API using MSAL device code flow.
    Returns an access token string.
    """
    pass


def fetch_application_emails(token):
    """
    Fetch emails from Outlook Inbox using Microsoft Graph API.
    Filters for messages with 'application' in the subject.
    Returns a list of email dicts (id, subject, bodyPreview, receivedDateTime).
    """
    pass


def filter_unprocessed_emails(emails, processed_ids):
    """
    Given a list of emails and a set of processed message IDs, return only unprocessed emails.
    """
    pass


def parse_application_email(email):
    """
    Parse job title, company, and date from the email's subject/body using regex.
    Returns a dict with parsed fields or None if parsing fails.
    """
    pass 