import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools import Tool
from langchain.agents import initialize_agent, AgentType

import warnings

warnings.filterwarnings(
    "ignore",
    message="LangChain agents will continue to be supported"
)

# Set your OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY in your environment or .env file")

# Initialize the ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)

# -------------------
# Tool 1: Extract Key Points
def extract_key_points(feedback: str) -> str:
    prompt = f"Extract the key points from the following user feedback:\n{feedback}\n\nKey Points:"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

extract_tool = Tool(
    name="extract_key_points",
    func=extract_key_points,
    description="Extracts key points from user feedback."
)

# -------------------
# Tool 2: Summarize Key Points
def summarize_key_points(key_points: str) -> str:
    prompt = f"Summarize the following key points clearly and concisely:\n{key_points}\n\nSummary:"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

summarize_tool = Tool(
    name="summarize_key_points",
    func=summarize_key_points,
    description="Summarizes key points into a concise summary."
)

# -------------------
# Tool 3: Prepare Email
def prepare_email(summary: str) -> str:
    prompt = f"Write a professional email to the team with the following summary:\n{summary}\n\nEmail:"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

email_tool = Tool(
    name="prepare_email",
    func=prepare_email,
    description="Creates a professional email draft based on a summary."
)

# -------------------
# Initialize the Agent with tools
tools = [extract_tool, summarize_tool, email_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# -------------------
# Interactive Chat Loop
def chat():
    print("🤖 Welcome to the Multi-Agent AI Chatbot!")
    print("Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        try:
            response = agent.invoke(user_input)
            print(f"\nAI: {response}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

# -------------------
if __name__ == "__main__":
    chat()
