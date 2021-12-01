import pygame
import constants as CONS
import util
pygame.init()
screen_size = pygame.display.set_mode((CONS.SCREEN_WIDTH, CONS.SCREEN_HEIGHT))


# 导入所有素材
player_graphics = util.load_graphics('./assets/textures/player')
enemy_graphics = util.load_graphics('./assets/textures/enemy')
scene_graphics = util.load_graphics('./assets/textures/scene')