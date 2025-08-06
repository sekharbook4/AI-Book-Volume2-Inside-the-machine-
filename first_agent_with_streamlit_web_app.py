import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Tool implementations (calculator, web_search, email_sender) same as before
def calculator_tool(input_text: str) -> str:
    try:
        result = eval(input_text)
        return f"The result is {result}."
    except Exception as e:
        return f"Calculator error: {e}"

def web_search_tool(query: str) -> str:
    if "weather" in query.lower():
        return "Today’s weather is sunny and 75°F."
    return "Simulated web search: No relevant information found."

def email_sender_tool(details: str) -> str:
    return f"Email sent successfully with the following details:\n{details}"

def run_agent(user_input: str) -> str:
    system_message = (
        "You are an intelligent agent that can use three tools:\n"
        "1. Calculator - Use for math expressions (e.g., '2+2').\n"
        "2. Web Search - Use for general knowledge or current events.\n"
        "3. Email Sender - Use to send emails. Input should include recipient, subject, and message.\n\n"
        "Respond ONLY in JSON format like:\n"
        '{"tool": "calculator", "query": "2+2"}\n'
        'or\n'
        '{"tool": "web_search", "query": "weather today"}\n'
        'or\n'
        '{"tool": "email_sender", "query": "recipient:... subject:... message:..."}'
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
    )
    try:
        tool_decision = response.choices[0].message.content.strip()
        tool_data = eval(tool_decision)
        tool = tool_data.get("tool")
        query = tool_data.get("query")

        if tool == "calculator":
            return calculator_tool(query)
        elif tool == "web_search":
            return web_search_tool(query)
        elif tool == "email_sender":
            return email_sender_tool(query)
        else:
            return "Unknown tool requested."
    except Exception as e:
        return f"Agent parsing error: {e}"

# Streamlit UI
st.title("AI Agent with Calculator, Web Search, and Email Tools")
user_input = st.text_input("Enter your question or command:")

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        answer = run_agent(user_input)
    st.markdown(f"**Agent:** {answer}")
