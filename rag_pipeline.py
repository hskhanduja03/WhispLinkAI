from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from vectorstore import get_relevant_chunks

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

def ask_question(question, collection_name):
    try:
        docs = get_relevant_chunks(question, collection_name)
    except Exception as e:
        return f"Retrieval failed: {e}"

    if not docs:
        return "🤷 No relevant information found in the document. Try rephrasing your question."

    context = "\n\n".join(doc.page_content for doc in docs[:5])

    prompt = [
        {
            "role": "system",
            "content": (
                "You're an intelligent and helpful assistant. "
                "A user will ask you questions based on content extracted from a specific webpage. "
                "Use the provided context and your general knowledge to answer clearly and accurately. "
                "If the answer isn’t present in the context, try to find it in your knowledge base — "
                "and if it still doesn’t exist, be honest and let the user know — don’t guess. "
                "Keep your tone friendly, concise, and helpful."
                "Do not answer queries outside the context of the document."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"LLM Error: {e}"
