import pygame
import util

from scenes import test_scene
from scenes import main_scene

def main():
    state_dict = {
        'main_scene': main_scene.Mainscene(),
        'test_screen': test_scene.TestScene()
    }
    game = util.Game(state_dict, 'main_scene')
    game.run()
# 开始程序
if __name__ == '__main__':
    main()