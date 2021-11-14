import pygame
import setup
import util
import constants as CONS

def create_enemy(enemy_data):
    enemy = Monster(enemy_data['x'], enemy_data['y'], enemy_data['width'], enemy_data['height'])
    return enemy


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.setup_state()
        self.setup_timer()



    def setup_state(self):
        self.x_vel = 0

        self.y_vel = 0

        self.frame_index = 1

        self.state = 'walk'

        self.face_right = True

    def setup_timer(self):
        self.walking_timer = 0

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_states()

    def handle_states(self):
        if self.state == 'walk':
            self.walk()
        if self.state == 'stand':
            self.stand()
        if self.state == 'fall':
            self.fall()

        self.image = self.frames[self.frame_index]

    def walk(self):
        self.x_vel = 1
        if self.current_time - self.walking_timer > 100:
            self.frame_index += 1
            self.frame_index %= 3
            self.walking_timer = self.current_time

    def stand(self):
        self.x_vel = 0
        self.frame_index = 1

    def fall(self):
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)

class Monster(Enemy):
    def __init__(self, x, y, w, h):
        Enemy.__init__(self, x, y, w, h)
        self.load_images()

    def load_images(self):
        running_frames = ['heroLeft1', 'heroLeft2', 'heroLeft3']
        self.right_frames = []
        self.left_frames = []
        for running_frame in running_frames:
            # 向左移动
            left_image = setup.enemy_graphics[running_frame]
            # 翻转并向右移动
            right_image = pygame.transform.flip(left_image, True, False)
            # 向右叠加图片
            self.right_frames.append(right_image)
            # 向左叠加
            self.left_frames.append(left_image)

        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]