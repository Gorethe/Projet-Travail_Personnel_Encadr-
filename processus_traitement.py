try:
    from langchain_community.document_loaders import PyPDFDirectoryLoader
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema.document import Document
    from get_embedding_function import get_embedding_function
    import psycopg2  # Pour interagir avec PostgreSQL
    import shutil  # Pour déplacer les fichiers
    import os
    print("Imports successful")
except ImportError as e:
    print(f"Import failed: {e}")

import argparse
import json

# Configuration de la base de données PostgreSQL
DB_HOST = "127.0.0.1"
DB_PORT = "5433"
DB_NAME = "Mind"
DB_USER = "christine"
DB_PASS = "1234567890"

DATA_PATH = "data"
PROCESSED_PATH = "processed_data"  # Dossier pour stocker les fichiers traités

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Charger et traiter les documents
    documents = load_documents()
    print(f"Nombre de documents chargés: {len(documents)}")

    chunks = split_documents(documents)
    print(f"Nombre de chunks générés: {len(chunks)}")

    add_to_postgresql(chunks)
    move_processed_documents()  # Déplacer les fichiers traités

def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    
    for i, chunk in enumerate(chunks):
        chunk.metadata['id'] = i
        chunk.metadata['content'] = chunk.page_content  # Ajout du contenu dans les métadonnées
    return chunks

def add_to_postgresql(chunks: list[Document]):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        embedding_function = get_embedding_function()

        cursor.execute("SELECT metadata->>'id' FROM embeddings")
        existing_ids = {str(row[0]) for row in cursor.fetchall()}

        for chunk in chunks:
            document_id = str(chunk.metadata.get("id"))
            if document_id in existing_ids:
                print(f"⚠️ Document avec l'ID {document_id} déjà dans la base.")
                continue
            
            vector = embedding_function.embed_documents([chunk.page_content])[0]
            # Nettoyer les chaînes de caractères avant insertion
            # Nettoyer toutes les séquences d'échappement Unicode non valides
            clean_metadata = json.dumps(chunk.metadata).encode('utf-8', 'ignore').decode('utf-8')
            cursor.execute(
                "INSERT INTO embeddings (metadata,vector) VALUES (%s, %s::vector)",(clean_metadata, vector)
                # (json.dumps(chunk.metadata),vector)
            )
            conn.commit()
            print(f"✅ Document ajouté avec l'ID: {document_id}")
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'insertion : {e}")
    finally:
        cursor.close()
        conn.close()

def move_processed_documents():
    if not os.path.exists(PROCESSED_PATH):
        os.makedirs(PROCESSED_PATH)
    
    for filename in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, filename)
        if os.path.isfile(file_path):
            shutil.move(file_path, os.path.join(PROCESSED_PATH, filename))
            print(f"📁 Fichier déplacé : {filename}")

def clear_database():
    pass

if __name__ == "__main__":
    main()
