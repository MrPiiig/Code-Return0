#main scene
import pygame


import setup
import constants as CONS

class Mainscene:
    def __init__(self):
        #设置场景
        self.setup_mainscene()
        self.setup_ui()
        #设置箭头
        self.setup_arrow()

    # def setup_ui(sheet, x, y, width, height):
    #     ui = pygame.surface((width, height))
    #     ui.blit(sheet, (0, 0), (x, y, width, height))  # 0,0位置，xywh取图
    #     return ui

    def setup_mainscene(self):
        #background picture
        self.mainscene= setup.scene_graphics['mainscene_background']


    def setup_ui(self):
        #start
        #load picture
        self.start_ui = setup.scene_graphics['mainscene_ui_start']
        #get picture size
        self.start_ui_size=self.start_ui.get_rect()
        #zoom picture size
        self.start_ui=pygame.transform.scale(self.start_ui,(int(self.start_ui_size.width * CONS.MAIN_BUTTON_RATE),int(self.start_ui_size.height * CONS.MAIN_BUTTON_RATE)))

        #setting
        self.setting_ui = setup.scene_graphics['mainscene_ui_setting']
        # get picture size
        self.setting_ui_size = self.setting_ui.get_rect()
        # zoom picture size
        self.setting_ui = pygame.transform.scale(self.setting_ui, (
        int(self.setting_ui_size.width * CONS.MAIN_BUTTON_RATE), int(self.setting_ui_size.height * CONS.MAIN_BUTTON_RATE)))


        #exit
        self.exit_ui = setup.scene_graphics['mainscene_ui_exit']
        # get picture size
        self.exit_ui_size = self.exit_ui.get_rect()
        # zoom picture size
        self.exit_ui = pygame.transform.scale(self.exit_ui, (
            int(self.exit_ui_size.width * CONS.MAIN_BUTTON_RATE), int(self.exit_ui_size.height * CONS.MAIN_BUTTON_RATE)))




    #绘制画布
    #draw surface
    def draw(self, surface):
        surface.blit(self.mainscene, (0, 0))
        surface.blit(self.start_ui, (820, 120))
        surface.blit(self.setting_ui, (820, 270))
        surface.blit(self.exit_ui, (820, 420))






    def setup_arrow(self):
        pass

    #更新画布
    def update(self, surface,key):

        self.draw(surface)
        pygame.display.update()