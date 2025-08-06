import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

loader = TextLoader("customer_faq.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(documents)

print(f"✅ Loaded and split into {len(documents)} chunks.")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = FAISS.from_documents(documents, embeddings)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)

qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

def ask_agent(question):
    result = qa_chain.invoke({"query": question})
    return result['result']  # extract answer from dict
if __name__ == "__main__":
    question = "How do I reset my password?"
    print("Q:", question)
    print("A:", ask_agent(question))
