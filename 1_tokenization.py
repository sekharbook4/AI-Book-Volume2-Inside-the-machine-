# Import the AutoTokenizer class from Hugging Face's 
# transformers library
from transformers import AutoTokenizer

# Load the tokenizer for the "distilbert-base-uncased" model
# This automatically downloads the correct vocab and config for tokenizing inputs the way DistilBERT expects
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Define a sample sentence for tokenization
sentence = "The cat sat on the mat."

# Tokenize the sentence into subword units (WordPiece tokens)
tokens = tokenizer.tokenize(sentence)
# Convert the sentence into token IDs that the model understands
# This includes special tokens like [CLS] and [SEP] if applicable
token_ids = tokenizer.encode(sentence)

# Print the original sentence
print("Sentence:", sentence)
# Print the tokenized output
print("Tokens:", tokens)
# Print the token IDs (numerical representation used by the model)
print("Token IDs:", token_ids)
