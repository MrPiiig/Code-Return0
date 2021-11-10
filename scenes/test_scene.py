import pygame
import setup
from components import player

class TestScene:
    def __init__(self):
        self.setup_background()
        self.setup_player()
        self.setup_cursor()

    def setup_background(self):
        self.background = setup.scene_graphics['bg']

    def setup_player(self):
        self.player = player.Player()
        self.player.rect.x = 300
        self.player.rect.y = 300


    def setup_cursor(self):
        pass

    def update(self, surface, keys):
        self.update_player_position()
        self.player.update(keys)
        pygame.display.update()
        self.draw(surface)


    def update_player_position(self):
        self.player.rect.x += self.player.vel

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.player.image, self.player.rect)
