import pygame
import constants as CONS
import util
pygame.init()
screen_size = (CONS.SCRENN_WIDTH, CONS.SCRENN_HEIGHT)
pygame.display.set_mode(screen_size)

# 导入所有素材
player_graphics = util.load_graphics('./assets/textures/player')
enemy_graphics = util.load_graphics('./assets/textures/enemy')
scene_graphics = util.load_graphics('./assets/textures/scene')
