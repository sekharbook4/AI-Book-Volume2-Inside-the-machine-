import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Load and read documents
loader = TextLoader("research_articles.txt")
docs = loader.load()

# Initialize OpenAI chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, openai_api_key=api_key)

# Load summarization chain using map_reduce method
chain = load_summarize_chain(llm, chain_type="map_reduce")

# Generate and print summary
summary = chain.invoke(docs)

print("🔍 Research Summary:")
print(summary['output_text'])
