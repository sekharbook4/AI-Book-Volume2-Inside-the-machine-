import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to fetch weather data
def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The weather in {city} is {desc} with a temperature of {temp}°C."
        else:
            return f"⚠️ Error fetching weather: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"⚠️ Weather fetch failed: {str(e)}"

# Function to ask OpenAI for a smart suggestion
def ask_openai(prompt: str) -> str:
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",  # You can also use "gpt-4-turbo" or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI error: {str(e)}"

# Main logic
if __name__ == "__main__":
    city = input("Enter your city: ").strip()
    weather_info = get_weather(city)

    user_question = f"What should I wear today in {city}?"
    full_prompt = f"{weather_info}\n\n{user_question}"

    response = ask_openai(full_prompt)

    print("\n🌤️ Weather Info:\n", weather_info)
    print("\n🤖 Assistant Suggestion:\n", response)
