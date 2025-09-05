# 🤖 Document ChatBot Assistant - RAG Chat Application

A clean, interactive RAG (Retrieval-Augmented Generation) chat application that lets you ask questions about your documents using AI.

## ✨ Features

- **Smart Document Processing** - Supports TXT, PDF, DOCX, MD, and VTT files
- **AI-Powered Chat** - Uses Euri API for intelligent responses
- **Vector Search** - FAISS(Facebook AI Similarity Search) for fast document retrieval
- **Auto-Loading** - One mor more Documents are loaded from Streamlit UI

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your Documents
Supported formats:
- `.txt` - Text files
- `.pdf` - PDF documents  
- `.docx` - Word documents
- `.md` - Markdown files
- `.vtt` - Video subtitle files

### 3. Run the Application
```bash
streamlit run main.py
```

### 4. Streamlit Public application link
```bash
streamlit run main.py
```

The app will automatically:
- Load all documents from the Uploaded documents icon
- Create embeddings using HuggingFace models
- Start the chat interface at `http://localhost:8501`

## 📁 Project Structure

```
DocumentChatAssistant/
├── main.py              # Main Streamlit application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── app/              # Document processing,utils
│   ├── config.py     # Configuration settings
│   ├── chat_utils    # Chat model logic
│   └── data_processor # Document processing logic
│   └── ui.py          # Streamlit file uploader logic
│   └── vectore_store_utils.py # Vector operations
└── .env               # API Key for model acess
```

## 🔧 Configuration

The application uses:
- **Euri API** for AI responses
- **FAISS** for vector storage

Configuration in `config.py`:

```python
## .env file contains:-
# Euri API
EURI_API_KEY = "euri-0d0f7d9990aaace6d3296a6970bc301f18bd04c09e3434fd8a94c024c4bab793"
```

## 💬 How to Use

1. **Start the app** - Run `streamlit run app.py`
2. **Wait for loading** - Upload your documents
3. **Start chatting** - Ask questions about your documents

### Example Questions:
- "What is machine learning?"
- "Summarize the key points from the documents"
- "Give me some practical examples"
- "Explain deep learning concepts"

## 🎯 Key Components

- **RAG System** - Combines document retrieval with AI generation
- **Vector Store** - Uses FAISS(Facebook AI Similarity Search) for semantic search
- **LLM Client** - Integrates with Euri API for responses
- **Data Processor** - Handles multiple file formats
- **Clean UI** - Streamlit-based chat interface

## 🛠️ Technical Details

- **Embeddings**: `sentence-transformers/all-mpnet-base-v2`
- **Vector DB**: FAISS(Facebook AI Similarity Search)
- **LLM**: Euri API (`gpt-4.1-nano` model)
- **UI Framework**: Streamlit with custom CSS
- **Text Chunking**: Overlapping chunks for better context

## 📝 Requirements

See `requirements.txt` for the complete list of dependencies:
- streamlit
- chromadb
- sentence-transformers
- requests
- python-dotenv
- And more...

## 🎨 UI Features

- **Responsive Design** - Works on desktop and mobile
- **Loading Indicators** - Shows when AI is thinking
- **Quick Actions** - Suggested questions to get started

---

Built with ❤️ for educational purposes using modern RAG techniques.