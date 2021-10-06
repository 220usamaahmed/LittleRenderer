import numpy as np


class PerspectiveCamera:

    def __init__(self, n, f, a):
        self.n = n
        self.f = f
        self.a = a
        self.position = { 'x': 0, 'y': 0, 'z': 0 }


    def get_camera_transform(self):
        return -np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [self.position['x'], self.position['y'], self.position['z'], 1]
        ])


    def get_viewing_transform(self):
        return np.array([
            [1 / np.tan(self.a / 2), 0, 0, 0],
            [0, 1 / np.tan(self.a / 2), 0, 0],
            [0, 0, (self.f + self.n) / (self.f - self.n), -1],
            [0, 0, 2 * self.f * self.n / (self.f - self.n), 0],
        ])


    def translate(self, x, y, z):
        self.position['x'] += x
        self.position['y'] += y
        self.position['z'] += z