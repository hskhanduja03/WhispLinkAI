from langchain_qdrant import QdrantVectorStore
from embedder import embedding_model
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
import requests
import uuid
import numpy as np
from qdrant_client import QdrantClient


load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

def ensure_collection(collection_name, vector_size=768):
    url = f"{QDRANT_URL}/collections/{collection_name}"
    headers = {"api-key": QDRANT_API_KEY, "Content-Type": "application/json"}

    body = {
        "vectors": {
            "size": vector_size,
            "distance": "Cosine"
        }
    }

    try:
        response = requests.put(url, json=body, headers=headers, timeout=20)
        if response.status_code in [200, 201]:
            print(f"Collection '{collection_name}' ensured.")
        else:
            print(f"Could not create collection: {response.status_code} {response.text}")
    except Exception as e:
        print(f"HTTP error creating collection: {e}")

def store_documents(docs, collection_name):
    ensure_collection(collection_name)

    try:
        texts = [doc.page_content for doc in docs]
        embeddings = embedding_model.embed_documents(texts)

        payload = {
            "points": [
                {
                    "id": str(uuid.uuid4()),
                    "vector": list(embeddings[i]),
                    "payload": docs[i].metadata if docs[i].metadata else {"source": "unknown"},
                }
                for i in range(len(docs))
            ]
        }

        response = requests.put(
            f"{QDRANT_URL}/collections/{collection_name}/points?wait=true",
            headers={"api-key": QDRANT_API_KEY, "Content-Type": "application/json"},
            json=payload,
            timeout=30
        )

        if response.status_code in [200, 201]:
            print(f"Stored {len(docs)} documents in Qdrant.")
        else:
            print(f"Failed to insert documents: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Manual upload error: {e}")


def get_relevant_chunks(query, collection_name, top_k=5):
    try:
        # 1. Embed the user query
        embedded_query = embedding_model.embed_query(query)

        # 2. Prepare search payload
        payload = {
            "vector": embedded_query,
            "top": top_k,
            "with_payload": True
        }

        headers = {
            "api-key": QDRANT_API_KEY,
            "Content-Type": "application/json"
        }

        # 3. Hit Qdrant Cloud's search endpoint
        response = requests.post(
            f"{QDRANT_URL}/collections/{collection_name}/points/search",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code not in [200, 201]:
            print(f"Qdrant search failed: {response.status_code} {response.text}")
            return []

        results = response.json()["result"]
        print(f"🔍 Retrieved {len(results)} results.")

        # 4. Convert to LangChain Documents
        documents = [
            Document(page_content=res["payload"].get("text", ""),
                     metadata=res["payload"])
            for res in results
        ]
        return documents

    except Exception as e:
        print(f"Error in get_relevant_chunks: {e}")
        return []
