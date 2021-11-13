import pygame
import util

from scenes import test_scene

def main():
    game = util.Game()
    stage1 = test_scene.TestScene()
    game.run(stage1)

# 开始程序
if __name__ == '__main__':
    main()