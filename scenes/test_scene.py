import pygame
import setup
from components import player

class TestScene:
    def __init__(self):
        self.setup_background()
        self.setup_player()
        self.setup_cursor()

    # 插入背景
    def setup_background(self):
        self.background = setup.scene_graphics['bg']

    # 设置玩家
    def setup_player(self):
        self.player = player.Player()
        # 初始化玩家位置
        self.player.rect.x = 300
        self.player.rect.y = 300

    def setup_cursor(self):
        pass

    # 更新并且在画布上画出玩家位置的变换
    def update(self, surface, keys):
        self.update_player_position()
        self.player.update(keys)
        pygame.display.update()
        self.draw(surface)

    # 玩家的状态
    def state(self, state):
        self.state = state

    # 玩家位置变换信息
    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        self.player.rect.y += self.player.y_vel

    # 画布画图
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.player.image, self.player.rect)


