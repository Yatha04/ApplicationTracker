def prompt_manual_entry():
    """
    Prompt the user interactively for job application fields:
    Job Title, Company, Applied On (YYYY-MM-DD), Status, Notes, Referral.
    Returns a dict with the collected data.
    """
    def get_required(prompt_text):
        while True:
            value = input(prompt_text).strip()
            if value:
                return value
            print("This field is required.")

    title = get_required("Job Title: ")
    company = get_required("Company: ")
    applied_date = get_required("Applied On (YYYY-MM-DD): ")
    status = get_required("Status: ")
    notes = input("Notes (optional): ").strip()
    referral = input("Referral (optional): ").strip()

    return {
        "title": title,
        "company": company,
        "applied_date": applied_date,
        "status": status,
        "notes": notes,
        "referral": referral,
    } 