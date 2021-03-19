from canvas import Canvas
from obj import OBJ
from vector_utils import *


def main():
    canvas = Canvas()

    obj = OBJ('./test_models/african_head.obj')
    for face in obj.get_faces():
        v0 = (int(face[0][0] * 256), int(face[0][1] * 256), int(face[0][2] * 256))
        v1 = (int(face[1][0] * 256), int(face[1][1] * 256), int(face[1][2] * 256))
        v2 = (int(face[2][0] * 256), int(face[2][1] * 256), int(face[2][2] * 256))

        v01 = get_direction_vector(v0, v1)
        v02 = get_direction_vector(v0, v2)

        face_normal = get_cross_product(v01, v02)
        face_normal = normalize(face_normal)
        face_normal_dot = get_dot_product(face_normal, (0, 0.5, 1))

        if face_normal_dot <= 0: continue

        canvas.filled_triangle_2(
            v0[:2], v1[:2], v2[:2],
            tuple([int(face_normal_dot * 255)] * 3)
        )
    
    canvas.show()


if __name__ == "__main__": main()