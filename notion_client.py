from notion_client import Client


def init_notion_client(token):
    """
    Initialize and return a Notion client using the provided integration token.
    """
    pass


def create_application_page(notion, database_id, title, company, applied_date, status, notes='', referral=''):
    """
    Create a new page in the specified Notion database with the given fields.
    Fields: Name (title), Company, Applied On (date), Status, Notes, Referral.
    Returns the created page object or raises on failure.
    """
    pass 