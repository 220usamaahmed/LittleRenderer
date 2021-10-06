import numpy as np

from src.scene import Scene
from src.obj import OBJ
from src.camera import PerspectiveCamera
from src.rasterizer import Rasterizer
from src.image_utils import show_image


def main():
    camera = PerspectiveCamera(0.2, 10, np.pi / 2)
    # camera.translate(0.5, 0.5, 0)
    scene = Scene(camera, 512)

    obj1 = OBJ('test_models/african_head/african_head.obj')
    obj1.load_texture_map('test_models/african_head/african_head_diffuse.jpg')
    obj1.load_normal_map('test_models/african_head/african_head_nm.jpg')
    obj1.load_specular_map('test_models/african_head/african_head_spec.jpg')
    obj1.translate(0, 0, -1.5)
    scene.add_obj(obj1)

    scene.render()


if __name__ == '__main__': main()