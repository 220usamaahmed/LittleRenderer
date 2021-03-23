from typing import Tuple, List
from PIL import Image, ImageDraw

from obj import OBJ
from vector_utils import *


class Canvas:

    def __init__(self, dimensions: Tuple[int, int] = (512, 512)):
        self.dimensions = dimensions
        self.image = Image.new("RGB", dimensions)
        self.imageDraw = ImageDraw.Draw(self.image)
        self.far_clipping = 256
        self.z_buffer = [[-self.far_clipping] * self.dimensions[0]
            for _ in range(self.dimensions[1])]


    def point(self, v: Tuple[int, int], color: Tuple[int, int, int]):
        x = self.dimensions[0] / 2 + v[0]
        y = self.dimensions[1] / 2 - v[1]
        self.imageDraw.point((x, y), fill=color)


    def line(self, v0: Tuple[int, int], v1: Tuple[int, int],
        color: Tuple[int, int, int]
    ):
        """
        Using Bresenham's line drawing algorithm
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

    
    def filled_triangle(self, v0: Tuple[int, int], v1: Tuple[int, int],
        v2: Tuple[int, int], color: Tuple[int, int, int]
    ):
        """
        Using Line sweeping algorithm. This function is left here just for
        reference. It can not be used in a 3D context because it does not take
        the z-buffer into account when rendering triangles.
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
                    (int(v0[0] + alpha * (v2[0] - v0[0])), v0[1] + y),
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


    def get_calmped_bb(self, vs: List[Tuple[float, ...]]):
        bounding_box = get_bounding_box(vs)
        
        return (
            int(max(bounding_box[0][0], -self.dimensions[0] / 2)),
            int(max(bounding_box[1][0], -self.dimensions[1] / 2)),
            int(min(bounding_box[0][1] + 1, self.dimensions[0] / 2)),
            int(min(bounding_box[1][1] + 1, self.dimensions[1] / 2))
        )


    def apply_perspective(self, v, c):
        divisor = 1 - v[2] / c
        return (v[0] / divisor, v[1] / divisor, v[2] / divisor)


    def render_OBJ(self, obj: OBJ):
        """
        Using barycentric coordinates to determine if pixel is within the 
        triangle. A z-buffer is used to implement object oclusion.
        """
        for face in obj.get_faces():
            v0 = self.apply_perspective(face[0]['v'], 2)
            v1 = self.apply_perspective(face[1]['v'], 2)
            v2 = self.apply_perspective(face[2]['v'], 2)

            v0 = scallar_multiply(v0, 256)
            v1 = scallar_multiply(v1, 256)
            v2 = scallar_multiply(v2, 256)

            vt0 = face[0]['vt']
            vt1 = face[1]['vt']
            vt2 = face[2]['vt']

            x_start, y_start, x_end, y_end = self.get_calmped_bb([v0, v1, v2])

            v01 = get_direction_vector(v0, v1)
            v02 = get_direction_vector(v0, v2)

            vt01 = get_direction_vector(vt0, vt1)
            vt02 = get_direction_vector(vt0, vt2)

            for y in range(y_start, y_end):
                for x in range(x_start, x_end):
                    v0p = get_direction_vector((x, y), v0[:2])

                    orthogonal_vector = get_cross_product(
                        (v01[0], v02[0], v0p[0]),
                        (v01[1], v02[1], v0p[1])
                    )
                    if orthogonal_vector[2] == 0: continue

                    barycentric = scallar_multiply(orthogonal_vector,
                        1 / orthogonal_vector[2])

                    if (barycentric[0] < 0 or barycentric[1] < 0
                        or barycentric[0] + barycentric[1] > 1): continue

                    z = (v0[2] + barycentric[0] * v01[2]
                        + barycentric[1] * v02[2])
                    y_i = int(self.dimensions[1] / 2) - y - 1
                    x_i = int(self.dimensions[0] / 2) + x - 1
                    if z < self.z_buffer[y_i][x_i]: continue
                    self.z_buffer[y_i][x_i] = z

                    vtx = vt0[0] + barycentric[0] * vt01[0] + barycentric[1] * vt02[0]
                    vty = vt0[1] + barycentric[0] * vt01[1] + barycentric[1] * vt02[1]

                    self.point((x, y), obj.get_texture(vtx, vty))


    def show(self):
        self.image.show()


    def show_z_buffer(self):
        import matplotlib.pyplot as plt
        import numpy as np

        plt.imshow(np.array(self.z_buffer))
        plt.show()
