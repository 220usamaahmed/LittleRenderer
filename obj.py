"""
This is a very curde and incomprehensive parser of .obj files. It does not check 
the validity of the file being parsed.
"""

from PIL import Image


class OBJ:

    def __init__(self, filepath):
        self.filepath = filepath
        self.vertices = []
        self.texture_coordinates = []
        self.faces = []

        self.read_file()
        self.texture_map = None
        self.texture_map_size = None


    def load_texture_map(self, filepath):
        image = Image.open(filepath)
        self.texture_map = image.load()
        self.texture_map_size = image.size


    def read_file(self):
        with open(self.filepath, 'r') as file:
            for line in file:
                data = line.split()
                if not len(data): continue
                if data[0] == 'v':
                    self.vertices.append(list(map(float, data[1:4])))
                if data[0] == 'vt':
                    self.texture_coordinates.append(
                        tuple(map(float, data[1:4]))
                    )
                if data[0] == 'f':
                    self.faces.append(
                        [tuple(map(lambda x: int(x) - 1, d.split('/'))) 
                            for d in data[1:4]]
                    )


    def get_faces(self):
        for face in self.faces:
            yield [{
                'v': self.vertices[f[0]],
                'vt': self.texture_coordinates[f[1]] } 
                for f in face]


    def get_texture(self, x, y):
        if self.texture_map == None:
            raise Exception("Texture map not loaded for object")
        
        x = int(x * self.texture_map_size[0])
        y = int(y * self.texture_map_size[1])

        if (0 <= x < self.texture_map_size[0] 
            and 0 <= y < self.texture_map_size[1]):
            return self.texture_map[x, y]
        else: raise Exception("Texture coordinates out of range.")


    def scale(self, scale_factor):
        for i in range(len(self.vertices)):
            self.vertices[i][0] *= scale_factor
            self.vertices[i][1] *= scale_factor
            self.vertices[i][2] *= scale_factor


    def translate(self, translation):
        for i in range(len(self.vertices)):
            self.vertices[i][0] += translation[0]
            self.vertices[i][1] += translation[1]
            self.vertices[i][2] += translation[2]
