from PIL import Image, ImageOps
import numpy as np


def convert_to_png(image_file):
    image = Image.open(image_file)
    image = image.convert("RGB")
    return image


def convert_to_grayscale(image):
    grayscale = image.convert("L")
    mean_brightness = np.mean(np.array(grayscale))
    if mean_brightness > 128:
        return ImageOps.invert(grayscale)
    return grayscale