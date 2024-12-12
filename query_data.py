import argparse
import psycopg2
from langchain.prompts import ChatPromptTemplate
from get_embedding_function import get_embedding_function
from langchain_ollama import OllamaLLM

# Connexion à la base de données PostgreSQL
def connect_to_db():
    try:
        return psycopg2.connect(
            dbname="Mind",
            user="christine",
            password="1234567890",
            host="localhost",
            port="5433" 
        )
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Fonction de recherche de similarité
def query_postgres(query_text, embedding_function, k=5):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Obtenir l'embedding de la question
    query_embedding = embedding_function.embed_query(query_text)
    
    # Recherche de similarité dans PostgreSQL
    try:
        cursor.execute("""
            SELECT id, metadata, vector <->%s::vector AS distance
            FROM embeddings
            ORDER BY distance ASC
            LIMIT %s;
        """, (query_embedding, k))  # Corrected line
        
        results = cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
        results = []
    finally:
        cursor.close()
        conn.close()

    # Formatage des résultats
    return [(result[0], result[1], result[2]) for result in results]

# Construction de la requête RAG
def query_rag(query_text: str):
    embedding_function = get_embedding_function()
    results = query_postgres(query_text, embedding_function)

    # Créer le contexte à partir des résultats
    context_text = "\n\n---\n\n".join([result[1].get("content", "") for result in results])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # LLM Ollama
    model = OllamaLLM(model="llama3.1:8b")
    response_text = model.invoke(prompt)

    sources = [result[0] for result in results]
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    formatted_response = f"Response:\n{response_text}\n\nSources:\n" + "\n".join(map(str, sources))
    print(formatted_response)
    return response_text

# Point d'entrée du script
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

if __name__ == "__main__":
    main()
