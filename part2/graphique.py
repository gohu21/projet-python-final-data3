import matplotlib.pyplot as plt
import os
from collections import Counter
import math
from analyse import lire_texte, extraire_chapitre_1
import re


def analyser_paragraphes(chapitre_texte):
    raw_paragraphes = re.split(r'\n', chapitre_texte)  # Split on single newlines
    paragraphes = []
    for p in raw_paragraphes:
        p = p.replace('\n', ' ').strip()
        if len(p.split()) >= 5:
            paragraphes.append(p)
    
    # Debug: Print paragraph count and word counts
    print(f"Nombre de paragraphes trouvés : {len(paragraphes)}")
    for i, p in enumerate(paragraphes[:5]):  # Limit to first 5 for brevity
        nb_mots = len(p.split())
        print(f"Paragraphe {i+1} : {nb_mots} mots (arrondi à {int(math.floor(nb_mots / 10.0) * 10)})")
    
    longueurs_arrondies = []
    for p in paragraphes:
        nb_mots = len(p.split())
        arrondi = int(round(nb_mots / 5.0) * 5)  # Round to nearest 5 instead of 10
        if arrondi == 0:
            continue
        longueurs_arrondies.append(arrondi)
    
    distribution = dict(sorted(Counter(longueurs_arrondies).items()))
    print("Valeurs arrondies utilisées :", distribution)
    return distribution



def generer_graphique(distribution, chemin_fichier):
    """Crée et enregistre un graphique"""
    os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)

    x = list(distribution.keys())
    y = list(distribution.values())

    plt.figure(figsize=(10, 6))
    plt.bar(x, y, width=0.8)
    plt.title("Distribution des longueurs des paragraphes (Chapitre 1)")
    plt.xlabel("Nombre de mots (arrondi à la dizaine)")
    plt.ylabel("Nombre de paragraphes")
    plt.grid(axis='y')

    plt.tight_layout()
    plt.savefig(chemin_fichier)
    plt.close()


if __name__ == "__main__":
    
    texte = lire_texte("part2/data/mobydick.txt")
    chapitre = extraire_chapitre_1(texte)
    print("\nAperçu du chapitre 1 :\n", chapitre[:500])
    distribution = analyser_paragraphes(chapitre)
    generer_graphique(distribution, "part2/output/graph.png")