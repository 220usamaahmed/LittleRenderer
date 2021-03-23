from scene import Scene
from obj import OBJ

import random


def main():
    
    scene = Scene((512, 512))
    
    # obj1 = OBJ('./test_models/african_head/african_head.obj')
    # obj1.load_texture_map('./test_models/african_head/african_head_diffuse.jpg')
    # obj1.scale(256)
    # obj1.translate((-196, 0, 0))
    # scene.add_object(obj1)

    # obj2 = OBJ('./test_models/african_head/african_head.obj')
    # obj2.load_texture_map('./test_models/african_head/african_head_diffuse.jpg')
    # obj2.scale(256)
    # obj2.translate((196, 0, 0))
    # scene.add_object(obj2)

    diablo_3_pose = OBJ('./test_models/diablo3_pose/diablo3_pose.obj')
    diablo_3_pose.load_texture_map('./test_models/diablo3_pose/diablo3_pose_diffuse.jpg')
    diablo_3_pose.scale(256)
    scene.add_object(diablo_3_pose)

    
    scene.render()
    scene.show()
    # scene.show_z_buffer()


if __name__ == "__main__": main()