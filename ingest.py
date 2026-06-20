import os
import json
from dotenv import load_dotenv

from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

# Disable Chroma telemetry

os.environ["ANONYMIZED_TELEMETRY"] = "False"

# --------------------------------------------------

# Load .env file

# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

print("Current Directory:", BASE_DIR)
print("Looking for .env at:", ENV_PATH)

load_dotenv(ENV_PATH)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

print("API Key Found:", NVIDIA_API_KEY is not None)

if not NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

# --------------------------------------------------

# Data Folder

# --------------------------------------------------

DATA_FOLDER = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_FOLDER):
    raise FileNotFoundError(f"Data folder not found: {DATA_FOLDER}")

documents = []

print("\nLoading JSON files...\n")

# --------------------------------------------------

# Read All JSON Files

# --------------------------------------------------

for filename in os.listdir(DATA_FOLDER):
    if not filename.endswith(".json"):
        continue

filepath = os.path.join(DATA_FOLDER, filename)

print(f"Processing: {filename}")

try:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    document_title = data.get("document_title", filename)

    sections = data.get("sections", [])

    for section in sections:

        section_title = section.get("section_title", "")

        for item in section.get("content", []):

            paragraph = item.get("paragraph", "").strip()

            if not paragraph:
                continue

            heading = item.get("heading", "")

            documents.append(
                Document(
                    page_content=paragraph,
                    metadata={
                        "source_file": filename,
                        "document_title": document_title,
                        "section_title": section_title,
                        "heading": heading
                    }
                )
            )

except Exception as e:
    print(f"Error processing {filename}: {e}")
    print(f"\nTotal chunks loaded: {len(documents)}")

if len(documents) == 0:
    raise ValueError("No documents were loaded from JSON files.")

# --------------------------------------------------

# Create Embeddings

# --------------------------------------------------

print("\nCreating embeddings...\n")

embedding_model = NVIDIAEmbeddings(
model="nvidia/nv-embed-v1",
api_key=NVIDIA_API_KEY
)

# --------------------------------------------------

# Create Vector Database

# --------------------------------------------------

print("Building Chroma Vector Database...\n")

vectorstore = Chroma.from_documents(
documents=documents,
embedding=embedding_model,
persist_directory="./vectorstore"
)

print("\nVector Database Created Successfully!")
print(f"Embedded Chunks: {len(documents)}")
print("Saved To: ./vectorstore")
