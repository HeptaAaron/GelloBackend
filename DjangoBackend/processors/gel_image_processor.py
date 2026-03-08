from PIL import Image


def convert_to_png(image_file):
    image = Image.open(image_file)
    image = image.convert("RGB")
    return image


def convert_to_grayscale(image):
    return image.convert("L")
