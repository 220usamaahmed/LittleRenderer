from canvas import Canvas
from vector_utils import *

from typing import Tuple


class Scene:

    def __init__(self, dimensions: Tuple[int, int] = (512, 512)):
        self.dimensions = dimensions
        self.far_clipping = 1024
        self.canvas = Canvas(self.dimensions)
        self.z_buffer = [[-self.far_clipping] * self.dimensions[0]
            for _ in range(self.dimensions[1])]
        self.objects = []


    def add_object(self, new_object):
        new_object.scale(400) # TODO Fix this scene scalling thing
        self.objects.append(new_object)


    def render(self):
        for obj in self.objects:
            for face in obj.get_faces():
                v0 = (int(face[0][0]), int(face[0][1]), int(face[0][2]))
                v1 = (int(face[1][0]), int(face[1][1]), int(face[1][2]))
                v2 = (int(face[2][0]), int(face[2][1]), int(face[2][2]))

                v01 = get_direction_vector(v0, v1)
                v02 = get_direction_vector(v0, v2)

                face_normal = get_cross_product(v01, v02)
                face_normal = normalize(face_normal)
                orientation = get_dot_product(face_normal, (0, 0, 1))

                self.canvas.filled_triangle_2(
                    v0, v1, v2, self.z_buffer,
                    tuple([int(orientation * 255)] * 3)
                )


    def show(self):
        self.canvas.show()


    def show_z_buffer(self):
        import matplotlib.pyplot as plt
        import numpy as np

        plt.imshow(np.array(self.z_buffer))
        plt.show()