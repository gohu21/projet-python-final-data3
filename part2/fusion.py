from PIL import Image

def coller_logo_sur_image(image_fond_path, logo_path, sortie_path, angle=180):

    fond = Image.open(image_fond_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.rotate(angle, expand=True)
    logo = logo.resize((80, 80))

    position = (fond.width - logo.width - 0, 0)

    fond.paste(logo, position, mask=logo)
    fond.convert("RGB").save(sortie_path)


if __name__ == "__main__":
    coller_logo_sur_image(
        image_fond_path="part2/output/fond_crop.jpg",
        logo_path="part2/images/logo.jpg",
        sortie_path="part2/output/image_avec_logo.jpg",
        angle=180
    )
