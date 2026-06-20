import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

# Load environment variables
load_dotenv()

# Get NVIDIA API Key
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

# Initialize embedding model
embedding = NVIDIAEmbeddings(
    model="nvidia/nv-embed-v1",
    api_key=api_key
)

# Load Chroma vector database
vectorstore = Chroma(
    persist_directory="./vectorstore",
    embedding_function=embedding
)

# Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

def retrieve_context(query):
    """
    Retrieve relevant context from vector database
    """

    try:
        docs = retriever.invoke(query)

        if not docs:
            return None

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        return context

    except Exception as e:
        print(f"Retriever Error: {e}")
        return None