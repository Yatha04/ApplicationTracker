from notion_client import Client


def init_notion_client(token):
    """
    Initialize and return a Notion client using the provided integration token.
    """
    return Client(auth=token)


def create_application_page(notion, database_id, title, company, applied_date, status, notes='', referral=''):
    """
    Create a new page in the specified Notion database with the given fields.
    Fields: Name (title), Company, Applied On (date), Status, Notes, Referral.
    Returns the created page object or raises on failure.
    """
    return notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
            "Company": {"rich_text": [{"text": {"content": company}}]},
            "Applied On": {"date": {"start": applied_date}},
            "Status": {"select": {"name": status}},
            "Notes": {"rich_text": [{"text": {"content": notes}}]},
            "Referral": {"rich_text": [{"text": {"content": referral}}]},
        }
    ) 