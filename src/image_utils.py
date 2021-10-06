import numpy as np
from PIL import Image 


def load_image(filepath):
    image = Image.open(filepath)
    return np.asarray(image)


def save_image(image_array, filepath):
    Image.fromarray(image_array).save(filepath)


def show_image(image_array):
    Image.fromarray(image_array).show()
