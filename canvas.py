from typing import Tuple

from PIL import Image, ImageDraw
from vector_utils import *


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
        color: Tuple[int, int, int]
    ):
        """
        Using Bresenham's line algorithm
        """
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
        v2: Tuple[int, int], color: Tuple[int, int, int]
    ):
        self.line(v0, v1, color)
        self.line(v1, v2, color)
        self.line(v2, v0, color)

    
    def filled_triangle_1(self, v0: Tuple[int, int], v1: Tuple[int, int],
        v2: Tuple[int, int], color: Tuple[int, int, int]
    ):
        """
        Using Line sweeping algorithm
        """
        v0, v1, v2 = sorted([v0, v1, v2], key=lambda v: v[1])

        height_v0_v2 = v2[1] - v0[1]
        height_v0_v1 = v1[1] - v0[1]
        height_v1_v2 = v2[1] - v1[1]

        if height_v0_v1:
            for y in range(height_v0_v1):
                alpha = y / height_v0_v2
                beta = y / height_v0_v1

                self.line(
                    (int(v0[0] + alpha * (v2[0] - v0[0])), v0.y + y),
                    (int(v0[0] + beta * (v1[0] - v0[0])), v0[1] + y),
                    color
                )
        
        if height_v1_v2:
            for y in range(height_v1_v2 + 1):
                alpha = y / height_v0_v2
                beta = y / height_v1_v2

                self.line(
                    (int(v2[0] + alpha * (v0[0] - v2[0])), v2[1] - y),
                    (int(v2[0] + beta * (v1[0] - v2[0])), v2[1] - y),
                    color
                )


    def filled_triangle_2(self, v0: Tuple[int, int], v1: Tuple[int, int],
        v2: Tuple[int, int], color: Tuple[int, int, int]
    ):
        """
        Using barycentric coordinates to determine if pixel is within the 
        triangle
        """
        bounding_box = get_bounding_box([v0, v1, v2])
        
        v01 = get_direction_vector(v0, v1)
        v02 = get_direction_vector(v0, v2)
        
        for x in range(bounding_box[0][0], bounding_box[0][1]):
            for y in range(bounding_box[1][0], bounding_box[1][1]):
                v0p = get_direction_vector((x, y), v0)

                orthogonal_vector = get_cross_product(
                    (v01[0], v02[0], v0p[0]),
                    (v01[1], v02[1], v0p[1])
                )
                barycentric = get_scallar_multiple(orthogonal_vector,
                    1 / orthogonal_vector[2])
                
                if (barycentric[0] < 0 or barycentric[1] < 0
                    or barycentric[2] < 0): continue

                self.point((x, y), color)


    def show(self):
        self.image.show()