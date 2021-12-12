# main scene
import pygame
import setup
import constants as CONS
from components import info,player
import util


class Mainscene:
    def __init__(self):
        self.init_scene()


    # 重置游戏关卡
    # # Reset game levels
    def init_scene(self):
        # 设置场景
        # Setting the scene
        self.setup_mainscene()
        self.setup_ui()
        # 设置箭头
        # Set arrow
        self.setup_arrow()
        self.setup_bgm()
        self.info = info.Info('main_scene')
        self.finished = False
        self.can_press = True
        self.in_menu = True
        self.next = 'game_scene'

    # 设定背景音效
    # Setting the background sound
    def setup_bgm(self):
        self.bg_sound = setup.bg_sounds['menu_bgm']
        self.bg_sound.set_volume(0.3)
        self.bg_sound.play(-1)
    def setup_mainscene(self):
        # background picture
        self.mainscene = setup.scene_graphics['mainscene_background']

    def setup_ui(self):
        # start
        # load picture
        self.start_ui = setup.scene_graphics['mainscene_ui_start']
        # get picture size
        self.start_ui_size = self.start_ui.get_rect()
        # zoom picture size
        self.start_ui = pygame.transform.scale(self.start_ui, (
            int(self.start_ui_size.width * CONS.MAIN_BUTTON_RATE),
            int(self.start_ui_size.height * CONS.MAIN_BUTTON_RATE)))

        # setting
        self.setting_ui = setup.scene_graphics['mainscene_ui_howtoplay']
        # get picture size
        self.setting_ui_size = self.setting_ui.get_rect()
        # zoom picture size
        self.setting_ui = pygame.transform.scale(self.setting_ui, (
            int(self.setting_ui_size.width * CONS.MAIN_BUTTON_RATE),
            int(self.setting_ui_size.height * CONS.MAIN_BUTTON_RATE)))

        # exit
        self.exit_ui = setup.scene_graphics['mainscene_ui_exit']
        # get picture size
        self.exit_ui_size = self.exit_ui.get_rect()
        # zoom picture size
        self.exit_ui = pygame.transform.scale(self.exit_ui, (
            int(self.exit_ui_size.width * CONS.MAIN_BUTTON_RATE),
            int(self.exit_ui_size.height * CONS.MAIN_BUTTON_RATE)))

        # instruction_bg
        self.instruction_bg = setup.instruction_graphics['howto playscene_background_1']

        #how to play ui
        self.howtoplay_attack = setup.instruction_graphics['settingscene_ui_attack']
        self.howtoplay_move = setup.instruction_graphics['settingscene_ui_move']
        self.howtoplay_jump = setup.instruction_graphics['settingscene_ui_jump']

        self.howtoplay_key = setup.instruction_graphics['settingscene_ui_keybord']

        # get origional picture and transform size
    def setup_arrow(self):
        self.select_arrow_org = setup.scene_graphics['mainscene_arrow']
        self.select_arrow_org_size = self.select_arrow_org.get_rect()
        self.select_arrow_org = pygame.transform.scale(self.select_arrow_org, (
            int(self.select_arrow_org_size.width * CONS.MAIN_BUTTON_RATE),
            int(self.select_arrow_org_size.height * CONS.MAIN_BUTTON_RATE)))

        # select it to sprite
        self.select_arrow = pygame.sprite.Sprite()
        self.select_arrow_image = self.select_arrow_org

        rect = self.select_arrow_image.get_rect()

        # location
        rect.x, rect.y = (650, 100)
        self.select_arrow.rect = rect
        self.select_arrow.state = 0

    # 绘制menu画布
    # draw surface
    def draw_menu(self, surface):
        surface.blit(self.mainscene, (0, 0))
        surface.blit(self.start_ui, (820, 120))
        surface.blit(self.setting_ui, (820, 270))
        surface.blit(self.exit_ui, (820, 420))
        surface.blit(util.creat_info('Use "A" and "D" keys to move the cursor  "Enter" key to confirm', size=35),
                     (200, 660))
        surface.blit(self.select_arrow_image, self.select_arrow.rect)

    # 绘制instruction
    # Drawinstruction
    def draw_instruction(self, surface):
        surface.blit(self.instruction_bg, (0, 0))

        surface.blit(self.howtoplay_attack, (280, 200))
        surface.blit(self.howtoplay_jump, (360, 330))
        surface.blit(self.howtoplay_move, (350, 460))

        #for attack
        surface.blit(self.howtoplay_key, (650, 200))
        surface.blit(util.creat_info('J', size=70), (675, 195))

        #for jump
        surface.blit(self.howtoplay_key, (650, 330))
        surface.blit(util.creat_info('K', size=70), (675, 325))

        #for move
        surface.blit(self.howtoplay_key, (650, 460))
        surface.blit(util.creat_info('A', size=70), (670, 455))

        surface.blit(self.howtoplay_key, (800, 460))
        surface.blit(util.creat_info('D', size=70), (820, 455))





      # load picture
        self.start_ui = setup.scene_graphics['mainscene_ui_start']
        # get picture size
        self.start_ui_size = self.start_ui.get_rect()
        # zoom picture size
        self.start_ui = pygame.transform.scale(self.start_ui, (
            int(self.start_ui_size.width * CONS.MAIN_BUTTON_RATE),
            int(self.start_ui_size.height * CONS.MAIN_BUTTON_RATE)))





    def judge_press(self, keys):
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.can_press = True

    # 状态机
    # Status machines
    # Selecting functions on the main screen according to key movements
    def update_arrow(self, keys):
        self.judge_press(keys)
        if self.select_arrow.state == 0:
            self.select_arrow.rect.y = 120
        elif self.select_arrow.state == 1:
            self.select_arrow.rect.y = 270
        else:
            self.select_arrow.rect.y = 420
        if self.in_menu:
            if keys[pygame.K_a] and self.can_press:
                self.can_press = False
                if self.select_arrow.state > 0:
                    self.select_arrow.state -= 1


            elif keys[pygame.K_d] and self.can_press:
                self.can_press = False
                if self.select_arrow.state < 2:
                    self.select_arrow.state += 1

            elif keys[pygame.K_RETURN]:
                if self.select_arrow.state == 0:
                    self.finished = True
                    self.bg_sound.stop()
                elif self.select_arrow.state == 1:
                    self.in_menu = False
                else:
                    pygame.display.quit()
        elif keys[pygame.K_ESCAPE] and not self.in_menu:
            self.in_menu = True


    # 更新画布
    # Update the canvas
    def update(self, surface, keys):
        self.update_arrow(keys)
        if self.in_menu:
            self.draw_menu(surface)
        else:
            self.draw_instruction(surface)

