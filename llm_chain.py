import os
from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from retriever import retrieve_context

# Load environment
load_dotenv()

# NVIDIA API KEY
api_key = os.getenv("NVIDIA_API_KEY")

# NVIDIA LLM
llm = ChatNVIDIA(
    model="ai-mixtral-8x7b-instruct",
    api_key=api_key,
    temperature=0.2,
    max_tokens=512
)

def ask_fedex_bot(query):

    # Retrieve context
    context = retrieve_context(query)

    if not context:
        return "No relevant information found."

    prompt = f"""
You are a FedEx customer support assistant.

Use ONLY the provided context to answer.

Context:
{context}

Question:
{query}

Provide a clear professional answer.
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"