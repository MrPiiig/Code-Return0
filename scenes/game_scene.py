import pygame
import setup
from components import player, stuff, enemy
import constants as CONS
from components.enemy import Enemy
from maps import map_testscene as map
from components import info



class GameScene:
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
        self.background = setup.scene_graphics['Background_1.1']
        rect = self.background.get_rect()
        # 将背景设置和游戏界面等高等宽
        self.background = pygame.transform.scale(self.background, (int(rect.width * CONS.BG_MULIT),
                                                                   int(rect.height * CONS.BG_MULIT)))
        self.background_rect = self.background.get_rect()
        # 滑动游戏窗口
        self.game_window = setup.SCREEN.get_rect()
        # 空白图层
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    # 设置玩家
    def setup_player(self):
        self.player = player.Player()
        # 初始化玩家位置
        self.player.rect.x = 300
        self.player.rect.y = 200

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
            self.enemy_group.add(enemy.create_enemy(member, self.player))

    # 更新函数，所有需要实时更新的内容
    def update(self, surface, keys):
        self.update_player_state()
        self.player.update(keys)
        # 更新跟随窗口
        self.update_game_window()

        for member in self.enemy_group:
            self.update_enemy_position(member)
            member.update()
        pygame.display.update()
        self.draw(surface)

    def update_game_window(self):
        forth = self.game_window.x + self.game_window.width / 4
        if self.player.x_vel > 0 and self.player.rect.centerx > forth:
            self.game_window.x += self.player.x_vel

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
                    if member.can_be_hit:
                        member.state = "hit"
                        member.hp -= CONS.PLAYER_ATTACK_VALUE
                        if member.hp > 0:
                            member.hit_timer = pygame.time.get_ticks()
                            if self.player.face_right:
                                member.hit_from_right = False
                            else:
                                member.hit_from_right = True
                        else:
                            self.enemy_group.remove(member)


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
        # 玩家跟随窗口移动
        self.game_ground.blit(self.background, self.game_window, self.game_window)
        # 人物移动更新画布
        surface.blit(self.background, (0, 0), self.game_window)
        pygame.draw.rect(surface, 'red', self.player.rect)
        pygame.draw.rect(surface, 'blue', self.player.right_attack)
        pygame.draw.rect(surface, 'blue', self.player.left_attack)

        surface.blit(self.player.image, (self.player.rect.x + CONS.PLAYER_TEXTURE_OFFSET_X, self.player.rect.y + CONS.PLAYER_TEXTURE_OFFSET_Y))

        for member in self.enemy_group:
            pygame.draw.rect(surface, 'red', member.rect)
            surface.blit(member.image, (member.rect.x + CONS.ENEMY_TEXTURE_OFFSET_X, member.rect.y + CONS.ENEMY_TEXTURE_OFFSET_Y))
            member.draw_hp(surface)

        self.draw_HUD(surface)

    # 绘制head up display
    def draw_HUD(self, surface):
        hp = setup.player_graphics['player_hp_logo']
        player_hp_black = setup.player_graphics['player_hp_black']
        player_hp_red = setup.player_graphics['player_hp_red']
        player_hp_percent = self.player.hp / CONS.PLAYER_HP
        player_hp_red = pygame.transform.scale(player_hp_red, (player_hp_red.get_width() * player_hp_percent, player_hp_red.get_height()))
        surface.blit(hp, (50, 80))
        surface.blit(player_hp_red, (136, 80))
        surface.blit(player_hp_black, (120, 80))

