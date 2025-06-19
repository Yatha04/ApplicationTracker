# ApplicationTracker

A Python tool to automatically track job application emails from your Gmail inbox and extract structured information using Large Language Models (LLMs).

## Overview
This project connects to your Gmail account, fetches job application-related emails, and uses an LLM to extract key details (such as company, position, and application date) from each email. The extracted data can be used for personal tracking, analytics, or integration with other tools.

## Features
- **Gmail Integration:** Securely connects to your Gmail account using OAuth2.
- **Automated Email Fetching:** Searches for emails with job application-related subjects.
- **LLM-Powered Extraction:** Uses an LLM to parse and extract structured information from email content.
- **Duplicate Filtering:** Avoids processing the same email multiple times.

## Getting Started

### Prerequisites
- Python 3.7+
- A Google account
- Access to an LLM API or local LLM (see below)

### 1. Clone the Repository
```sh
git clone https://github.com/Yatha04/ApplicationTracker.git
cd ApplicationTracker
```

### 2. Set Up Google API Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable the **Gmail API** for your project.
4. Go to **APIs & Services > Credentials**.
5. Click **Create Credentials > OAuth client ID**.
6. Choose **Desktop app** and create.
7. Download the `credentials.json` file and place it in the project root directory.

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. LLM Extraction Setup
This project uses an LLM to extract structured data from email content. By default, it calls the `extract_fields_with_llm` function (see `llm_extract.py`).

- You may need to configure your LLM API key or endpoint in `llm_extract.py` or via environment variables, depending on your LLM provider (e.g., OpenAI, local model, etc.).
- See `llm_extract.py` for details and adjust as needed for your LLM setup.

### 5. First Run & Authorization
- Run the application (e.g., `python main.py` or `python manual_cli.py`).
- On first run, a browser window will open for you to log in and authorize Gmail access.
- This will generate a `token.pickle` file for your account.

## Usage
- Use the provided scripts to fetch and process job application emails:
  - `python main.py` – Main entry point (customize as needed)
  - `python manual_cli.py` – Manual command-line interface
- The application will fetch recent job application emails, extract relevant fields using the LLM, and output or store the results as configured.

## Security Notice
- **Never commit `credentials.json` or `token.pickle` to git or share them publicly.**
- These files contain sensitive information unique to your Google account.
- Ensure your `.gitignore` file contains:
  ```
  credentials.json
  token.pickle
  ```
- If you accidentally commit these files, remove them from your git history and regenerate your credentials.

## License
See [LICENSE](LICENSE) for details.
