import numpy as np

from src.image_utils import load_image


class OBJ:

    def __init__(self, filepath):
        self.load_file(filepath)
        self.texture_map = None
        self.normal_map = None
        self.specular_map = None


    def load_file(self, filepath):
        vertex_coordinates = []
        vertex_texture_coordinates = []
        vertex_normals = []
        faces = []

        with open(filepath, 'r') as obj_file:
            for line in obj_file:
                data = line.split()
                if not len(data): continue
                key = data[0]
                values = data[1:]
                if key == 'v':
                    vertex_coordinates.append(list(map(float, values)))
                elif key == 'vt':
                    vertex_texture_coordinates.append(list(map(float, values[:2])))
                elif key == 'vn':
                    vertex_normals.append(list(map(float, values)))
                elif key == 'f':
                    faces.append([
                        list(map(lambda x: int(x) - 1, value.split('/')))
                        for value in values
                    ])
        
        self.vertex_coordinates = np.array(vertex_coordinates)
        self.vertex_texture_coordinates = np.array(vertex_texture_coordinates)
        self.vertex_normals = np.array(vertex_normals)
        self.faces = np.array(faces)


    # TODO Calling these load function again to update map would cause incorrect
    # scallling of the coordinates
    def load_texture_map(self, filepath):
        self.texture_map = load_image(filepath)
        self.vertex_texture_coordinates *= self.texture_map.shape[:2]


    def load_normal_map(self, filepath):
        normal_map = load_image(filepath)
        if normal_map.shape[:2] != self.texture_map.shape[:2]:
            raise Exception('Size of texture and normal map must be the same')
        self.normal_map = normal_map


    def load_specular_map(self, filepath):
        specular_map = load_image(filepath)
        if specular_map.shape[:2] != self.texture_map.shape[:2]:
            raise Exception('Size of texture and specular map must be the same')
        self.specular_map = specular_map


    def get_vertex_coordinates(self):
        return self.vertex_coordinates


    def get_vertex_texture_coordinates(self):
        return self.vertex_texture_coordinates


    def get_vertex_normals(self):
        return self.vertex_normals


    def get_texture_color(self, x, y):
        if self.texture_map is None:
            raise Exception('Texture map not loaded for object')

        if (0 <= x < self.texture_map.shape[0] 
            and 0 <= y < self.texture_map.shape[1]):
            return self.texture_map[y, x]
        else: raise Exception('Texture coordinates out of range.')


    def get_normal(self, x, y):
        if self.normal_map is None:
            raise Exception('Normal map not loaded for object.')

        if (0 <= x < self.texture_map.shape[0] 
            and 0 <= y < self.texture_map.shape[1]):
            return self.normal_map[y, x] / 255
        else: raise Exception('Normal coordinates out of range.')


    def get_specular_values(self, x, y):
        if self.specular_map is None:
            raise Exception('Speuclar map not loaded for object.')

        if (0 <= x < self.texture_map.shape[0] 
            and 0 <= y < self.texture_map.shape[1]):
            return self.specular_map[y, x] / 255
        else: raise Exception('Specular coordinates out of range.')


    def get_faces(self):
        for face in self.faces:
            yield face


    def translate(self, x, y, z):
        self.vertex_coordinates += [x, y, z]