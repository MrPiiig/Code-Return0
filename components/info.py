import pygame
import constants as CONS

pygame.font.init()


class Info:
    def __init__(self, state):
        self.state = state
        self.create_state_labels()
        self.create_info_labels()

    def create_state_labels(self):
        if self.state == 'main_scene':
            pass

    def create_info_labels(self):
        pass

    def create_label(self, label, size=40, width_scale=1.25, hight_scale=1):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass
