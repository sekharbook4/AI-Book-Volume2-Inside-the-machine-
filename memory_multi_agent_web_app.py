import os
from dotenv import load_dotenv
import streamlit as st
import warnings

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

# Suppress warnings
warnings.filterwarnings("ignore", message="LangChain agents will continue to be supported")

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please set OPENAI_API_KEY in your .env file")
    st.stop()

# Initialize LLM with your key
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)

# --- Define tools ---

def extract_key_points(feedback: str) -> str:
    prompt = f"Extract the key points from the following user feedback:\n{feedback}\n\nKey Points:"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

def summarize_key_points(key_points: str) -> str:
    prompt = f"Summarize the following key points clearly and concisely:\n{key_points}\n\nSummary:"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

def prepare_email(summary: str) -> str:
    prompt = f"Write a professional email to the team with the following summary:\n{summary}\n\nEmail:"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

extract_tool = Tool(
    name="extract_key_points",
    func=extract_key_points,
    description="Extracts key points from user feedback."
)

summarize_tool = Tool(
    name="summarize_key_points",
    func=summarize_key_points,
    description="Summarizes key points into a concise summary."
)

email_tool = Tool(
    name="prepare_email",
    func=prepare_email,
    description="Creates a professional email draft based on a summary."
)

tools = [extract_tool, summarize_tool, email_tool]

# --- Initialize conversation memory ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# --- Initialize agent with memory ---
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=False
)

# --- Streamlit UI ---
st.title("🤖 Multi-Agent AI Chatbot with Memory")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip():
    # Append user input to session chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("AI is thinking..."):
        # Run the agent and get response
        response = agent.run(user_input)
    # Append AI response to chat history
    st.session_state.chat_history.append({"role": "ai", "content": response})

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**AI:** {chat['content']}")
