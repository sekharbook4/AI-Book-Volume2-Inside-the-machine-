"""
Agentic AI Server Health Monitor (LLM Edition)
---------------------------------------------
Continuously analyzes system metrics using GPT-5 for reasoning,
detects anomalies, identifies probable causes, and emails a summary
to the system administrator.

Requires:
    pip install openai
"""
import os
import smtplib
import json
import random
from datetime import datetime
from email.mime.text import MIMEText
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# ==============================
#  CONFIGURATION
# ==============================


ADMIN_EMAIL    = "domain@gmail.com"    # Destination address
SENDER_EMAIL   =  EMAIL_ADDRESS          # Sender address
SMTP_PASSWORD  =  EMAIL_PASSWORD         # Gmail App Password or SMTP key

# ==============================
#  1. INPUT FEED SIMULATION
# ==============================

def get_server_feed():
    """Simulates a live metrics feed. Replace this with your real server logs."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "server_ip": "192.168.1.23",
        "cpu_usage": random.randint(15, 99),
        "disk_usage": random.randint(55, 99),
        "reboots_this_week": random.randint(0, 4),
        "latency_ms": random.randint(5, 350),
        "packet_loss": random.choice([0, 1, 3, 6, 10]),
        "uptime_days": random.randint(0, 10)
    }

# ==============================
#  2. REFLECT + PLAN (LLM CORE)
# ==============================

def analyze_server_health(feed):
    """
    Uses GPT-5 (LLM) to reflect on the server data, detect anomalies,
    infer possible causes, and propose next actions.
    """

    prompt = f"""
    You are an autonomous Agentic AI for IT system monitoring.
    Analyze the following server metrics and logs. Detect anomalies, 
    summarize key issues, infer probable root causes, and recommend next actions.

    Present your output in this format:
    - Server Summary
    - Detected Issues
    - Probable Causes
    - Recommended Actions

    Metrics Data:
    {json.dumps(feed, indent=2)}
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert server health analyst AI agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    analysis = completion.choices[0].message.content.strip()
    return analysis

# ==============================
#  3. ACT (EMAIL NOTIFICATION)
# ==============================

def send_email(subject, body, to_email):
    """Send an email notification using Gmail SMTP."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print("✅ Email notification sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ==============================
#  4. MAIN AGENT LOOP
# ==============================

def main():
    print("🚀 Agentic Server Health Monitor (LLM Edition) starting...\n")

    # Step 1: Gather feed
    feed = get_server_feed()
    print(f"Collected Metrics:\n{json.dumps(feed, indent=2)}\n")

    # Step 2: Reflect + Plan using LLM
    print("Analyzing server health via GPT-5...")
    analysis = analyze_server_health(feed)
    print("\n--- LLM Analysis ---\n")
    print(analysis)
    print("\n--------------------\n")

    # Step 3: Act – Send email
    if any(keyword in analysis.lower() for keyword in ["critical", "alert", "issue", "reboot", "high", "fail"]):
        subject = f"🚨 Server Alert: {feed['server_ip']}"
    else:
        subject = f"✅ Server Health Summary: {feed['server_ip']}"

    send_email(subject, analysis, ADMIN_EMAIL)


if __name__ == "__main__":
    main()
