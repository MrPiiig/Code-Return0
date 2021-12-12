import pygame
import constants as CONS
import util

pygame.init()
screen_size = (CONS.SCREEN_WIDTH, CONS.SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(screen_size)



# 导入所有素材
# Import all material
player_graphics = util.load_graphics('./assets/textures/player')
enemy_graphics = util.load_graphics('./assets/textures/enemy')
scene_graphics = util.load_graphics('./assets/textures/scene')
instruction_graphics = util.load_graphics('./assets/textures/scene/Control') 
bg_sounds = util.load_sounds('./assets/sounds/BGM')
game_sounds = util.load_sounds('./assets/sounds/player')
