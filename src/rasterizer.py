import numpy as np
from tqdm import tqdm


class Rasterizer:

    def __init__(self, camera, image_size=512):
        self.image_size = image_size
        self.camera = camera
        self.image = np.zeros((image_size, image_size, 3), dtype='uint8')
        self.depth_buffer = (np.ones((image_size, image_size, 1))
            * (-camera.f * self.image_size / 2)
        )


    def euclidean_to_homogeneous(self, vertex_coordinates):
        return np.concatenate(
            (vertex_coordinates, np.ones((vertex_coordinates.shape[0], 1))), 1
        )

    def homogeneous_to_euclidean(self, vertex_coordinates):
        w = vertex_coordinates[:, 3].reshape((-1, 1))
        vertex_coordinates = vertex_coordinates[:, :3]
        return vertex_coordinates / w


    def apply_camera_transform(self, vertex_coordinates):
        return vertex_coordinates.dot(
            self.camera.get_camera_transform()
        )


    def apply_viewing_transform(self, vertex_coordinates):
        return vertex_coordinates.dot(
            self.camera.get_viewing_transform()
        )


    def scale_vertex_coordinates(self, vertex_coordinates):
        return vertex_coordinates * self.image_size / 2


    def get_bounding_box(self, vs):
        bounding_box = []
        for c in range(len(vs[0])):
            bounding_box.append((
                vs[vs.index(min(vs, key=lambda x: x[c]))][c],
                vs[vs.index(max(vs, key=lambda x: x[c]))][c]
            ))
        return (
            int(bounding_box[0][0]),
            int(bounding_box[1][0]),
            int(bounding_box[0][1]) + 1,
            int(bounding_box[1][1]) + 1
        )


    def get_preped_vertex_coordinates(self, vertex_coordinates):
        vertex_coordinates = self.euclidean_to_homogeneous(vertex_coordinates)
        vertex_coordinates = self.apply_camera_transform(vertex_coordinates)
        vertex_coordinates = self.apply_viewing_transform(vertex_coordinates)
        vertex_coordinates = self.homogeneous_to_euclidean(vertex_coordinates)
        vertex_coordinates = self.scale_vertex_coordinates(vertex_coordinates)
        return vertex_coordinates


    def get_barycentric_coordinates(self, v01, v02, pv0):
        orthogonal_vector = np.cross(
            [v01[0], v02[0], pv0[0]],
            [v01[1], v02[1], pv0[1]]
        )

        # What causes orthogonal vector to have a third component of 0?
        if orthogonal_vector[2] == 0: return None

        return orthogonal_vector / orthogonal_vector[2]


    def extract_vertex_values(self, f, v, vt, vn):
        return (
            v[f[0][0]], v[f[1][0]], v[f[2][0]],
            vt[f[0][1]], vt[f[1][1]], vt[f[2][1]],
            vn[f[0][2]], vn[f[1][2]], vn[f[2][2]]
        )


    def rasterize_obj(self, obj):
        vertex_coordinates = obj.get_vertex_coordinates()
        v = self.get_preped_vertex_coordinates(vertex_coordinates.copy())
        vt = obj.get_vertex_texture_coordinates()
        vn = obj.get_vertex_normals()

        for f in tqdm(obj.get_faces()):
        # for f in obj.get_faces():
            v0, v1, v2, vt0, vt1, vt2, _, _, _ = self.extract_vertex_values(f, v, vt, vn)

            v01 = v1 - v0
            v02 = v2 - v0

            vt01 = vt1 - vt0
            vt02 = vt2 - vt0

            x_start, y_start, x_end, y_end = self.get_bounding_box([
                list(v0), list(v1), list(v2)
            ])

            for y in range(y_start, y_end):
                for x in range(x_start, x_end):
                    y_i = int(self.image_size / 2) - y
                    x_i = int(self.image_size / 2) + x

                    # If point is outside the image
                    if not (0 <= x_i < self.image_size
                        and 0 <= y_i < self.image_size): continue

                    pv0 = v0 - np.array([x, y, 0])
                    if (b_c := self.get_barycentric_coordinates(v01, v02, pv0)) is None: continue

                    # If point is outside the triangle
                    if (b_c[0] < 0 or b_c[1] < 0
                        or b_c[0] + b_c[1] > 1):
                        continue

                    z = (v0[2] + b_c[0] * v01[2]
                        + b_c[1] * v02[2])
                    # If point is occluded
                    if z < self.depth_buffer[y_i, x_i]: continue
                    self.depth_buffer[y_i, x_i] = z

                    # Calculating color
                    vtx = int(vt0[0] + b_c[0] * vt01[0] + b_c[1] * vt02[0])
                    vty = int(vt0[1] + b_c[0] * vt01[1] + b_c[1] * vt02[1])

                    base_color = obj.get_texture_color(vtx, vty)
                    normal = obj.get_normal(vtx, vty)
                    specular = obj.get_specular_values(vtx, vty)

                    p = np.array([x, y, z])
                    
                    to_camera = -p
                    to_camera = to_camera / np.linalg.norm(to_camera)
                    
                    to_light = np.array([0, -100, 0]) - p
                    to_light = to_light / np.linalg.norm(to_light)

                    h = (to_camera + to_light) / 2
                    h = h / np.linalg.norm(h)

                    color = base_color * (np.dot(normal, to_light)) + 255 * specular * np.power(np.dot(normal, h), 8)
                    color = np.clip(color, a_min=0, a_max=255)

                    self.image[y_i, x_i] = color


    def show_z_buffer(self):
        import matplotlib.pyplot as plt
    
        plt.imshow(self.depth_buffer)
        plt.show()
