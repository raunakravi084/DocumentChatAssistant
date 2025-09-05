from pypdf import PdfReader
from docx import Document
from typing import List,Optional,Dict,Any
from . import config
import re
import os


class DataProcessor:
    """Handles processing of different file types and text extraction"""
    
    def __init__(self):
        self.supported_extensions = config.SUPPORTED_EXTENSIONS
        
        
    def read_pdf_file(self,file)-> str:
        """Extract text from pdf

        Args:
            file: pdf file

        Returns:
            text: extracted text
        """
        try:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text = text + page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF file {file}: {e}")
            return ""
    
        
    def read_text_file(self, file):
        """Read text from a .txt or .md file"""
        try:
            # Streamlit UploadedFile object
            if hasattr(file, "read"):
                return file.read().decode("utf-8")
            # Fallback for file path
            with open(file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file} : {e}")
            return ""
        
    
    def read_docx_file(self,file):
        """Extract text from a Word document"""
        try:
            doc = Document(file)
            text = ''
            for paragraph in doc.paragraphs:
                text = text + paragraph.text + '\n'
            return text
        
        except Exception as e:
            print(f"Error reading DOCX file {file} file: {e}")
            return ""
                
        
    def read_vtt_file(self, file) -> str:
        """Extract text from a VTT subtitle file"""
        try:
            text = ""
            # Handle Streamlit UploadedFile
            if hasattr(file, "read"):
                file.seek(0)  # Ensure pointer is at start
                lines = file.read().decode("utf-8").splitlines()
            else:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            
            print("VTT lines:", lines) # for debug
            # Skip WEBVTT header and empty lines
            content_lines = []
            for line in lines:
                line = line.strip()
                # Skip WEBVTT, timestamps, and empty lines
                if (line and 
                    not line.startswith('WEBVTT') and 
                    not re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}$', line) and
                    not line.isdigit()):
                    content_lines.append(line)
            
            # Join all content lines
            text = ' '.join(content_lines)
            print(f"Extracted VTT text: {text[:200]}")  # Print first 200 chars for debug
            return text
        except Exception as e:
            print(f"Error reading VTT file {file}: {e}")
            return ""
        
        
    def read_chat_recording_file(self, file) -> str:
        """Extract text from chat recording files with timestamps"""
        try:
            text = ""
            # Handle Streamlit UploadedFile
            if hasattr(file,"read"):
                lines = file.read().decode("utf-8").splitlines()
            else:
                with open(file, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            
            # Extract messages from chat format: timestamp\tSpeaker:\tMessage
            messages = []
            for line in lines:
                line = line.strip()
                if line and '\t' in line:
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        # Extract just the message content (skip timestamp and speaker)
                        message = parts[2].strip()
                        if message:
                            messages.append(message)
            
            # Join all messages
            text = ' '.join(messages)
            return text
        except Exception as e:
            print(f"Error reading chat recording file {file}: {e}")
            return ""
        
    def process_file(self, file):
        
        """Process a single file and return its content with metadata"""
        file_extension = os.path.splitext(file.name)[1].lower()
        file_name = os.path.basename(file.name)
        
        # Check if it's a supported extension or special file type
        if file_extension not in self.supported_extensions:
            #Check for special file types
            if file_extension == '.vtt':
                content = self.read_vtt_file(file)
            elif 'RecordingnewChat' in file_name or 'Recording' in file_name:
                content = self.read_chat_recording_file(file)
            else:
                return None
        
        else:
            # Extract text based on file type
            if file_extension in ['.txt', '.md']:
                content = self.read_text_file(file)
            elif file_extension == '.pdf':
                content = self.read_pdf_file(file)
            elif file_extension == '.docx':
                content = self.read_docx_file(file)
            elif file_extension == '.vtt':
                content = self.read_vtt_file(file)
            else:
                content = ""
        
        # check if content is empty
        if not content.strip():
            return None
        
        return content
            
    
