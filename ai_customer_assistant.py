import os
import sqlite3
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# 🔁 CHANGE THIS to your actual DB path
DB_PATH = r"C:\Users\sekha\Documents\customers.db"

# Function to fetch customer name from SQLite DB
def get_customer_name(customer_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM customers WHERE id=?", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "Customer not found."

# Function schema for OpenAI to understand what can be called
function_definitions = [
    {
        "name": "get_customer_name",
        "description": "Get the customer's name by their ID",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The unique ID of the customer",
                }
            },
            "required": ["customer_id"],
        },
    }
]

# Main function where agent makes decision to call a tool
def ask_openai_with_function_call(user_input: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        functions=function_definitions,
        function_call="auto",
        temperature=0.5,
    )

    message = response.choices[0].message

    # 🛠️ AI decides to call function
    if message.function_call:
        func_name = message.function_call.name
        arguments = message.function_call.arguments or "{}"
        args = json.loads(arguments)

        # Call Python function manually
        if func_name == "get_customer_name":
            customer_id = args.get("customer_id")
            function_result = get_customer_name(customer_id)

            # Second round: AI uses function result in response
            followup_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": user_input},
                    message,
                    {
                        "role": "function",
                        "name": func_name,
                        "content": function_result,
                    },
                ],
                temperature=0.5,
            )
            return followup_response.choices[0].message.content

    # If no function was called
    return message.content

# --- Main entry point ---
if __name__ == "__main__":
    print("Ask about a customer (e.g. 'Who is customer 123?')\n")
    user_input = input("Your question: ").strip()

    answer = ask_openai_with_function_call(user_input)
    print("\n🤖 AI Agent Response:\n", answer)
