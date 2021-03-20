from canvas import Canvas
from obj import OBJ
from vector_utils import *

import random


def main():
    canvas = Canvas()

    obj = OBJ('./test_models/african_head.obj')
    obj.scale(256)
    for face in obj.get_faces():
        v0 = (int(face[0][0]), int(face[0][1]), int(face[0][2]))
        v1 = (int(face[1][0]), int(face[1][1]), int(face[1][2]))
        v2 = (int(face[2][0]), int(face[2][1]), int(face[2][2]))

        v01 = get_direction_vector(v0, v1)
        v02 = get_direction_vector(v0, v2)

        face_normal = get_cross_product(v01, v02)
        face_normal = normalize(face_normal)
        orientation = get_dot_product(face_normal, (0, 0, 1))

        if orientation <= 0: continue

        canvas.filled_triangle_1(
            v0[:2], v1[:2], v2[:2],
            tuple([int(orientation * 255)] * 3)
            # random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        )
    
    canvas.show()


if __name__ == "__main__": main()