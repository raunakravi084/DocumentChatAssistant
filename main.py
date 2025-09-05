import streamlit as st 
from app.ui import file_uploader
from app.chat_utils import get_chat_model, ask_chat_model
from app.data_processor import DataProcessor
from app.vector_store_utils import create_faiss_index, retrieve_faiss_index
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
import os,time


load_dotenv()
EURI_API_KEY = os.getenv('EURI_API_KEY')

# Creting instance of DataProcessor
data_processor = DataProcessor()

st.set_page_config(
    page_title="💬 MediChat Pro - Medical Document Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.assistant {
        background-color: #f0f2f6;
        color: black;
    }
    .chat-message .avatar {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .chat-message .message {
        flex: 1;
    }
    .chat-message .timestamp {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    .stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff3333;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_model" not in st.session_state:
    st.session_state.chat_model = None
    
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #0DBDBF; font-size: 3rem; margin-bottom: 0.5rem;">🏥 MediChat Pro</h1>
    <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Your Intelligent Document Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for document upload
with st.sidebar:
    st.markdown("<span style='color: #0DBDBF'><h2>📁 Document Upload</h2></span>", unsafe_allow_html=True)
    st.markdown("Upload your documents to start chatting!")
    st.markdown("**Supported formats:** .txt, .pdf, .docx, .md, .vtt")
    
    uploaded_files = file_uploader()
    
    if uploaded_files:
        st.success(f"📄 {len(uploaded_files)} document(s) uploaded")
        
        # Process document
        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing your medical documents..."):
                
                # Extract text from all PDFs
                all_texts =[]
                for file in uploaded_files:
                    if file is not None:
                        text = data_processor.process_file(file)
                        if text is not None:
                            all_texts.append(text)
                    
                # Split text into chunks
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
                
                chunks = []
                for text in all_texts:
                    chunks.extend(text_splitter.split_text(text))
            
                print("Original Text:", text)    
                print("Chunks:", chunks)  # Print out the chunks list
                
                if not chunks:
                    print("Error: Chunks list is empty")
                    st.error("❌ No text could be extracted from your documents. Please check your files and try again.")
                else:
                    # create FAISS index
                    vectorstore = create_faiss_index(chunks)
                    st.session_state.vectorstore = vectorstore
                    
                    # Initialize chat model
                    chat_model = get_chat_model(api_key=EURI_API_KEY)
                    st.session_state.chat_model = chat_model
                    
                    st.success("✅ Documents processed successfully!")
                    st.balloons()
                
# Main chat interface
st.markdown("### 💬 Chat with Your Medical Documents")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Chat input
if prompt := st.chat_input("Ask about your medical documents..."):
    # Add user message to chat history
    timestamp = time.strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt, 
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)
        
    # Generate response
    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching documents..."):
                
                # Retrieve relevant documents
                relevant_docs = retrieve_faiss_index(st.session_state.vectorstore,prompt)
                
                # Create context from relevant documents
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
                
                
                # Create prompt with context
                system_prompt = f"""You are MediChat Pro, an intelligent medical document assistant. 
                Based on the following medical documents, provide accurate and helpful answers. 
                If the information is not in the documents, clearly state that.
                when you are giving an answer make sure that try to take help from llm and give me a full diagnosis of the problem.

                Medical Documents:
                {context}

                User Question: {prompt}

                Answer:"""
                
                response = ask_chat_model(st.session_state.chat_model,system_prompt)
                
            st.markdown(response)
            st.caption(timestamp)
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response, 
                "timestamp": timestamp
            })
    else:
        with st.chat_message("assistant"):
            st.error("⚠️ Please upload and process documents first!")
            st.caption(timestamp)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🤖 Powered by AI & RAG | 🗎 🏥 Medical Document Intelligence | Built with ❤️ and crafted by Raunak Ravi.</p>
</div>
""", unsafe_allow_html=True)    
                
                    
    