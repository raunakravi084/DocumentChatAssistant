from euriai.langchain import create_chat_model

def get_chat_model(api_key:str):
    """
    Return a chat model using the given api_key.

    Args:
        api_key (str): API key from euriai

    Returns:
        chat_model: the chat model
    """
    return create_chat_model(api_key=api_key,
                             model= "gpt-4.1-nano",
                             temperature=0.7)
    
def ask_chat_model(chat_model,query):
    """
    Ask the chat model a question.

    Args:
        chat_model: the chat model
        query (str): the question to ask the model

    Returns:
        str: the response from the model
    """
    response = chat_model.invoke(query)
    return response.content