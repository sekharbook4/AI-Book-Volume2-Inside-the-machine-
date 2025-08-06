import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ----- Tool 1: Calculator -----
def calculator_tool(input_text: str) -> str:
    try:
        result = eval(input_text)
        return f"The result is {result}."
    except Exception as e:
        return f"Calculator error: {e}"

# ----- Tool 2: Web Search (Simulated) -----
def web_search_tool(query: str) -> str:
    if "weather" in query.lower():
        return "Today’s weather is sunny and 75°F."
    return "Simulated web search: No relevant information found."

# ----- Agent Logic -----
def run_agent(user_input: str) -> str:
    # Ask OpenAI which tool to use and what the query is
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
        tool_data = eval(tool_decision)  # Parses the JSON-like output
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

# ----- Chat Loop -----
def chat():
    print("🤖 Agent is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        result = run_agent(user_input)
        print("Agent:", result)

if __name__ == "__main__":
    chat()
