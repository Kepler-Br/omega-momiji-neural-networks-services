from PIL import Image


def fill_alpha_with_color(image: Image) -> Image:
    if 'A' in image.getbands():
        background = Image.new('RGBA', image.size, (255, 255, 255))

        alpha_composite = Image.alpha_composite(background, image)

        return alpha_composite
    else:
        return image
