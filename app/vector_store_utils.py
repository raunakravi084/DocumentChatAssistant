from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List

def create_faiss_index(texts: List[str]):
    """Create FAISS index from a list of texts using HuggingFaceEmbeddings

    Args:
        texts (List[str]): list of text strings

    Returns:
        FAISS: FAISS index
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return FAISS.from_texts(texts,embeddings)


def retrieve_faiss_index(vector_store:FAISS,query:str,k:int=4):
    """ Retrieve k nearest neighbors from vector store using FAISS

    Args:
        vector_store (FAISS): FAISS vector store
        query (str): query string
        k (int): number of nearest neighbors to return, default is 4

    Returns:
        List[Tuple[float, str]]: list of tuples containing similarity score and text
    """
    return vector_store.similarity_search(query,k=k)