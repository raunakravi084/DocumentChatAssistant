import streamlit as st 
from . import config

def file_uploader():
    """
    Returns a Streamlit file uploader widget that accepts one or more files.

    Parameters:
        None

    Returns:
        A Streamlit file uploader widget
    """
    return st.file_uploader("Upload a file", type=config.SUPPORTED_EXTENSIONS, 
                            accept_multiple_files=True, help="Upload one or more files to process")