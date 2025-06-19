import msal
import requests
import re

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages"


def authenticate_msal(client_id, tenant_id):
    """
    Authenticate to Microsoft Graph API using MSAL device code flow.
    Returns an access token string.
    """
    app = msal.PublicClientApplication(client_id=client_id, authority=f"https://login.microsoftonline.com/{tenant_id}")
    scopes = ["Mail.Read"]
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        raise RuntimeError("Failed to initiate device flow")
    print(flow["message"])  # User instruction
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError("Failed to acquire token: " + str(result.get("error_description")))
    return result["access_token"]


def fetch_application_emails(token):
    """
    Fetch emails from Outlook Inbox using Microsoft Graph API.
    Filters for messages with 'application' in the subject.
    Returns a list of email dicts (id, subject, bodyPreview, receivedDateTime).
    """
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "$top": 10,
        "$filter": "contains(subject,'application')",
        "$select": "id,subject,bodyPreview,receivedDateTime"
    }
    resp = requests.get(GRAPH_API_ENDPOINT, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("value", [])


def filter_unprocessed_emails(emails, processed_ids):
    """
    Given a list of emails and a set of processed message IDs, return only unprocessed emails.
    """
    return [email for email in emails if email.get("id") not in processed_ids]


def parse_application_email(email):
    """
    Parse job title, company, and date from the email's subject/body using regex.
    Returns a dict with parsed fields or None if parsing fails.
    """
    subject = email.get("subject", "")
    body = email.get("bodyPreview", "")
    received = email.get("receivedDateTime", "")
    # Try subject first
    match = re.search(r"application for (.+?) at (.+?)(?:$|[.!?])", subject, re.IGNORECASE)
    if not match:
        # Try body
        match = re.search(r"application for (.+?) at (.+?)(?:$|[.!?])", body, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        company = match.group(2).strip()
        return {"title": title, "company": company, "applied_date": received}
    return None 