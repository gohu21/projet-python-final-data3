from PIL import Image


def rogner_image_entete(chemin_source, chemin_sortie, hauteur_crop=130):
    """Rogne l'image"""
    image = Image.open(chemin_source)
    largeur, hauteur = image.size

    zone = (0, hauteur_crop, largeur, hauteur)
    image_cropped = image.crop(zone)

    image_cropped.save(chemin_sortie)


# Test direct
if __name__ == "__main__":
    rogner_image_entete(
        chemin_source="part2/images/fond.jpg",
        chemin_sortie="part2/output/fond_crop.jpg",
        hauteur_crop=130
    )
