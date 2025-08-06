import streamlit as st
import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import PyPDF2
import openai

# --- Load .env ---
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMAIL = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
openai.api_key = OPENAI_API_KEY

db_path = r"C:\Users\<YOUR NAME>\Documents\customer_data.db"

# --- Database Setup ---
def get_customer_by_id(customer_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM customers WHERE id=?", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# --- Weather Fetch ---
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()
    if res.status_code == 200:
        return f"{data['weather'][0]['description'].title()}, {data['main']['temp']}°C"
    else:
        return "Weather data not available."

# --- Send Email ---
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()
        return "✅ Email sent!"
    except Exception as e:
        return f"❌ Error: {e}"

# --- PDF Read & Summarize ---
# Read PDF from file-like object (Streamlit uploader)
# --- Helper: Read PDF and extract text ---
def read_pdf(file):
    file.seek(0)  # Ensure pointer is at start
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        except Exception as e:
            st.warning(f"❌ Error reading page: {e}")
    return text

def split_text(text, max_chars=3000):
    raw_chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
    chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]
    return chunks

def analyze_chunks(chunks):
    summaries = []
    for i, chunk in enumerate(chunks):
        st.write(f"🔍 Analyzing chunk {i + 1} of {len(chunks)}...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes documents."},
                {"role": "user", "content": f"Summarize this:\n\n{chunk}"}
            ],
            temperature=0.3
        )
        summaries.append(response.choices[0].message["content"].strip())
    return summaries

def summarize_document(file):
    text = read_pdf(file)
    if not text.strip():
        return "⚠️ No extractable text found in PDF."

    chunks = split_text(text)
    if not chunks:
        return "⚠️ Text chunks are empty after splitting."

    summaries = analyze_chunks(chunks)
    combined_summary = "\n\n---\n\n".join(summaries)

    st.write("📝 Combined summary before final condensing:")
    st.write(combined_summary[:1000])  # Show sample of result

    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert summarizer."},
            {"role": "user", "content": f"Summarize this concise summary:\n\n{combined_summary}"}
        ],
        temperature=0.3
    )
    return final_response.choices[0].message["content"].strip()

# --- Streamlit UI ---
st.set_page_config(page_title="Smart Assistant", layout="wide")
st.title("🤖 AI-Powered Smart Assistant Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["📁 Customer DB", "☁️ Weather", "✉️ Email", "📄 PDF Summary"])

# --- Customer DB Tab ---
with tab1:
    st.header("🔎 Lookup Customer by ID")
    customer_id = st.text_input("Enter Customer ID")
    if st.button("Fetch Customer"):
        result = get_customer_by_id(customer_id)
        if result:
            st.success(f"Customer: {result[0]}, Email: {result[1]}")
        else:
            st.error("No customer found.")

# --- Weather Tab ---
with tab2:
    st.header("🌦️ Get Weather Info")
    city = st.text_input("Enter City")
    if st.button("Get Weather"):
        weather = get_weather(city)
        st.info(weather)

# --- Email Tab ---
with tab3:
    st.header("📧 Send Email")
    to_email = st.text_input("To")
    subject = st.text_input("Subject")
    body = st.text_area("Body")
    if st.button("Send Email"):
        result = send_email(to_email, subject, body)
        st.success(result)

# --- PDF Summary Tab ---
# --- PDF Summary Tab ---
with tab4:
    st.header("📄 Upload and Summarize PDF")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("Processing document..."):
            summary = summarize_document(uploaded_file)
        st.subheader("Summary:")
        st.write(summary)
