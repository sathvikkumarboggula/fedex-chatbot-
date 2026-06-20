import os
from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from retriever import retrieve_context

# Load environment variables
load_dotenv()

# Get NVIDIA API Key
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

# Initialize NVIDIA LLM
llm = ChatNVIDIA(
    model="ai-mixtral-8x7b-instruct",
    api_key=api_key,
    temperature=0.2,
    max_tokens=512
)

def ask_fedex_bot(query):
    """
    Retrieve context from vector DB and generate answer
    """

    # Retrieve relevant context
    context = retrieve_context(query)

    if not context:
        return "I could not find relevant information in the FedEx knowledge base."

    prompt = f"""
You are FedAssist, an AI-powered FedEx logistics support assistant.

Your expertise includes:
- FedEx Services
- Shipping Guidance
- Shipment Tracking
- Customs Documentation
- Money-Back Guarantee (MBG) Policy
- Dimensional Weight
- Prohibited Items
- Delivery Exceptions
- Logistics Terminology
- Frequently Asked Questions

Rules:
1. Answer ONLY using the provided context.
2. Do NOT make up information.
3. If the answer is not available in the context, say:
   "I could not find that information in the FedEx knowledge base."
4. Be professional and concise.
5. Use bullet points when appropriate.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"