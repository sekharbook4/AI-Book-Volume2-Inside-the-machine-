from langchain.output_parsers import RegexParser

def filter_output(text):
    forbidden_words = ["hate", "violence", "terrorism"]
    if any(word in text.lower() for word in forbidden_words):
        return "Sorry, I cannot provide that content."
    return text

response = "I love peace and kindness."
safe_response = filter_output(response)
print(safe_response)  # Output: I love peace and kindness.
