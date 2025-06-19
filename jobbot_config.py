import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

CONFIG_VARS = [
    'NOTION_TOKEN',
    'NOTION_DATABASE_ID',
    'OUTLOOK_CLIENT_ID',
    'OUTLOOK_TENANT_ID',
]

PROCESSED_IDS_PATH = Path.home() / '.jobbot_processed.json'

def load_env():
    """Load and return required environment variables as a dict. Raises if missing."""
    config = {}
    for var in CONFIG_VARS:
        value = os.getenv(var)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {var}")
        config[var] = value
    return config

def load_processed_ids():
    """Load processed Outlook message IDs from the local JSON file. Returns a set."""
    if not PROCESSED_IDS_PATH.exists():
        return set()
    with open(PROCESSED_IDS_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return set(data)
        except Exception:
            return set()

def save_processed_ids(ids):
    """Save the set of processed Outlook message IDs to the local JSON file."""
    with open(PROCESSED_IDS_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(ids), f) 