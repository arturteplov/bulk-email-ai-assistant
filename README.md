# Bulk Email AI Assistant - cR0tor 

A Python script to send bulk emails with dynamic templates, subject lines, and optional AI personalization. Includes structured CSV logging for tracking sent emails.

---

## Features

- Send bulk emails from a CSV list of recipients  
- Use multiple dynamic templates (`templates.py`) with placeholders like `{name}`, `{city}`, `{price}`, `{company}`  
- Randomly pick or customize subject lines (`subjects.py`)  
- Optional AI personalization via OpenAI API  
- Structured CSV logging for sent emails (`email_log.csv`)  
- Easy to test/demo with safe example recipients  

---

## Project Structure
project-root/
│
├── script.py # Main email sending script
├── templates.py # Email templates with placeholders
├── subjects.py # Subject line options
├── recipients.csv # Example recipients (user can upload)
├── requirements.txt # Python dependencies
└── README.md # This file

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/bulk-email-ai-assistant.git
cd bulk-email-ai-assistant
```

### 2. Create a virtual environment
```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables in a .env file
```bash
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_email_password_or_app_password
OPENAI_API_KEY=your_openai_api_key   # optional
```

### 5. Prepare your recipient CSV (recipients.csv)
```bash
name,email,city,price,company
Arthur,arthur@example.com,Toronto,$35,Meta
```

### 6. Run the script
```bash
python script.py
```
---

## How It Works

- Loads recipients from recipients.csv
- Randomly selects a template from templates.py and a subject from subjects.py
- Fills in placeholders ({name}, {city}, {price}, {company})
- Optional: Personalizes the message with OpenAI (requires API key)
- Sends email via SMTP
- Logs each email into email_log.csv with: Timestamp , Recipient info, Template used, Subject line, Status (SENT / FAILED), Error message (if any)

---

## Customizing Templates and Subjects
templates.py – Add or edit templates:
```bash
EMAIL_TEMPLATES = {
    "template_1": "Hi {name}, special offer in {city} for only {price}!",
    "template_2": "Hello {name}, check out {company}'s deals in {city}.",
}
```
subjects.py – Add or edit subject lines:
```bash
EMAIL_SUBJECTS = {
    "subject_1": "Don't miss this deal!",
    "subject_2": "Special offers just for you",
}
```

---

## Logging

- Loads recipients from recipients.csv
- Randomly selects a template from templates.py and a subject from subjects.py
- Fills in placeholders ({name}, {city}, {price}, {company})

## Optional AI Personalization 

- Comment OpenAI code in script.py and unset OPENAI_API_KEY in .env - if you don't need OpenAI API calls 
- If choose with AI, it will rewrite each email to sound friendly and professional 

## Safety Tips

- Use a dummy/test email first to ensure templates and logging work
- For Gmail, generate an app password for SMTP (see: Gmail App Passwords)

## Dependencies

See requirements.txt for all Python packages such as:
```bash
pandas – for reading CSV
python-dotenv – for environment variables
openai – optional AI personalization
requests – optional for external integrations
```
## License / Notes

- This project is for educational/demo purposes
- Emails sent to real users should comply with spam laws (GDPR / CAN-SPAM)
- Example recipient emails use example.com domains