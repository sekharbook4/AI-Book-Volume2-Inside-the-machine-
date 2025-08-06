import os
import openai
from dotenv import load_dotenv
import PyPDF2

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read PDF
def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Split text into smaller chunks
def split_text(text, max_chars=3000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# Analyze each chunk using OpenAI
def analyze_chunks(chunks):
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"🔍 Analyzing chunk {i + 1} of {len(chunks)}...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes documents."},
                {"role": "user", "content": f"Summarize this:\n\n{chunk}"}
            ],
            temperature=0.3
        )
        summaries.append(response.choices[0].message.content)
    return summaries

# Combine summaries
def summarize_document(pdf_path):
    text = read_pdf(pdf_path)
    chunks = split_text(text)
    summaries = analyze_chunks(chunks)
    return "\n\n---\n\n".join(summaries)

# Run the analysis
if __name__ == "__main__":
    final_summary = summarize_document("mybook.pdf")
    print("\n✅ Final Summary:\n")
    print(final_summary)
