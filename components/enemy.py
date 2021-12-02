import pygame
import setup
import util
import constants as CONS
from components import player
from scenes import test_scene


# 生成敌人实例
def create_enemy(enemy_data, player):
    enemy = Enemy(enemy_data['x'], enemy_data['y'], enemy_data['width'], enemy_data['height'], player)
    return enemy


# 敌人基类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, player):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.load_images()
        self.rect = self.image.get_rect()
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
        self.update_position()
        self.update()

    def load_images(self):
        running_frames = ["heroLeft1", "heroLeft2", "heroLeft3"]
        self.right_frames = []
        self.left_frames = []
        for running_frames in running_frames:
            left_image = setup.enemy_graphics[running_frames]
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
        self.frames = self.left_frames
        self.image = self.frames[self.frame_index]

    # 更新函数
    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_states()
        self.update_position()

    # 状态机
    def handle_states(self):
        if self.state == 'walk':
            self.walk()
        if self.state == 'stand':
            self.stand()
        if self.state == 'fall':
            self.fall()
        elif self.state == "move":
            self.move()
        elif self.state == "follow_player":
            self.follow_player()

        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    def update_position(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    # 行走
    def walk(self):
        if self.current_time - self.timer > 100:
            self.frame_index += 1
            self.frame_index %= 3
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time
        if self.rect.x == CONS.POSITION_LEFT:
            self.state = "move"

    # 站立
    def stand(self):
        self.x_vel = 0
        self.frame_index = 1

    # 坠落
    def fall(self):
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)

    # 敌人巡逻
    def move(self):
        if self.current_time - self.timer > 100:
            self.frame_index += 1
            self.frame_index %= 3
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time
        if self.rect.x <= CONS.POSITION_LEFT:
            self.face_right = True
            self.x_vel = 1 * CONS.ENEMY_SPEED
        elif self.rect.x >= CONS.POSITION_RIGHT:
            self.face_right = False
            self.x_vel = -1 * CONS.ENEMY_SPEED

    # 敌人追击
    def follow_player(self):
        self.state = "follow_player"
        if self.player.rect.x < self.rect.x:
            if self.current_time - self.timer > 100:
                self.frame_index += 1
                self.frame_index %= 3
                self.image = self.frames[self.frame_index]
                self.timer = self.current_time
            self.face_right = False
            self.x_vel = -1 * CONS.ENEMY_SPEED
            if self.rect.x - self.player.rect.x > 200:
                self.state = "move"
        elif self.player.rect.x > self.rect.x:
            if self.current_time - self.timer > 100:
                self.frame_index += 1
                self.frame_index %= 3
                self.image = self.frames[self.frame_index]
                self.timer = self.current_time
            self.face_right = True
            self.x_vel = 1 * CONS.ENEMY_SPEED
            if self.rect.x - self.player.rect.x < -200:
                self.state = "move"
