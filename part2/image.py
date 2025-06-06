from PIL import Image


def rogner_image_entete(chemin_source, chemin_sortie, hauteur_crop=130):
    """Rogne l'image"""
    image = Image.open(chemin_source)
    largeur, hauteur = image.size

    zone = (0, hauteur_crop, largeur, hauteur)
    image_cropped = image.crop(zone)

    image_cropped.save(chemin_sortie)

def coller_logo_sur_image(image_fond_path, logo_path, sortie_path, angle=180):

    fond = Image.open(image_fond_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.rotate(angle, expand=True)
    logo = logo.resize((80, 80))

    position = (fond.width - logo.width - 0, 0)

    fond.paste(logo, position, mask=logo)
    fond.convert("RGB").save(sortie_path)

# Test direct
if __name__ == "__main__":
    rogner_image_entete(
        chemin_source="part2/images/fond.jpg",
        chemin_sortie="part2/output/fond_crop.jpg",
        hauteur_crop=130
    )
