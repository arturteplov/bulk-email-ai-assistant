import smtplib
from email.message import EmailMessage
import pandas as pd
import random
from dotenv import load_dotenv
import os
from openai import OpenAI
from templates import EMAIL_TEMPLATES 
from subjects import EMAIL_SUBJECTS
from datetime import datetime
import csv

#===============================
# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
openai_api_key = os.getenv("OPENAI_API_KEY") 
client = OpenAI(api_key=openai_api_key)
 

#===============================
# Load recipients
recipients = pd.read_csv("recipients.csv")  # columns: name,email,city,price etc - use pd.read_excel() for excel

#Helper function for CSV logging

LOG_FILE = "email_log.excel"

def log_email(row):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "name",
                "email",
                "city",
                "company",
                "price",
                "subject",
                "template_id",
                "status",
                "error",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

#===============================

# Optional: AI personalization  function (up to you if needed)
def personalize_message(template_text, name, city):
    """
    Uses OpenAI to make the email more engaging
    """
    prompt = f"Personalize this email for {name} in {city}:\n{template_text}\nMake it friendly but professional."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
#===============================

# Choose template dynamically
def select_template():
    template_id = random.choice(list(EMAIL_TEMPLATES.keys()))
    return template_id, EMAIL_TEMPLATES[template_id]


# Send emails (SMPT = connects to email server)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    
    for _, row in recipients.iterrows():
        name = row['name']
        email = row['email']
        city = row['city']
        price = row['price']
        company = row['company']
        
        # Pick template
        template_id, template_text = select_template()
        
        # Fill placeholders
        message_text = template_id.format(name=name, city=city, price=price, company = company)
        
        # Optional: AI personalization (if you don't need AI, remove and run static script as well)
        if openai_api_key:
           message_text = personalize_message(message_text, name, city) 
        
        # Create email
        msg = EmailMessage()
        msg['Subject'] = random.choice(list(EMAIL_SUBJECTS.values()))
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg.set_content(message_text)
        
        #Sent
        try:
            smtp.send_message(msg)
            log_email({
                "timestamp": datetime.now().isoformat(),
                "name": name,
                "email": email,
                "city": city,
                "company": company,
                "price": price,
                "subject": msg["Subject"],
                "template_id": template_id,
                "status": "SENT",
                "error": "",
            })
            print(f"Sent email to {name} ({email})")

        except Exception as e:
            log_email({
                "timestamp": datetime.now().isoformat(),
                "name": name,
                "email": email,
                "city": city,
                "company": company,
                "price": price,
                "subject": msg["Subject"],
                "template_id": template_id,
                "status": "FAILED",
                "error": str(e),
            })

            print(f"Failed to send to {email}: {e}")

    

