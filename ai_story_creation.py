import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)

messages = [
    HumanMessage(
        content="You are a creative writing assistant. Write a short story plot about a time-traveling detective who solves mysteries in the future."
    )
]

response = llm.invoke(messages)

print(response.content)
