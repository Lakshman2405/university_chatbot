# 🎓 University Chatbot

A conversational AI assistant powered by LangChain that answers university-related questions by retrieving information from PDF documents. The chatbot uses retrieval-augmented generation (RAG) to provide accurate, context-based responses without hallucination.

## Stack

- **Language:** Python 3.10
- **Framework / Runtime:** Streamlit (web UI) + LangChain (RAG orchestration)
- **Notable libraries:**
  - **LangChain Community** - Document loading, RAG pipelines, vector stores
  - **FAISS** - Vector database for semantic search
  - **Transformers** - LLM inference (FLAN-T5 base model)
  - **Sentence-Transformers** - Text embeddings (all-MiniLM-L6-v2)

## How It's Organized

```
├── app.py                  Streamlit web interface & chat UI
├── chatbot.py              RAG pipeline: document loading, embeddings, QA chain
├── utils/
│   └── prompt.py           System prompt templates for the LLM
├── data/
│   └── project-chatbot.pdf Knowledge base document(s)
├── requirements.txt        Python dependencies
├── pyproject.toml          Project metadata (Python 3.10)
└── render.yaml             Deployment config (Render platform)
```

### How It Fits Together

When you ask a question:

1. **Document Loading** (`load_documents()`): PDF files from the `data/` directory are loaded using PyPDFLoader
2. **Chunking & Indexing** (`create_vector_db()`): Text is split into 1000-token chunks with 200-token overlap and embedded using HuggingFace's `all-MiniLM-L6-v2` model into a FAISS vector database
3. **Retrieval** (`RetrievalQA`): Your query is embedded and matched against stored chunks; the top 5 most relevant documents are retrieved
4. **LLM Generation** (`create_llm()`): The FLAN-T5 base model generates an answer using only the retrieved context, with adaptive prompting for broad vs. concise questions
5. **UI Display** (`app.py`): Streamlit renders the chat interface, maintaining conversation history with a "Clear Chat" button

The system is designed to prevent hallucination by enforcing strict context-only answers.

## How to Run It

### Prerequisites
- Python 3.10
- Pip package manager

### Setup & Run Locally

```bash
# Clone the repository
git clone https://github.com/Lakshman2405/university_chatbot.git
cd university_chatbot

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The app will launch at `http://localhost:8501` by default.

### Deploy on Render

This repository includes a `render.yaml` configuration for one-click deployment:

```bash
git push  # Push to GitHub
# Then connect your repo to Render and it will auto-deploy using render.yaml
```

The service will start on port 10000 with Python 3.10.

## Adding Knowledge Base Documents

1. Place PDF files in the `data/` directory
2. Restart the app—it will automatically:
   - Load all `.pdf` files from `data/`
   - Create embeddings and rebuild the vector database
   - Use the new documents for answering queries

## Usage Tips

- **Broad questions** (10+ words): The chatbot provides detailed, multi-chunk explanations
- **Concise questions**: Shorter, focused answers from a single context window
- **Out-of-scope questions**: The chatbot responds with *"I am sorry, that information is not in my database."*
- Use the **Clear Chat** button to reset the conversation history

## Try Asking

- "What are the main topics covered in the project documentation?"
- "How do I get started with the university chatbot system?"
- "What technical stack is recommended for this project?"

---

**Created:** April 3, 2026  
**License:** None specified  
**Status:** Active
