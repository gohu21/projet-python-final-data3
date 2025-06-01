import re

def lire_texte(chemin_fichier):
    """Lit le contenu texte de mobydick.txt"""
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        return f.read()

def extraire_infos(texte):
    """Extrait le titre et l’auteur du livre à partir des données du txt"""
    lignes = texte.splitlines()
    titre = auteur = None

    for ligne in lignes:
        if "Title:" in ligne:
            titre = ligne.replace("Title:", "").strip()
        elif "Author:" in ligne:
            auteur = ligne.replace("Author:", "").strip()
        if titre and auteur:
            break

    return titre, auteur

def extraire_chapitre_1(texte):

    match_start = re.search(r"\*\*\* START OF(.*?)\*\*\*", texte, re.IGNORECASE)
    debut = match_start.end() if match_start else 0
    texte_pur = texte[debut:].strip()

    chapter1_positions = [m.start() for m in re.finditer(r"CHAPTER 1\. Loomings\.", texte_pur)]
    chapter2_positions = [m.start() for m in re.finditer(r"CHAPTER 2\. The Carpet-Bag\.", texte_pur)]

    if not chapter1_positions or not chapter2_positions:
        print("chapitres non trouvés")
        return ""

    max_distance = -1
    best_chap1_pos = None
    best_chap2_pos = None
    for chap1_pos in chapter1_positions:
        next_chap2 = next((pos for pos in chapter2_positions if pos > chap1_pos), None)
        if next_chap2:
            distance = next_chap2 - chap1_pos
            if distance > max_distance:
                max_distance = distance
                best_chap1_pos = chap1_pos
                best_chap2_pos = next_chap2

    if best_chap1_pos is not None and best_chap2_pos is not None:
        chapitre_1 = texte_pur[best_chap1_pos:best_chap2_pos].strip()
        return chapitre_1
    else:
        print("chapitre non trouvé")
        return ""

if __name__ == "__main__":
    chemin = "part2/data/mobydick.txt"
    texte = lire_texte(chemin)
    titre, auteur = extraire_infos(texte)
    chapitre_1 = extraire_chapitre_1(texte)

    print("Titre :", titre)
    print("Auteur :", auteur)
    print("\nDébut du chapitre 1 :\n", chapitre_1[:1000], "...")