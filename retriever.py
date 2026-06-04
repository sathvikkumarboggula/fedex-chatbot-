import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

# Load env
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")

# Embedding model
embedding = NVIDIAEmbeddings(
    model="nvidia/nv-embed-v1",
    api_key=api_key
)

# Load vector DB
vectorstore = Chroma(
    persist_directory="./vectorstore",
    embedding_function=embedding
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


def retrieve_context(query):
    """
    Retrieve top matching documents
    """
    docs = retriever.invoke(query)

    if not docs:
        return None

    return "\n\n".join([doc.page_content for doc in docs])