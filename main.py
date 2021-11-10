import pygame
import util

from scenes import test_scene

def main():
    game = util.Game()
    state = test_scene.TestScene()
    game.run(state)

if __name__ == '__main__':
    main()