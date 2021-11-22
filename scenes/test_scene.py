import pygame
import setup
from components import player, stuff, enemy
import constants as CONS
from maps import map_testscene as map

from components import info

def create_enemy(enemy_data):
    enemy = Monster(enemy_data['x'], enemy_data['y'], enemy_data['width'], enemy_data['height'])
    return enemy


class TestScene:
    def __init__(self):
        self.start_x = 0
        self.end_x = 1200
        self.setup_background()
        self.setup_player()
        self.setup_enemies()
        self.setup_cursor()
        self.setup_stuff()
        self.finished = False

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

    # 设置物品、地形
    def setup_stuff(self):
        self.ground_items_group = pygame.sprite.Group()
        for item in map.ground:
            self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height']))

    # 设置敌人
    def setup_enemies(self):
        self.enemy_group = pygame.sprite.Group()
        for member in map.enemy:
            self.enemy_group.add(enemy.create_enemy(member))

    # 更新函数，所有需要实时更新的内容
    def update(self, surface, keys):
        self.update_player_state()
        self.player.update(keys)
        for member in self.enemy_group:
            self.update_enemy_position(member)
            member.update()
        pygame.display.update()
        self.draw(surface)


    # 更新玩家位置
    def update_player_state(self):
        if self.player.is_attacking:
            if self.player.face_right == True:
                self.check_player_enemy_collisions(self.player.right_attack)
            elif self.player.face_right == False:
                self.check_player_enemy_collisions(self.player.left_attack)
        self.player.rect.x += self.player.x_vel

        self.player.right_attack.rect.x = self.player.rect.right
        self.player.left_attack.rect.x = self.player.rect.left - self.player.rect.width
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        if self.player.rect.x > self.end_x:
            self.player.rect.x = self.end_x

        # x变化后检测x方向上碰撞
        self.check_x_collisions(self.player)

        self.player.rect.y += self.player.y_vel
        self.player.right_attack.rect.y = self.player.rect.top
        self.player.left_attack.rect.y = self.player.rect.top
        # y变化后检测y方向上碰撞
        self.check_y_collisions(self.player)



    # 更新敌人位置
    def update_enemy_position(self, enemy):
        enemy.rect.x += enemy.x_vel
        self.check_x_collisions(enemy)

        enemy.rect.y += enemy.y_vel
        self.check_y_collisions(enemy)

    # 检测x轴碰撞
    def check_x_collisions(self, being):
        ground_item = pygame.sprite.spritecollideany(being, self.ground_items_group)
        if ground_item:
            self.adjust_x(being, ground_item)

    # 检测y轴碰撞
    def check_y_collisions(self, being):
        ground_item = pygame.sprite.spritecollideany(being, self.ground_items_group)
        if ground_item:
            self.adjust_y(being, ground_item)
        # 检测脚底是否为空
        self.check_falling(being)

    # 检测玩家和敌人的碰撞
    def check_player_enemy_collisions(self, being):
        attacked_enemy = pygame.sprite.spritecollide(being, self.enemy_group, False)
        if self.player.is_attacking:
            if len(attacked_enemy) > 0:
                for member in attacked_enemy:
                    member.x_vel = 10
        self.player.is_attacking = False


    # 检测到碰撞后重设x位置
    def adjust_x(self, being, item):
        if being.rect.x < item.rect.x:
            being.rect.right = item.rect.left
        else:
            being.rect.left = item.rect.right

        being.x_vel = 0

    # 检测到碰撞后重设y位置
    def adjust_y(self, being, item):
        if being.rect.bottom < item.rect.bottom:
            being.y_vel = 0
            being.rect.bottom = item.rect.top
            being.state = 'walk'

        else:
            being.rect.top = item.rect.bottom
            being.state = 'fall'
            being.y_vel = 7

    # 检测脚底是否有碰撞，没有就下落
    def check_falling(self, being):
        being.rect.y += 1
        if not pygame.sprite.spritecollideany(being, self.ground_items_group) and being.state != 'jump':
            being.state = 'fall'
        else:
            being.rect.y -= 1

    # 画布画图
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.player.image, self.player.rect)
        surface.blit(self.player.left_attack.image, self.player.left_attack.rect)
        surface.blit(self.player.right_attack.image, self.player.right_attack.rect)
        for member in self.enemy_group:
            surface.blit(member.image, member.rect)

# class Level:
#     def __init__(self):
#         self.finished = False
#         self.next = None
#         self.info = info.Info('level')
#         self.setup_background()
#
#     def setup_background(self):
#         self.background = setup.Gra