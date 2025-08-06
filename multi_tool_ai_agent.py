import os
from dotenv import load_dotenv
from openai import OpenAI
from duckduckgo_search import DDGS
import streamlit as st

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ----- Tool 1: Calculator -----
def calculator_tool(input_text: str) -> str:
    try:
        result = eval(input_text)
        return f"🧮 Result: {result}"
    except Exception as e:
        return f"Calculator error: {e}"

# ----- Tool 2: Real Web Search using DuckDuckGo -----
from duckduckgo_search import DDGS

def web_search_tool(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=1)
            if not results:
                return "No relevant results found."

            result = results[0]
            title = result.get("title", "No title")
            snippet = result.get("body", "No description")
            url = result.get("href", "")

            return f"🔍 {title}\n{snippet}\n{url}"

    except Exception as e:
        return f"Web search error: {e}"


# ----- Agent Logic -----
def run_agent(user_input: str) -> str:
    system_message = (
        "You are an intelligent agent that can use two tools:\n"
        "1. Calculator - Use for math expressions (e.g., '2+2', 'sqrt(16)').\n"
        "2. Web Search - Use for general knowledge or current events.\n\n"
        "Based on the user input, select the correct tool and prepare the query for it. "
        "Respond ONLY in this format:\n\n"
        "{\"tool\": \"calculator\", \"query\": \"2+2\"}\n"
        "or\n"
        "{\"tool\": \"web_search\", \"query\": \"What's the weather today?\"}"
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
        else:
            return "Unknown tool requested."
    except Exception as e:
        return f"Agent parsing error: {e}"

# ----- Streamlit UI -----
st.set_page_config(page_title="Agentic AI Assistant", page_icon="🤖")
st.title("🤖 Agentic AI Assistant")
st.markdown("Ask anything! Math, general knowledge, or current events.")

user_input = st.text_input("Your question:", placeholder="e.g., What's 25 * 12 or What's the weather in Paris?")
if user_input:
    with st.spinner("Thinking..."):
        result = run_agent(user_input)
    st.markdown(result)
