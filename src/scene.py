from src.rasterizer import Rasterizer
from src.image_utils import show_image


class Scene:

    def __init__(self, camera, image_size=512):
        self.camera = camera
        self.objs = []
        self.rasterizer = Rasterizer(camera, image_size)


    def add_obj(self, obj):
        self.objs.append(obj)


    def render(self):
        for obj in self.objs:
            self.rasterizer.rasterize_obj(obj)
        show_image(self.rasterizer.image)