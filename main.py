from scene import Scene
from obj import OBJ

import random


def main():
    
    scene = Scene((640, 640))
    
    obj1 = OBJ('./test_models/african_head/african_head.obj')
    obj1.load_texture_map('./test_models/african_head/african_head_diffuse.jpg')
    scene.add_object(obj1)

    # obj2 = OBJ('./test_models/african_head/african_head.obj')
    # obj2.load_texture_map('./test_models/african_head/african_head_diffuse.jpg')
    # scene.add_object(obj2)

    # diablo_3_pose = OBJ('./test_models/diablo3_pose/diablo3_pose.obj')
    # diablo_3_pose.load_texture_map('./test_models/diablo3_pose/diablo3_pose_diffuse.jpg')
    # scene.add_object(diablo_3_pose)

    
    scene.render()
    scene.show()
    # scene.show_z_buffer()


if __name__ == "__main__": main()