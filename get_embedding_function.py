from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings

def get_embedding_function(): 
    embeddings = OllamaEmbeddings(model="llama3.1:8b")  # Spécifie le modèle à utiliser
    return embeddings



# from langchain_community.embeddings.ollama import OllamaEmbeddings
# from langchain_ollama import OllamaEmbeddings

# def get_embedding_function(): 
#     return OllamaEmbeddings(model="llama3.1:8b")  # Spécifie le modèle à utiliser

