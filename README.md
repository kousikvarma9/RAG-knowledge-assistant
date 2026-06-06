####🧠💬 RAG KNOWLEDGE ASSISTANT ####

A production-style Multimodal Retrieval-Augmented Generation (RAG) system that allows users to upload documents, build a knowledge base, and ask questions grounded in their own data.
The system combines document ingestion, semantic search, vector databases, reranking, and Large Language Models to provide accurate and context-aware answers.

---

## 🚀 Features

### 📄 Document Processing
* Upload PDF, DOCX, and TXT documents
* Automatic text extraction and chunking
* Metadata management
* Knowledge base analytics

### 🖼 Multimodal Capabilities
* PDF image extraction
* Image filtering
* Image description generation
* Image-aware document understanding

### 🔍 Advanced Retrieval
* Semantic search
* Hybrid retrieval pipeline
* Reranking for improved relevance
* FAISS vector database integration

### 🤖 AI-Powered Question Answering
* Gemini 2.5 Flash integration
* Context-grounded responses
* Source-aware answers
* Hallucination reduction through RAG

### 💬 Interactive Chat Interface
* ChatGPT-style conversation UI
* Persistent chat history
* Download chat history
* Source tracking
* Retrieval debugging mode

### 📂 Knowledge Base Management
* Upload documents
* Delete documents
* Automatic knowledge base rebuild
* Processing statistics
* Document analytics dashboard

---

# 🏗 Architecture

```text
User Query
     │
     ▼
Streamlit Frontend
     │
     ▼
FastAPI Backend
     │
     ▼
Hybrid Retrieval
     │
     ├── Vector Search (FAISS)
     └── Semantic Search
     │
     ▼
Reranker
     │
     ▼
Top Relevant Chunks
     │
     ▼
Gemini 2.5 Flash
     │
     ▼
Generated Answer
```

---

# 📁 Project Structure

```text
RAG PROJECT
│
├── app
│   ├── ingestion
│   ├── loaders
│   ├── rag
│   ├── query
│   ├── vision
│   └── chat
│
├── data
│   ├── uploads
│   ├── extracted_images
│   └── vector_store
│
├── tests
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```
---
# ⚙️ Tech Stack

### Frontend
* Streamlit

### Backend
* FastAPI

### Vector Database
* FAISS

### LLM
* Google Gemini 2.5 Flash

### Embeddings
* Sentence Transformers

### Retrieval
* Hybrid Search
* Reranking

### Document Processing
* Docling
* PyMuPDF
* python-docx

### Computer Vision
* Image Extraction
* Image Analysis Pipeline

---

📊 Workflow

Document Ingestion

```text
Upload Documents
       │
       ▼
Text Extraction
       │
       ▼
Chunking
       │
       ▼
Embeddings
       │
       ▼
Vectordb Storage
```
Question Answering
```text
User Question
       │
       ▼
Query Embedding
       │
       ▼
Hybrid Retrieval
       │
       ▼
Reranking
       │
       ▼
Relevant Context
       │
       ▼
Gemini 2.5 Flash
       │
       ▼
Answer + Sources
```

---

🛠 Installation

Clone Repository

```bash
git clone https://github.com/kousikvarma9/RAG-knowledge-assistant.git

cd RAG-knowledge-assistant
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Configure Environment Variables

Create `.env`

```env
GOOGLE_API_KEY=your_api_key_here
```

Run Application

```bash
streamlit run app.py
```

---

📈 Current Capabilities

✅ PDF Processing
✅ DOCX Processing
✅ TXT Processing
✅ Image Extraction
✅ Image Analysis
✅ Hybrid Search
✅ Reranking
✅ Qdrant Integration
✅ Gemini Integration
✅ Persistent Chat History
✅ Document Deletion
✅ Processing Statistics
✅ Knowledge Base Analytics
✅ Source Attribution

---

🎯 Future Enhancements

* User Authentication
* Multi-user Knowledge Bases
* Role-based Access Control
* Cloud Deployment
* API Monitoring Dashboard
* Advanced Citation System
* Real-time Streaming Responses

---

👨‍💻 Author

KOUSIK VARMA GATTUPALLI

Artificial Intelligence & Machine Learning Student

Built as a portfolio project to demonstrate:
* Retrieval-Augmented Generation (RAG)
* LLM Integration
* Vector Databases
* Hybrid Search
* Multimodal AI Systems
* Full-Stack AI Application Development
