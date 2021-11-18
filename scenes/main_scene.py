#main scene
import pygame


import setup
import constants as CONS

class Mainscene:
    def __init__(self):
        #设置场景
        self.setup_mainscene()
        #设置箭头
        self.setup_arrow()

    def setup_mainscene(self):
        self.mainscene= setup.scene_graphics['mainscene_background']

    #绘制画布
    def draw(self, surface):
        surface.blit(self.mainscene, (0, 0))





    def setup_arrow(self):
        pass

    #更新画布
    def update(self, surface,key):

        self.draw(surface)
        pygame.display.update()