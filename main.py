import pygame
import util

from scenes import test_scene
from scenes import main_scene

def main():
    game = util.Game()
    stage1 = test_scene.TestScene()

    stage0 = main_scene.Mainscene()

    game.run(stage0)

# 开始程序
if __name__ == '__main__':
    main()