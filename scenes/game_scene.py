import pygame
import setup
from components import player, stuff, enemy
import constants as CONS
from components import info
import json
import os
import util


class GameScene:
    def __init__(self):
        self.load_map_data()
        self.init_scene()

    # 初始化各种场景
    # Initialisation of various scenarios
    def init_scene(self):
        self.setup_background()
        self.setup_sound()
        self.setup_grounditems()
        self.setup_player()
        self.setup_enemies()
        self.setup_checkpoint()
        self.setup_info()
        self.setup_switch()

    # 初始化场景的切换
    # Switching of initialisation scenes
    def setup_info(self):
        self.next = 'main_scene'
        self.info = info.Info('game_scene')

        self.stage = 0

    #初始化一些开关
    # Initialise some switches
    def setup_switch(self):
        self.finished = False
        self.check_can_move_screen = False
        self.bgm_switch = False
        self.win_sound_switch = False
        self.lose_sound_switch = False

    # 载入json数据
    # Loading json data
    def load_map_data(self):
        file_name = 'data.json'
        file_path = os.path.join('data', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

    # 初始化音效
    # Initialising sound effects
    def setup_sound(self):
        self.dead_sound = setup.game_sounds['Died']
        self. bg_sound = setup.bg_sounds['game_bgm']
        self.win_sound = setup.bg_sounds['win_sound']
        self.lose_sound = setup.bg_sounds['lose_sound']
        self.bg_sound.set_volume(0.3)
        self.win_sound.set_volume(0.3)
        self.lose_sound.set_volume(0.3)

    # 插入背景
    # Insert background
    def setup_background(self):
        self.image_name = self.map_data['image_name']
        self.background = setup.scene_graphics[self.image_name]
        rect = self.background.get_rect()
        # 将背景设置和游戏界面等高等宽
        # Highly widened background settings, game interface, etc.
        self.background = pygame.transform.scale(self.background, (int(rect.width * CONS.BG_MULIT),
                                                                   int(rect.height * CONS.BG_MULIT)))
        self.background_rect = self.background.get_rect()
        # 滑动游戏窗口
        # Sliding game window
        self.game_window = pygame.Rect(0, 0, CONS.SCREEN_WIDTH, CONS.SCREEN_HEIGHT)
        # 空白图层
        # Blank layer
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    # 添加地图地面（后面需要添加砖块需要的碰撞物体）
    # Add map ground (collision objects needed to add bricks later)
    def setup_grounditems(self):
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height']))
        # 设置平台
        # Setting the platform
        self.platform_items_group = pygame.sprite.Group()
        for name in ['platform']:
            for item in self.map_data[name]:
                self.platform_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height']))
                self.platform = setup.scene_graphics['platform']

    # 设置玩家
    # Setting the player
    def setup_player(self):
        self.player = player.Player()
        # 初始化玩家位置
        self.player.rect.x = self.game_window.x + 50
        self.player.rect.y = 200


    # 设置敌人
    # Setting the enemy
    def setup_enemies(self):
        self.enemy_all_dead = False
        self.enemy_group = pygame.sprite.Group()
        # 设置敌人死亡组
        # Setting up enemy death groups
        self.enemy_dead_group = pygame.sprite.Group()
        self.enemy_group_dirt = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_groupid, enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data, self.player))
                self.enemy_group_dirt[enemy_groupid] = group

    # 设置checkpoint
    # Setting up checkpoint
    def setup_checkpoint(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x, y, w, h = item['x'], item['y'], item['width'], item['height']
            checkpoint_type = item['type']
            enemy_groupid = item.get('enemy_groupid')
            self.checkpoint_group.add(stuff.Checkpoint(x, y, w, h, checkpoint_type, enemy_groupid))

    # 更新函数，所有需要实时更新的内容
    # Update function, all content that needs to be updated in real time
    def update(self, surface, keys):
        self.current_time = pygame.time.get_ticks()

        # 主角死亡时音效处理
        # Sound treatment when the main character dies
        if self.player.dead:
            self.draw_lose(surface)
            if not self.lose_sound_switch:
                self.lose_sound_switch = True
                self.bg_sound.stop()
                self.lose_sound.play()
                self.lose_timer = self.current_time
            if self.current_time - self.lose_timer > 5000:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        self.lose_sound.stop()
                        self.finished = True

        #  敌人死亡时音效处理
        # Sound processing when enemies die
        elif self.enemy_all_dead:
            if not self.win_sound_switch:
                self.win_sound_switch = True
                self.bg_sound.stop()
                self.win_sound.play()
                self.win_timer = self.current_time
            self.draw_win(surface)
            if self.current_time - self.win_timer > 5000:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        self.win_sound.stop()
                        self.finished = True

        else:
            if not self.bgm_switch:
                self.bgm_switch = True
                self.bg_sound.play()

            self.update_player_state(keys)
            self.check_enemy_number()
            # 如果把屏幕里所有的怪物全部死亡，开始窗口移动到下一个区域
            # If all the monsters in the screen die, the start window moves to the next area
            if self.check_can_move_screen:
                self.update_game_window()
            # 时刻检查死没死
            # Always check to see if you're dead
            self.check_if_go_die()
            # # 检查checkpoint
            # Check checkpoint
            self.check_checkpoints()

            for member in self.enemy_group:
                self.update_enemy_position(member)
                member.update()
            # pygame.display.update()
            self.draw(surface)

    # 检查已经死亡的敌人的数量，进行场景切换
    # Check the number of enemies that have died and make a scene switch
    def check_enemy_number(self):
        if len(self.enemy_dead_group) == 2 and self.stage == 0:
            self.check_can_move_screen = True
            self.stage = 1
        elif len(self.enemy_dead_group) == 5 and self.stage == 2:
            self.check_can_move_screen = True
            self.stage = 3
        elif len(self.enemy_dead_group) == 9:
            self.enemy_all_dead = True

    # 更新游戏窗口的移动速度
    # Update the movement speed of the game window
    def update_game_window(self):
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_vel > 0:
            if self.player.rect.centerx < third - 50:
                self.game_window.x += util.calcu_vel(self.player.x_vel, 5, 0, False)
            elif self.player.rect.centerx >= third + 50:
                self.game_window.x += util.calcu_vel(self.player.x_vel, 5, 12, True)
            else:
                self.game_window.x += self.player.x_vel

        if self.game_window.right >= 2150 and self.stage == 1:
            self.check_can_move_screen = False
            self.stage = 2
        elif self.game_window.right >= 3050 and self.stage == 3:
            self.check_can_move_screen = False
            self.stage = 4

    # 检查触发checkpoints
    # Check trigger checkpoints
    def check_checkpoints(self):
        checkpoint_player = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)

        if checkpoint_player:
            if checkpoint_player.checkpoint_type == 0:  # 释放敌人
                self.enemy_group.add(self.enemy_group_dirt[str(checkpoint_player.enemy_groupid)])
                checkpoint_player.kill()

    # 检测主角是否死亡
    # # Detecting the death of the main character
    def check_if_go_die(self):
        if self.player.hp <= 0:
            self.player.go_die()

    # 更新玩家位置 状态
    # Update Player Location Status
    def update_player_state(self, keys):
        self.player.update(keys)
        if self.player.is_attacking:
            if self.player.face_right == True:
                self.check_player_enemy_collisions(self.player.right_attack)
            elif self.player.face_right == False:
                self.check_player_enemy_collisions(self.player.left_attack)

        self.player.rect.x += self.player.x_vel
        if self.player.rect.x <= self.game_window.x:
            self.player.rect.x = self.game_window.x
        if self.player.rect.right >= self.game_window.x + CONS.SCREEN_WIDTH:
            self.player.rect.right = self.game_window.x + CONS.SCREEN_WIDTH

        # x变化后检测x方向上碰撞
        # Detecting collisions in the x-direction after a change in x
        self.check_x_collisions(self.player)

        self.player.rect.y += self.player.y_vel
        # y变化后检测y方向上碰撞
        # # Collision detection in the y-direction after a change in y
        self.check_y_collisions(self.player)

    # 更新敌人位置
    # Update enemy locations
    def update_enemy_position(self, enemy):
        enemy.rect.x += enemy.x_vel
        self.check_x_collisions(enemy)

        enemy.rect.y += enemy.y_vel
        self.check_y_collisions(enemy)

    # 检测x轴碰撞
    # Detecting x-axis collisions
    def check_x_collisions(self, being):
        ground_item = pygame.sprite.spritecollideany(being, self.ground_items_group)
        if ground_item:
            self.adjust_x(being, ground_item)

    # 检测y轴碰撞
    # Detecting y-axis collisions
    def check_y_collisions(self, being):
        ground_item = pygame.sprite.spritecollideany(being, self.ground_items_group)
        if ground_item:
            self.adjust_y(being, ground_item)
        # 检测脚底是否为空
        # Detects if the bottom of the foot is empty
        self.check_falling(being)

    # 检测玩家的攻击和敌人的碰撞
    # # Detection of player attacks and enemy collisions
    def check_player_enemy_collisions(self, being):
        attacked_enemy = pygame.sprite.spritecollide(being, self.enemy_group, False)
        if self.player.is_attacking:
            if len(attacked_enemy) > 0:
                for member in attacked_enemy:
                    if member.can_be_hit:
                        member.hp -= CONS.PLAYER_ATTACK_VALUE
                        if member.hp > 0:
                            member.state = "hit"
                            member.hit_timer = pygame.time.get_ticks()
                            member.y_vel = -3
                            if self.player.face_right:
                                member.hit_from_right = False
                            else:
                                member.hit_from_right = True
                        else:
                            member.hp = 0
                            member.go_die(self.enemy_group, self.enemy_dead_group)
                            self.dead_sound.stop()
                            self.dead_sound.play()

    # 检测到碰撞后重设x位置
    # Reset x position after collision detected
    def adjust_x(self, being, item):
        if being.rect.x < item.rect.x:
            being.rect.right = item.rect.left
        else:
            being.rect.left = item.rect.right
        being.x_vel = 0

    # 检测到碰撞后重设y位置
    # Reset y position after collision detected
    def adjust_y(self, being, item):
        if being.rect.bottom < item.rect.bottom:
            being.y_vel = 0
            being.rect.bottom = item.rect.top
            if being.can_be_hit:
                being.state = 'walk'
        else:
            being.rect.top = item.rect.bottom
            being.state = 'fall'
            being.y_vel = 7

    # 检测脚底是否有碰撞，没有就下落
    # # Detects if there is a collision on the bottom of the foot and drops if there is not
    def check_falling(self, being):
        being.rect.y += 1
        if not pygame.sprite.spritecollideany(being,
                                              self.ground_items_group) and being.state != 'jump' and being.state != 'hit':
            being.state = 'fall'
        else:
            being.rect.y -= 1

    # 画布画图
    # Canvas drawing
    def draw(self, surface):
        # 玩家跟随窗口移动
        # Players follow window movement
        self.game_ground.blit(self.background, self.game_window, self.game_window)
        self.game_ground.blit(self.player.image, (
            self.player.rect.x + CONS.PLAYER_TEXTURE_OFFSET_X, self.player.rect.y + CONS.PLAYER_TEXTURE_OFFSET_Y))
        for member in self.platform_items_group:
            self.platform = pygame.transform.scale(self.platform, (
                int(member.rect.width), int(member.rect.height)))
            self.game_ground.blit(self.platform, (member.rect.x, member.rect.y))

        for member in self.enemy_group:
            self.game_ground.blit(member.image,
                                  (member.rect.x + CONS.ENEMY_TEXTURE_OFFSET_X,
                                   member.rect.y + CONS.ENEMY_TEXTURE_OFFSET_Y))
            member.draw_hp(self.game_ground)

        self.draw_HUD(self.game_ground)

        # 人物移动更新画布
        # Character movement to update the canvas
        surface.blit(self.game_ground, (0, 0), self.game_window)

    # 绘制游戏失败的效果
    # Drawing the effects of a failed game
    def draw_lose(self, surface):
        surface.blit(setup.scene_graphics['gameover_menu'], (0, 0))
    # 绘制游戏胜利的效果
    # Drawing the effects of a win game
    def draw_win(self, surface):
        surface.blit(setup.scene_graphics['win_menu'], (0, 0))

    # 绘制head up display
    # Drawing head up display
    def draw_HUD(self, surface):
        hp = setup.player_graphics['player_hp_logo']
        player_hp_black = setup.player_graphics['player_hp_black']
        player_hp_red = setup.player_graphics['player_hp_red']
        player_hp_percent = self.player.hp / CONS.PLAYER_HP
        player_hp_red = pygame.transform.scale(player_hp_red, (
            int(player_hp_red.get_width() * player_hp_percent), player_hp_red.get_height()))
        surface.blit(hp, (self.game_window.x + 50, 45))
        surface.blit(player_hp_red, (self.game_window.x + 136, 45))
        surface.blit(player_hp_black, (self.game_window.x + 120, 45))

