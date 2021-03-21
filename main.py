from scene import Scene
from obj import OBJ

import random


def main():
    
    scene = Scene((512, 512))
    
    obj1 = OBJ('./test_models/african_head.obj')
    obj1.scale(256)
    obj1.translate((-195, 0, 0))
    scene.add_object(obj1)

    obj2 = OBJ('./test_models/african_head.obj')
    obj2.scale(256)
    obj2.translate((195, 0, 0))
    scene.add_object(obj2)
    
    scene.render()
    scene.show()
    scene.show_z_buffer()


if __name__ == "__main__": main()