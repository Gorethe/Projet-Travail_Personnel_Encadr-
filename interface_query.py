import tkinter as tk
from tkinter import messagebox, scrolledtext
from query_data import query_rag  # Importe la fonction pour interroger

# Fonction pour exécuter la recherche
def interroger_embeddings():
    query_text = query_entry.get()
    if not query_text.strip():
        messagebox.showerror("Erreur", "Veuillez entrer une question.")
        return

    try:
        # Appeler la fonction pour exécuter la recherche
        response_text = query_rag(query_text)  # Appelle query_rag
        response_lines = response_text.split("\nSources:\n")  # Sépare réponse et sources
        response = response_lines[0] if len(response_lines) > 0 else "Aucune réponse trouvée."
        sources = response_lines[1] if len(response_lines) > 1 else "Sources non disponibles."
        
        # Afficher les résultats
        result_area.insert(tk.END, f"Question : {query_text}\n")  # Afficher la question
        result_area.insert(tk.END, f"Réponse : {response}\n")  # Afficher la réponse
        result_area.insert(tk.END, f"Sources : {sources}\n\n")  # Afficher les sources
        query_entry.delete(0, tk.END)  # Effacer la zone de saisie après la requête
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Interrogation des Embeddings")
root.geometry("700x500")  # Taille de la fenêtre

# Zone pour entrer la requête
tk.Label(root, text="Entrez votre question :").pack(pady=10)
query_entry = tk.Entry(root, width=80)
query_entry.pack(pady=10)

# Bouton pour lancer la recherche
search_button = tk.Button(root, text="Rechercher", command=interroger_embeddings)
search_button.pack(pady=10)

# Zone pour afficher les résultats
tk.Label(root, text="Résultats :").pack(pady=10)
result_area = scrolledtext.ScrolledText(root, width=80, height=20)
result_area.pack(pady=10)

# Lancement de la boucle principale
root.mainloop()
