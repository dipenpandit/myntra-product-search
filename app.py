import streamlit as st
from src.vector_store.search import search
from config import DATA_PATH
import joblib
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)





# Sidebar: Get API Key from user input (stored only in memory)
st.sidebar.title("Gemini API Key Setup")
user_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if user_key:
    # Store key in session state
    st.session_state["GEMINI_API_KEY"] = user_key
    st.sidebar.success("API Key loaded for session ✅")
else:
    st.sidebar.warning("Please enter your Gemini API key to proceed.")

# App Title
st.title("🔎 Hybrid Semantic Search - Myntra Fashion Products")

# Block search if API key is not present
if "GEMINI_API_KEY" not in st.session_state:
    st.warning("❌ Please enter your Gemini API key in the sidebar to use the search.")
    st.stop()

# Search Input
query = st.text_input("Enter your search query:")
if st.button("Search"):
    if query.strip():
        with st.spinner("🔍 Searching..."):
            try:
                results = search(query)
                if results:
                    st.success("✅ Results found:")
                    for result in results:
                        payload = result.payload
                        st.header(payload.get('product_name', 'No Product Name'))
                        st.write(f"Brand: {payload.get('product_brand', 'N/A')}")
                        st.write(f"Gender: {payload.get('gender', 'N/A')}")
                        st.write(f"Price: ₹{payload.get('price', 'N/A')}")
                        st.write(f"Color: {payload.get('color', 'N/A')}")
                        st.write(f"Description: {payload.get('description', 'N/A')}")
                        st.markdown("---")
                else:
                    st.warning("No items found for your query. Please try a different search term.")
            except Exception as e:
                st.error(f"❗ Error: {e}")
    else:
        st.warning("Please enter a valid query.")
