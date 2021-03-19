from typing import Tuple

from PIL import Image, ImageDraw

class Canvas:

    def __init__(self, dimensions: Tuple[int, int] = (512, 512)):
        self.dimensions = dimensions
        self.image = Image.new("RGB", dimensions)
        self.imageDraw = ImageDraw.Draw(self.image)


    def point(self, v: Tuple[int, int], color: Tuple[int, int, int]):
        x = self.dimensions[0] / 2 + v[0]
        y = self.dimensions[1] / 2 - v[1]
        self.imageDraw.point((x, y), fill=color)


    def show(self):
        self.image.show()