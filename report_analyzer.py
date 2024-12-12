import psycopg2  # Pour interagir avec la base de données PostgreSQL
from typing import List, Dict  # Pour les annotations de type

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

# Récupération des rapports selon un mot-clé
def get_reports_by_keyword(keyword: str) -> List[Dict]:
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, metadata->>'content' AS content
            FROM embeddings
            WHERE metadata->>'content' ILIKE %s;
        """, (f"%{keyword}%",))
        results = [
            {"id": row[0], "content": row[1]}
            for row in cursor.fetchall()
        ]
    except Exception as e:
        print(f"Erreur lors de la requête : {e}")
        results = []
    finally:
        cursor.close()
        conn.close()
    return results

# Analyse d'un rapport spécifique
def analyze_report(report_id: int) -> Dict:
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, metadata->>'content' AS content
            FROM embeddings
            WHERE id = %s;
        """, (report_id,))
        report = cursor.fetchone()
        if report:
            report_data = {
                "id": report[0],
                "content_length": len(report[1]),
                "content_preview": report[1][:100]
            }
        else:
            report_data = {}
    except Exception as e:
        print(f"Erreur lors de l'analyse du rapport : {e}")
        report_data = {}
    finally:
        cursor.close()
        conn.close()
    return report_data

# Fonction principale interactive
def main():
    print("=== Analyseur de rapports ===")
    while True:
        print("\nOptions :")
        print("1. Rechercher des rapports par mot-clé")
        print("2. Analyser un rapport par ID")
        print("3. Quitter")

        choice = input("Votre choix : ")
        if choice == "1":
            keyword = input("Entrez un mot-clé : ")
            results = get_reports_by_keyword(keyword)
            if results:
                print(f"{len(results)} rapport(s) trouvé(s) :")
                for report in results:
                    print(f"- ID: {report['id']}, Aperçu: {report['content'][:500]}...")
            else:
                print("Aucun rapport trouvé.")
        elif choice == "2":
            try:
                report_id = int(input("Entrez l'ID du rapport à analyser : "))
                analysis = analyze_report(report_id)
                if analysis:
                    print(f"Analyse du rapport {report_id} :")
                    print(f"- Longueur du contenu : {analysis['content_length']}")
                    print(f"- Aperçu : {analysis['content_preview']}")
                else:
                    print("Aucun rapport trouvé avec cet ID.")
            except ValueError:
                print("Veuillez entrer un ID valide.")
        elif choice == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
