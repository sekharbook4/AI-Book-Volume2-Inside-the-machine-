import os
from dotenv import load_dotenv
import streamlit as st
import warnings

from langchain_openai import ChatOpenAI

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please set OPENAI_API_KEY in your .env file")
    st.stop()

# Initialize LLM with your OpenAI key
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)

# Custom moderation filter to catch unsafe words
def custom_moderation_filter(text):
    forbidden_words = ["hate", "violence", "terrorism", "racism", "kill"]
    lowered = text.lower()
    for word in forbidden_words:
        if word in lowered:
            return True
    return False

# Safe chatbot logic
def safe_chatbot(user_input):
    # Step 1: Check user input for unsafe content
    if custom_moderation_filter(user_input):
        return "Sorry, I cannot respond to that request."

    # Step 2: Compose a guarded prompt
    prompt = (
        "You are a helpful and responsible AI assistant. "
        "Answer politely and truthfully. "
        "If you don’t know the answer, say 'I don’t know.' "
        "Do not generate harmful, offensive, or unsafe content.\n\n"
        f"User: {user_input}\nAI:"
    )

    # Step 3: Get response from LLM
    response = llm.invoke([{"role": "user", "content": prompt}])

    # Step 4: Filter AI output
    if custom_moderation_filter(response.content):
        return "Sorry, my response was flagged as unsafe."

    return response.content

# Streamlit UI
st.title("Safe AI Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

user_text = st.text_input("You:")

if st.button("Send") and user_text:
    st.session_state.history.append({"role": "user", "content": user_text})
    with st.spinner("AI is thinking..."):
        reply = safe_chatbot(user_text)
    st.session_state.history.append({"role": "ai", "content": reply})

# Display conversation history
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**AI:** {chat['content']}")
