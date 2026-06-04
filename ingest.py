import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import json
from dotenv import load_dotenv

from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

# Load env
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env")

# Load FAQ JSON
with open("fedex_structured_rag.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []

for item in data:
    question = item.get("question", "")
    answer = item.get("answer", "")

    content = f"Question: {question}\nAnswer: {answer}"

    documents.append(
        Document(
            page_content=content,
            metadata={"question": question}
        )
    )

# Embedding model
embedding = NVIDIAEmbeddings(
    model="nvidia/nv-embed-v1",
    api_key=api_key
)

# Create Chroma vector DB
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory="./vectorstore"
)

print("✅ Vector DB created successfully!")