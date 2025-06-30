# 🔍 Myntra Fashion Product Search 
A hybrid semantic search system for Myntra fashion products combining vector similarity and LLM-powered filtering.


<img src="./img/system%20workflow.png" alt="System Workflow" width="1000" />

| Tools         |                                                                                          |
|---------------|----------------------------------------------------------------------------------------------|
| Streamlit     | <img src="https://docs.streamlit.io/logo.svg" alt="Streamlit Logo" width="50"/> |
| Qdrant       | <img src="https://logo.svgcdn.com/l/qdrant.svg" alt="Qdrant Logo" width="80" />               |
| Google Gemini | <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" alt="Google Logo" width="80"/>       |
| SBERT         | <img src="https://sbert.net/_static/logo.png" alt="SBERT Logo" width="82"/>                   |


## Features
- Search with embeddings: Uses `all-MinLM-16-v2` embeddings for similarity search on description of products.
- Keyword filter: Uses Gemini to extract filters from the user query.

## Tech Stack 

| Component       | Technology               |                
|-----------------|--------------------------|
| Vector Database | Qdrant Cloud             |
| Embeddings      | all-MinLM-16-v2          |
| NLP Processing  | Gemini API               |
| UI Framework    | Streamlit                |
| Data Pipeline   | Pandas + Joblib          |


## Run locally

1. Clone repository:
   ```bash
   git clone 'https://github.com/dipenpandit/myntra-product-search'
   cd myntra-product-search
   ```

2. Set up environment:
   ```bash
   python -m venv venv
   source venv/bin/activate     # linux/mac
   venv\Scripts\activate        # cmd windows
   pip install uv      # uv for faster package installation
   uv pip install -r requirements.txt
   ```

3. Add secrets to `.env`:
   ```env
   QDRANT_API_KEY=your_qdrant_key
   ```

4. Index the points in qdrant cluster
    ```bash
    python -m src.vector_store.index_data
    ```

5. Run the streamlit app:
    ```bash
    streamlit run app.py
    ```

6. Enter you Google API Key in the sidebar before searching.

**Example Queries:**
- "Show me white shirts under 3k"
- "Adidas running shoes for men"
- "Formal dresses in black color"

