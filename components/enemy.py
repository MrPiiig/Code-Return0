import pygame
import setup
import util
import constants as CONS
from components import player
from scenes import game_scene


# 生成敌人实例
def create_enemy(enemy_data, player):
    enemy = Enemy(enemy_data['x'], enemy_data['y'], enemy_data['width'], enemy_data['height'], player)
    return enemy


# 敌人基类
class Enemy(pygame.sprite.Sprite):
    walk_left = 0
    walk_right = 0
    def __init__(self, x, y, w, h, player):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.load_images()
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.x = x
        self.rect.bottom = y
        self.timer = 0
        self.x_vel = -1 * CONS.ENEMY_SPEED
        self.y_vel = 0
        self.state = "walk"
        self.face_right = False
        self.current_time = pygame.time.get_ticks()
        self.player = player
        self.handle_states()
        self.walk_left = x - 200
        self.walk_right = x + 200

    def load_images(self):
        running_frames = ["Move_1", "Move_2", "Move_3", "Move_4", "Move_5"]
        attack_frames = ["Attack_1", "Attack_2", "Attack_3", "Attack_4"]

        self.right_frames = []
        self.left_frames = []
        for running_frames in running_frames:
            left_image = setup.player_graphics[running_frames]
            left_image = pygame.transform.scale(left_image, (left_image.get_width() * 0.4, left_image.get_height() * 0.4))
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
        for attack_frame in attack_frames:
            left_image = setup.player_graphics[attack_frame]
            left_image = pygame.transform.scale(left_image,
                                                (left_image.get_width() * 0.4, left_image.get_height() * 0.4))
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
        self.frames = self.left_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    # 更新函数
    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_states()


    # 状态机
    def handle_states(self):
        if self.state == 'walk':
            self.walk()
        if self.state == 'stand':
            self.stand()
        if self.state == 'fall':
            self.fall()
        elif self.state == "follow_player":
            self.follow_player()
        elif self.state == "attack":
            self.attack()

        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    # 站立
    def stand(self):
        self.x_vel = 0
        self.frame_index = 1

    # 坠落
    def fall(self):
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)

    # 敌人巡逻
    def walk(self):
        if self.current_time - self.timer > 100:
            self.frame_index += 1
            self.frame_index %= 3
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time
        if self.rect.x <= self.walk_left:
            self.face_right = True
            self.x_vel = 1 * CONS.ENEMY_SPEED
        elif self.rect.x >= self.walk_right:
            self.face_right = False
            self.x_vel = -1 * CONS.ENEMY_SPEED

    # 敌人追击
    def follow_player(self):
        if self.player.rect.x < self.rect.x:
            if self.current_time - self.timer > 100:
                self.frame_index += 1
                self.frame_index %= 3
                self.image = self.frames[self.frame_index]
                self.timer = self.current_time
            self.face_right = False
            self.x_vel = -1 * CONS.ENEMY_SPEED
            if self.rect.x - self.player.rect.x > 200:
                self.state = "walk"
            if self.rect.x - self.player.rect.x < 100:
                self.state = "attack"
        elif self.player.rect.x > self.rect.x:
            if self.current_time - self.timer > 100:
                self.frame_index += 1
                self.frame_index %= 3
                self.image = self.frames[self.frame_index]
                self.timer = self.current_time
            self.face_right = True
            self.x_vel = 1 * CONS.ENEMY_SPEED
            if self.rect.x - self.player.rect.x < -200:
                self.state = "walk"
            if self.rect.x - self.player.rect.x > -100:
                self.state = "attack"

    # 敌人攻击
    def attack(self):

        self.frame_index = 6
        if self.current_time - self.timer > 110:
            self.frame_index += 1
            self.state = "follow_player"






