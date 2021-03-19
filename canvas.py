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


    def line(self, v0: Tuple[int, int], v1: Tuple[int, int],
        color: Tuple[int, int, int]):
        steep = False

        if abs(v0[0] - v1[0]) < abs(v0[1] - v1[1]):
            steep = True
            v0 = (v0[1], v0[0])
            v1 = (v1[1], v1[0])

        if v0[0] > v1[0]:
            v0, v1 = v1, v0

        dx = v1[0] - v0[0]
        dy = v1[1] - v0[1]
        error = 0
        d_error = abs(dy) * 2
        y = v0[1]

        for x in range(v0[0], v1[0]):
            if steep: self.point([y, x], color)
            else: self.point([x, y], color)
            error += d_error
            if error > dx:
                y += 1 if v1[1] > v0[1] else -1
                error -= dx * 2


    def triangle(self, v0: Tuple[int, int], v1: Tuple[int, int],
        v2: Tuple[int, int], color: Tuple[int, int, int]):
        self.line(v0, v1, color)
        self.line(v1, v2, color)
        self.line(v2, v0, color)


    def show(self):
        self.image.show()