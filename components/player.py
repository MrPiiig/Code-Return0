"""
角色的所有行为
"""
import setup
import pygame
# 导入常量数据
import constants as CONS
import util


class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, w, h)


# 定义玩家类
class Player(pygame.sprite.Sprite):
    # 类方法， method
    def __init__(self):
        self.hp = CONS.PLAYER_HP
        pygame.sprite.Sprite.__init__(self)
        self.setup_state()
        self.setup_timers()
        self.setup_velocities()
        self.load_images()
        self.setup_attack()
        self.type = "player"

    def setup_attack(self):
        self.right_attack = Attack(self.rect.right, self.rect.top, CONS.PLAYER_ATTACK_WIDTH, CONS.PLAYER_ATTACK_HEIGHT)
        self.left_attack = Attack(self.rect.left - CONS.PLAYER_TEXTURE_OFFSET_X, self.rect.top, CONS.PLAYER_ATTACK_WIDTH, CONS.PLAYER_ATTACK_HEIGHT)

    # 主角状态
    def setup_state(self):
        # 初始化状态为 "站立"
        self.state = 'stand'
        # 脸朝向为右
        self.face_right = True
        # 初始帧
        self.frame_index = 1
        # 攻击状态判断
        self.is_attacking = False
        # 能否跳跃判断
        self.can_jump = True
        # 能否攻击判断
        self.can_attack = True

    # 各种计时器，以后buff时间，道具使用倒计时
    def setup_timers(self):
        self.walking_timer = 0
        self.jumping_timer = 0
        self.attacking_time = 0

    # 速度数值
    def setup_velocities(self):
        self.x_vel = 0
        self.y_vel = 0
        self.max_walk_vel = CONS.MAX_WALK_SPEED
        self.max_run_vel = CONS.MAX_RUN_SPEED
        self.max_y_vel = CONS.MAX_Y_SPEED
        self.walk_accel = CONS.WALK_ACCEL
        self.turn_accel = CONS.TRUN_ACCEL
        self.run_accel = CONS.RUN_ACCEL
        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel


    # 帧造型，方便表示出运动的变化
    def load_images(self):
        running_frames = ['Move_1', 'Move_2', 'Move_3', 'Move_4', 'Move_5'] # 1~5
        jumping_frames = ['Jump_1', 'Jump_2', 'Jump_3'] # 6, 7, 8
        attacking_frams = ['Attack_1', 'Attack_2', 'Attack_3', 'Attack_4'] # 9~12
        left_stand_image = setup.player_graphics['Stand_1'] # 0
        left_stand_image = pygame.transform.scale(left_stand_image, (left_stand_image.get_width() * 0.4, left_stand_image.get_height() * 0.4))
        right_stand_image = pygame.transform.flip(left_stand_image, True, False)
        self.right_frames = []
        self.left_frames = []
        self.right_frames.append(right_stand_image)
        self.left_frames.append(left_stand_image)
        for running_frame in running_frames:
            # 向左移动
            left_image = setup.player_graphics[running_frame]
            left_image = pygame.transform.scale(left_image, (left_image.get_width() * 0.4, left_image.get_height() * 0.4))
            # 翻转并向右移动
            right_image = pygame.transform.flip(left_image, True, False)
            # 向右叠加图片
            self.right_frames.append(right_image)
            # 向左叠加
            self.left_frames.append(left_image)

        for jumping_frame in jumping_frames:
            # 向左跳跃
            left_image = setup.player_graphics[jumping_frame]
            left_image = pygame.transform.scale(left_image,
                                                (left_image.get_width() * 0.4, left_image.get_height() * 0.4))
            # 向右跳跃
            right_image = pygame.transform.flip(left_image, True, False)
            # 添加图片
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)

        for attacking_frame in attacking_frams:
            # 向左跳跃
            left_image = setup.player_graphics[attacking_frame]
            left_image = pygame.transform.scale(left_image,
                                                (left_image.get_width() * 0.4, left_image.get_height() * 0.4))
            # 向右跳跃
            right_image = pygame.transform.flip(left_image, True, False)
            # 添加图片
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)


        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = pygame.Rect(0, 0, CONS.PLAYER_RECT_WIDTH, CONS.PLAYER_RECT_HEIGHT)


    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        # 切换状态
        self.handle_states(keys)

    # 处理各种状态
    def handle_states(self, keys):
        self.judge_jump(keys)
        self.judge_attack(keys)
        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'attack':
            self.attack(keys)
        # 面向的图片
        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    # 站立
    def stand(self, keys):
        self.frame_index = 0
        # 方向右键
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        # 左键
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'
        # 空格跳跃
        elif keys[pygame.K_SPACE] and self.can_jump:
            self.y_vel = CONS.MAX_Y_SPEED
            self.state = 'jump'
            self.jumping_timer = self.current_time


        # 按z键攻击
        elif keys[pygame.K_z] and self.can_attack:
            self.state = 'attack'
            self.attacking_time = self.current_time

    # 行走
    def walk(self, keys):
        # 定义最大速度和加速度
        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel
        # 如果相应时间大于100毫秒，换帧
        if self.current_time - self.walking_timer > 100:
            if self.frame_index < 5:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time

        if keys[pygame.K_SPACE] and self.can_jump:
            self.y_vel = CONS.MAX_Y_SPEED
            self.state = 'jump'
            self.jumping_timer = self.current_time

        # 按z键攻击
        elif keys[pygame.K_z] and self.can_attack:
            self.x_vel = 0.4 * self.x_vel
            self.state = 'attack'
            self.attacking_time = self.current_time

        # 向左移动
        elif keys[pygame.K_RIGHT]:
            self.face_right = True
            # 如果速度小于0，刹车站立帧
            if self.x_vel < 0:
                self.frame_index = 1
                self.x_accel = self.turn_accel
            # 计算速度
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 1
                self.x_accel = self.turn_accel
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, False)



        # 什么按键都不按，则切换到站立状态
        else:
            if self.face_right:
                self.x_vel -= self.x_accel
                if self.x_vel < 0:
                    self.x_vel = 0
                    self.state = 'stand'
            else:
                self.x_vel += self.x_accel
                if self.x_vel > 0:
                    self.x_vel = 0
                    self.state = 'stand'

    # 跳跃
    def jump(self, keys):
        self.frame_index = 6
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        if self.current_time - self.jumping_timer > 120:
            self.frame_index += 1
        self.can_jump = False
        self.y_vel += CONS.ANTI_GRAVITY
        if self.y_vel >= 0:
            self.state = 'fall'

    # 下落
    def fall(self, keys):
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        self.frame_index = 8
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)

    # 判断是否可以跳跃
    def judge_jump(self, keys):
        if not keys[pygame.K_SPACE]:
            self.can_jump = True

    # 攻击
    def attack(self, keys):
        self.can_attack = False
        self.is_attacking = True
        self.frame_index = 9
        if self.current_time - self.attacking_time > 150:
            self.frame_index = 10
        if self.current_time - self.attacking_time > 200:
            self.frame_index = 11
        if self.current_time - self.attacking_time > 250:
            self.frame_index = 12
        if self.current_time - self.attacking_time > 300:
            self.frame_index = 9
        if self.current_time - self.attacking_time > 400:
            self.state = 'walk'
            self.is_attacking = False

    def hit(self, keys):
        pass

    def judge_attack(self, keys):
        if not keys[pygame.K_z]:
            self.can_attack = True