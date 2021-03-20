from scene import Scene
from obj import OBJ

import random


def main():
    
    scene = Scene((800, 800))
    
    obj = OBJ('./test_models/african_head.obj')
    scene.add_object(obj)
    
    scene.render()
    scene.show()
    # scene.show_z_buffer()


if __name__ == "__main__": main()