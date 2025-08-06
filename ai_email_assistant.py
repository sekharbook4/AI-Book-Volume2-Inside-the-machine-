import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def send_email(to_email, subject, body_text, body_html=None):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = EMAIL_ADDRESS
        message["To"] = to_email

        message.attach(MIMEText(body_text, "plain"))
        if body_html:
            message.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)

        return "✅ Email sent successfully."
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"

def get_email_from_ai(user_input):
    prompt = f"""
You are an AI assistant. Based on the user input below, decide whether to send an email.
If yes, reply ONLY with these two lines exactly:

Subject: <subject line>
Body: <email body>

If no email is needed, reply with:

No email needed.

User input:
{user_input}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    user_input = input("Enter your request or update: ").strip()

    ai_response = get_email_from_ai(user_input)
    print("\nAI response:\n", ai_response)  # Debug print to see exact AI output

    if "Subject:" in ai_response and "Body:" in ai_response:
        lines = ai_response.splitlines()
        subject = next((line.replace("Subject:", "").strip() for line in lines if line.startswith("Subject:")), "No Subject")
        body = next((line.replace("Body:", "").strip() for line in lines if line.startswith("Body:")), "No Body")

        to_email = input("Enter recipient email: ").strip()
        result = send_email(to_email, subject, body, f"<p>{body}</p>")
        print(result)
    else:
        print("🛑 No email needed according to AI.")
