# Job Application Tracker Bot

A local Python agent that ingests Outlook "application confirmation" emails, parses key fields, and pushes them into a Notion database. Includes a manual CLI fallback for applications that don't generate a confirmation email.

## Features
- Automate ingestion of new applications via Outlook (Microsoft Graph API)
- Persist state so each email is processed exactly once
- Manual CLI entry for "no-email" cases
- Store all records in Notion for a rich, visual front end
- Run unattended on a local machine via cron

## Requirements
- Python 3.9+
- Notion integration token and database ID
- Azure AD app for Microsoft Graph API (Mail.Read scope)

## Setup
1. Clone this repo.
2. Copy `.env.example` to `.env` and fill in your credentials.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot (see usage below).

## Environment Variables
See `.env.example` for all required variables:
- `NOTION_TOKEN`: Notion integration secret
- `NOTION_DATABASE_ID`: Your Notion database ID
- `OUTLOOK_CLIENT_ID`: Azure AD app client ID
- `OUTLOOK_TENANT_ID`: Azure tenant ID

## Usage
- To run automatically (via cron):
  ```bash
  python main.py
  ```
- For manual entry:
  ```bash
  python main.py --manual
  ```

## State & Persistence
Processed Outlook message IDs are stored in `~/.jobbot_processed.json`.

## License
MIT
