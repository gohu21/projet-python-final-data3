import requests
import os
import requests

def telecharger_livre(url, chemin_fichier):
    """Télécharge un fichier texte depuis l'URL et le sauvegarde localement."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)

        with open(chemin_fichier, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Livre téléchargé avec succès dans : {chemin_fichier}")
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False


#télécharge image livre
url = "https://m.media-amazon.com/images/I/71DDUTDIE2L._SY425_.jpg"
chemin_fichier = "part2/images/fond.jpg"

r = requests.get(url)
with open(chemin_fichier, "wb") as f:
    f.write(r.content)

print(f"Image téléchargée : {chemin_fichier}")

if __name__ == "__main__":
    url = "https://www.gutenberg.org/cache/epub/2701/pg2701.txt"
    chemin = "part2/data/mobydick.txt"
    telecharger_livre(url, chemin)