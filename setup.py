import pygame
import constants as CONS
import util
pygame.init()
screen_size = (CONS.SCRENN_WIDTH, CONS.SCRENN_HEIGHT)
pygame.display.set_mode(screen_size)

player_graphics = util.load_graphics('./assets/textures/player')
scene_graphics = util.load_graphics('./assets/textures/scene')