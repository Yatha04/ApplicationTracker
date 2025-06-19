import requests
import json
import os
import re

def extract_fields_with_llm(subject, body, lmstudio_url=None):
    if lmstudio_url is None:
        lmstudio_url = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1/chat/completions")
    prompt = f"""
        Extract the following information from this job application email:
        - Job Title
        - Company
        - Applied On (date, if present)
        - Status (default to \"Applied\" if not present)
        - Notes (optional)
        - Referral (optional)

        Email content:
        Subject: {subject}
        Body: {body}

        Return the result as a JSON object with keys: title, company, applied_date, status, notes, referral.
        """
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that extracts structured data from emails."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }
    response = requests.post(lmstudio_url, headers=headers, json=data)
    result = response.json()
    try:
        content = result["choices"][0]["message"]["content"]
        # Extract JSON from the response (between triple backticks or first {...})
        match = re.search(r'```(?:json)?\s*({[\s\S]+?})\s*```', content)
        if not match:
            # Fallback: try to find the first {...} block
            match = re.search(r'({[\s\S]+})', content)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
        else:
            print("LLM extraction failed: No JSON found in response.")
            return None
    except Exception as e:
        print("LLM extraction failed:", e)
        return None 