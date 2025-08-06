import os
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY in your environment or .env file")

# Initialize ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)

# Custom moderation function
def moderate_text(text: str) -> str:
    forbidden_words = ["hate", "violence", "terrorism", "racism", "kill"]
    lowered = text.lower()
    for word in forbidden_words:
        if word in lowered:
            return "Content flagged as unsafe."
    return "Safe"

# Filter output for safety
def filter_output(response: str) -> str:
    if moderate_text(response) == "Content flagged as unsafe.":
        return "Sorry, my response was flagged as unsafe."
    return response

def safe_chatbot(input_text: str) -> str:
    # Step 1: Moderate user input
    if moderate_text(input_text) == "Content flagged as unsafe.":
        return "Sorry, I cannot respond to that request."

    # Step 2: Create prompt with guardrails
    prompt = (
        "You are a responsible AI assistant. "
        "Answer truthfully and politely. "
        "If you don’t know the answer, say 'I don’t know.'\n\n"
        f"User: {input_text}\nAI:"
    )

    # Step 3: Get response from ChatOpenAI (use invoke with HumanMessage)
    response = llm.invoke([HumanMessage(content=prompt)])

    # Step 4: Filter output for safety
    filtered_response = filter_output(response.content)
    return filtered_response

# Example usage
if __name__ == "__main__":
    print(safe_chatbot("Tell me a hateful joke."))
    print(safe_chatbot("Who won the Nobel Prize in 2024?"))
