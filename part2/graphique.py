import matplotlib.pyplot as plt
import os
from collections import Counter
import math
from analyse import lire_texte, extraire_chapitre_1



def analyser_paragraphes(chapitre_texte):
    """Analyse le chapitre : compte les mots par paragraphe (arrondis à la dizaine)."""
    paragraphes = [p.strip() for p in chapitre_texte.split('\n\n') if p.strip()]
    longueurs_arrondies = []

    for paragraphe in paragraphes:
        mots = paragraphe.split()
        nb_mots = len(mots)

        if nb_mots < 1:
            continue  # Ignore les paragraphes vides

        arrondi = int(math.floor(nb_mots / 10.0) * 10)
        longueurs_arrondies.append(arrondi)



    distribution = Counter(longueurs_arrondies)
    distribution = dict(sorted(distribution.items()))
    return distribution


def generer_graphique(distribution, chemin_fichier):
    """Crée et enregistre un graphique de distribution."""
    os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)

    x = list(distribution.keys())
    y = list(distribution.values())

    plt.figure(figsize=(10, 6))
    plt.bar(x, y, width=8)
    plt.title("Distribution des longueurs des paragraphes (Chapitre 1)")
    plt.xlabel("Nombre de mots (arrondi à la dizaine)")
    plt.ylabel("Nombre de paragraphes")
    plt.grid(axis='y')

    plt.tight_layout()
    plt.savefig(chemin_fichier)
    plt.close()




# Test direct
if __name__ == "__main__":
    
    texte = lire_texte("part2/data/mobydick.txt")
    chapitre = extraire_chapitre_1(texte)
    print("\nAperçu du chapitre 1 :\n", chapitre[:500])
    distribution = analyser_paragraphes(chapitre)
    generer_graphique(distribution, "part2/output/graph.png")