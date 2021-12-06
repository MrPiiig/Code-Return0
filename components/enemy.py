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
    def __init__(self, x, y, w, h, target):
        pygame.sprite.Sprite.__init__(self)
        self.setup_state()
        self.setup_timer()
        self.setup_velocities(x, y)
        self.setup_box(x, y, w, h)
        self.setup_attack()
        self.load_images()
        self.target = target


    # 初始化碰撞盒子
    def setup_box(self, x, y, w, h):
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.x = x
        self.rect.bottom = y

    # 初始化各类状态判断
    def setup_state(self):
        self.state = "walk"
        self.face_right = False
        self.hit_from_right = True
        self.can_be_hit = True
        self.frame_index = 0
        self.type = 'enemy'
        self.hp = CONS.ENEMY_HP

    # 初始化各类计时器
    def setup_timer(self):
        self.timer = 0
        # 受击计时器，计算受击时间
        self.hit_timer = 0
        # 获取当前时间
        self.current_time = pygame.time.get_ticks()

    # 初始化速度相关属性
    def setup_velocities(self, x, y):
        self.x_vel = -1 * CONS.ENEMY_SPEED
        self.y_vel = 0
        self.walk_left = x - 200
        self.walk_right = x + 200


    # 初始化攻击范围
    def setup_attack(self):
        pass
        self.right_attack = player.Attack(self.rect.right, self.rect.top, CONS.PLAYER_ATTACK_WIDTH, CONS.PLAYER_ATTACK_HEIGHT)
        self.left_attack = player.Attack(self.rect.left - CONS.PLAYER_TEXTURE_OFFSET_X, self.rect.top,
                                  CONS.PLAYER_ATTACK_WIDTH, CONS.PLAYER_ATTACK_HEIGHT)
    # 绘制血条
    def draw_hp(self, surface):
        hp_percent = self.hp / CONS.ENEMY_HP
        hp_black = setup.enemy_graphics['enemy_hp_black']
        hp_red = setup.enemy_graphics['enemy_hp_red']
        hp_red = pygame.transform.scale(hp_red, (int(hp_red.get_width() * hp_percent), int(hp_red.get_height())))
        surface.blit(hp_red, (self.rect.x + 18, self.rect.y - 20))
        surface.blit(hp_black, (self.rect.x + 8, self.rect.y - 20))

    def load_images(self):
        self.right_frames = []
        self.left_frames = []
        running_frames = ["Move_1", "Move_2", "Move_3", "Move_4", "Move_5"]
        attack_frames = ["Attack_1", "Attack_2", "Attack_3", "Attack_4"]

        for running_frames in running_frames:
            left_image = setup.player_graphics[running_frames]
            left_image = pygame.transform.scale(left_image, (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
        for attack_frame in attack_frames:
            left_image = setup.player_graphics[attack_frame]
            left_image = pygame.transform.scale(left_image,
                                                (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)

        left_hit_image = setup.player_graphics['Hit_1']  # 9
        left_hit_image = pygame.transform.scale(left_hit_image, (
            int(left_hit_image.get_width() * 0.4), int(left_hit_image.get_height() * 0.4)))
        right_hit_image = pygame.transform.flip(left_hit_image, True, False)
        self.right_frames.append(right_hit_image)
        self.left_frames.append(left_hit_image)

        self.frames = self.left_frames
        self.image = self.frames[self.frame_index]

    # 更新函数
    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.update_attack_position()
        self.handle_states()


    def update_attack_position(self):
        self.right_attack.rect.x = self.rect.right
        self.left_attack.rect.x = self.rect.left - self.rect.width
        self.right_attack.rect.y = self.rect.top
        self.left_attack.rect.y = self.rect.top

    # 状态机
    def handle_states(self):
        if self.state == 'walk':
            self.walk()
        elif self.state == 'stand':
            self.stand()
        elif self.state == 'hit':
            self.hit()
        elif self.state == 'fall':
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
        if abs(self.target.rect.x - self.rect.x) < 300:
            self.state = "follow_player"
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
        if self.target.rect.x < self.rect.x:
            if self.current_time - self.timer > 100:
                self.frame_index += 1
                self.frame_index %= 3
                self.image = self.frames[self.frame_index]
                self.timer = self.current_time
            self.face_right = False
            self.x_vel = -1 * CONS.ENEMY_SPEED
            if self.rect.x - self.target.rect.x > 300:
                self.state = "walk"
            if 100 < self.rect.x - self.target.rect.x < 150:
                self.state = "attack"
        elif self.target.rect.x > self.rect.x:
            if self.current_time - self.timer > 100:
                self.frame_index += 1
                self.frame_index %= 3
                self.image = self.frames[self.frame_index]
                self.timer = self.current_time
            self.face_right = True
            self.x_vel = 1 * CONS.ENEMY_SPEED
            if self.rect.x - self.target.rect.x < -300:
                self.state = "walk"
            if -100 > self.rect.x - self.target.rect.x > -150:
                self.state = "attack"

    # 敌人攻击
    def attack(self):
        self.x_vel = 0
        self.frame_index = 5
        if self.current_time - self.timer < 300:
            self.check_attack_player_collisions()
        if self.current_time - self.timer > 150:
            self.frame_index = 6
        if self.current_time - self.timer > 200:
            self.frame_index = 7
        if self.current_time - self.timer > 250:
            self.frame_index = 8
        if self.current_time - self.timer > 300:
            self.frame_index = 5
        if self.current_time - self.timer > 2000:
            self.state = 'follow_player'


    # 检测攻击与玩家碰撞
    def check_attack_player_collisions(self):
        if self.face_right:
            if pygame.sprite.collide_rect(self.right_attack, self.target) and self.target.can_be_hit:
                self.target.state = 'hit'
                self.target.x_vel = 3
                self.target.y_vel = -2
                self.target.hp -= CONS.ENEMY_ATTACK_VALUE
                if self.target.hp < 0:
                    self.target.hp =0
                self.target.hit_timer = self.current_time
                self.target.face_right = False

        else:
            if pygame.sprite.collide_rect(self.left_attack, self.target) and self.target.can_be_hit:
                self.target.state = 'hit'
                self.target.x_vel = -3
                self.target.y_vel = -2
                self.target.hp -= CONS.ENEMY_ATTACK_VALUE
                if self.target.hp < 0:
                    self.target.hp =0
                self.target.hit_timer = self.current_time
                self.target.face_right = True

    # 收到攻击
    def hit(self):
        self.frame_index = 9
        self.can_be_hit = False
        if self.hp <= 0:
            self.hp = 0
        if self.hit_from_right:
            self.x_vel = -2
        else:
            self.x_vel = 2
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)
        if self.current_time - self.hit_timer > 200:
            self.x_vel = 0
        if self.current_time - self.hit_timer > 1000:
            self.can_be_hit = True

            self.state = "follow_player"





