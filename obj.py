class OBJ:

    def __init__(self, filepath):
        self.filepath = filepath
        self.vertices = []
        self.faces = []

        self.read_file()


    def read_file(self):
        # TODO Check if file is valid
        with open(self.filepath, 'r') as file:
            for line in file:
                data = line.split()
                if not len(data): continue
                if data[0] == 'v':
                    self.vertices.append(list(map(float, data[1:4])))
                if data[0] == 'f':
                    self.faces.append([int(d.split('/')[0]) - 1 for d in data[1:4]])


    def get_faces(self):
        for face in self.faces:
            yield (
                self.vertices[face[0]],
                self.vertices[face[1]],
                self.vertices[face[2]]
            )