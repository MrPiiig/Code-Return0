import pygame
import setup
from components import player, stuff
import constants as CONS
from maps import  map_testscene as map

class TestScene:
    def __init__(self):
        self.start_x = 0
        self.end_x = 1200
        self.setup_background()
        self.setup_player()
        self.setup_cursor()
        self.setup_stuff()


    # 插入背景
    def setup_background(self):
        self.background = setup.scene_graphics['bg']

    # 设置玩家
    def setup_player(self):
        self.player = player.Player()
        # 初始化玩家位置
        self.player.rect.x = 300
        self.player.rect.y = 400

    def setup_cursor(self):
        pass

    def setup_stuff(self):
        self.ground_items_group = pygame.sprite.Group()
        for item in map.ground:
            self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item["height"]))


    # 更新并且在画布上画出玩家位置的变换
    def update(self, surface, keys):
        self.update_player_position()
        self.player.update(keys)
        pygame.display.update()
        self.draw(surface)



    # 玩家位置变换信息
    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        if self.player.rect.x > self.end_x:
            self.player.rect.x = self.end_x
        # x变化后检测x方向上碰撞
        self.check_x_collisions()

        self.player.rect.y += self.player.y_vel
        # y变化后检测y方向上碰撞
        self.check_y_collisions()
    # 检测x轴碰撞
    def check_x_collisions(self):
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        if ground_item:
            self.adjust_player_x(ground_item)
    # 检测y轴碰撞
    def check_y_collisions(self):
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        if ground_item:
            self.adjust_player_y(ground_item)
        # 检测脚底是否为空
        self.check_falling(self.player)

    # 检测到碰撞后重设x位置
    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right

        self.player.x_vel = 0
    # 检测到碰撞后重设y位置
    def adjust_player_y(self,sprite):
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'

        else:
            self.player.rect.top = sprite.rect.bottom
            self.player.state = 'fall'
            self.player.y_vel = 7
    # 检测脚底是否有碰撞，没有就下落
    def check_falling(self, sprite):
        self.player.rect.y += 1
        if not pygame.sprite.spritecollideany(sprite, self.ground_items_group) and sprite.state != 'jump':
            sprite.state = 'fall'
        else:
            self.player.rect.y -= 1

    # 画布画图
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.player.image, self.player.rect)


