import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
from_email = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

# Schedule meeting 3 days from now at 10 AM
meeting_datetime = datetime.now() + timedelta(days=3)
meeting_datetime = meeting_datetime.replace(hour=10, minute=0, second=0, microsecond=0)
meeting_date_str = meeting_datetime.strftime("%A, %B %d, %Y at %I:%M %p")

# Initialize OpenAI chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, openai_api_key=openai_api_key)

# Prepare prompt for generating email body
prompt = f"""
You are an assistant that writes professional meeting confirmation emails.
Write a friendly and professional email confirming a meeting scheduled for {meeting_date_str}.
Keep it concise and polite.
"""

messages = [HumanMessage(content=prompt)]

# Generate email body text using OpenAI
response = llm.invoke(messages)
email_body = response.content

print("Generated Email Body:\n", email_body)

# Function to send email
def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, email_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Send confirmation email
send_email("youremail@gmail.com", "Meeting Confirmation", email_body)
