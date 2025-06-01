from download import telecharger_livre
from analyse import lire_texte, extraire_chapitre_1, extraire_infos
from graphique import generer_graphique, analyser_paragraphes
from image import rogner_image_entete, coller_logo_sur_image
from rapport import generer_rapport

# 1 Télécharge
telecharger_livre(
    url="https://www.gutenberg.org/cache/epub/2701/pg2701.txt",
    chemin_fichier="part2/data/mobydick.txt"
)

# 2 Lire texte et extraire
texte = lire_texte("part2/data/mobydick.txt")
chapitre = extraire_chapitre_1(texte)
titre, auteur = extraire_infos(texte)
paragraphe = chapitre.split("\n")[1].strip()

# 3  Graphe
distribution = analyser_paragraphes(chapitre)
generer_graphique(distribution, "part2/output/graph.png")

# 4 Image + logo
rogner_image_entete("part2/images/fond.jpg", "part2/output/fond_crop.jpg")
coller_logo_sur_image("part2/output/fond_crop.jpg", "part2/images/logo.jpg", "part2/output/image_avec_logo.jpg", angle=180)

# 5 Rapport
generer_rapport()
