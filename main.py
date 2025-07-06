import streamlit as st
from scraper import scrape_text_and_images
from embedder import split_text
from vectorstore import store_documents
from rag_pipeline import ask_question
from utils import generate_collection_name

st.set_page_config(page_title="RAG from URL")
st.title("🧠 Chat with Any Website")

url = st.text_input("Enter website URL")
question = st.text_input("Ask a question")

if url and st.button("Process URL"):
    with st.spinner("Scraping and embedding..."):
        text, images = scrape_text_and_images(url)
        if not text.strip():
            st.error("Couldn't extract readable content from this page. Try another URL.")
        else:
            chunks = split_text(text)
            if images:
                chunks[0].metadata["images"] = images
            collection = generate_collection_name(url)
            store_documents(chunks, collection)
            st.session_state["collection"] = collection
            st.success("Ingested and ready!")

if question and "collection" in st.session_state:
    response = ask_question(question, st.session_state["collection"])
    st.markdown("**Answer:**")
    st.write(response)
