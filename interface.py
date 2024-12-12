from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
from processus_traitement import load_documents, split_documents, add_to_postgresql , move_processed_documents  # Importez vos fonctions ici

# Fonction pour charger les documents
def charger_documents():
    folder = filedialog.askdirectory()  # Demande à l'utilisateur de sélectionner un dossier
    if folder:
        load_documents()  # Appelez votre fonction pour charger les documents
        messagebox.showinfo("Succès", f"Documents chargés depuis : {folder}")

# Fonction pour diviser les documents en chunks
def diviser_chunks():
    documents = load_documents()  # Charger les documents d'abord
    chunks = split_documents(documents)  # Diviser les documents en chunks
    messagebox.showinfo("Succès", f"{len(chunks)} documents divisés en chunks.")

# Fonction pour envoyer les chunks vers la base de données
def envoyer_vers_base():
    documents = load_documents()  # Charger les documents d'abord
    chunks = split_documents(documents)  # Diviser en chunks
    add_to_postgresql(chunks)  # Passer les chunks à la fonction pour insérer dans la base
    move_processed_documents() 
    messagebox.showinfo("Succès", "Chunks insérés dans la base de données.")


# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion des Documents")
root.geometry("500x350")  # Taille de la fenêtre
root.configure(bg="#000000")  # Couleur de fond

# Style moderne
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 14), background="#f5f5f5", foreground="#333")

# Titre
title_label = ttk.Label(root, text="Gestion des Documents", anchor="center")
title_label.pack(pady=20)

# Ajout des boutons à l'interface avec ttk
btn_charger = ttk.Button(root, text="Charger des Documents", command=charger_documents)
btn_charger.pack(pady=10, fill="x")

btn_diviser = ttk.Button(root, text="Diviser en Chunks", command=diviser_chunks)
btn_diviser.pack(pady=10, fill="x")

btn_envoyer = ttk.Button(root, text="Envoyer vers la Base", command=envoyer_vers_base)
btn_envoyer.pack(pady=10, fill="x")

# Bouton pour quitter
btn_quitter = ttk.Button(root, text="Quitter", command=root.quit)
btn_quitter.pack(pady=20, side="bottom")

# Lancement de la boucle principale Tkinter
root.mainloop()



# # Ajout des boutons à l'interface
# tk.Button(root, text="Charger des documents", command=charger_documents).pack(pady=10)
# tk.Button(root, text="Diviser en chunks", command=diviser_chunks).pack(pady=10)
# tk.Button(root, text="Envoyer vers la base", command=envoyer_vers_base).pack(pady=10)

# # Lancement de la boucle principale Tkinter
# root.mainloop()
