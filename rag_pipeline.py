from langchain_google_genai import ChatGoogleGenerativeAI
from vectorstore import get_retriever
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

def ask_question(question, collection_name):
    retriever = get_retriever(collection_name)
    docs = retriever.get_relevant_documents(question)
    
    if not docs:
        return "No relevant information found in the document. Try rephrasing your question."

    context = "\n\n".join(doc.page_content for doc in docs[:5])

    prompt = [
        {"role": "system", "content": "You are a helpful assistant. Use the context below to answer."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    response = llm.invoke(prompt)
    return response.content.strip()
