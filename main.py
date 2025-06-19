import argparse
from jobbot_config import load_env, load_processed_ids, save_processed_ids
from notion_api import init_notion_client, create_application_page
from email_ingest import authenticate_gmail, fetch_application_emails, filter_unprocessed_emails, parse_application_email
from manual_cli import prompt_manual_entry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manual', action='store_true', help='Manual entry mode')
    args = parser.parse_args()

    config = load_env()
    processed_ids = load_processed_ids()
    notion = init_notion_client(config['NOTION_TOKEN'])
    database_id = config['NOTION_DATABASE_ID']

    if args.manual:
        entry = prompt_manual_entry()
        create_application_page(
            notion,
            database_id,
            entry['title'],
            entry['company'],
            entry['applied_date'],
            entry['status'],
            entry.get('notes', ''),
            entry.get('referral', '')
        )
        print('Manual entry added to Notion.')
        return

    # Automated polling mode
    service = authenticate_gmail()
    emails = fetch_application_emails(service)
    new_emails = filter_unprocessed_emails(emails, processed_ids)
    added = 0
    for email in new_emails:
        parsed = parse_application_email(email)
        if parsed:
            create_application_page(
                notion,
                database_id,
                parsed['title'],
                parsed['company'],
                parsed['applied_date'],
                'Applied',
                '',
                ''
            )
            processed_ids.add(email['id'])
            added += 1
    if added:
        save_processed_ids(processed_ids)
    print(f'{added} new applications added to Notion.')


if __name__ == '__main__':
    main() 