"""
角色的所有行为
"""
import setup
import pygame
# 导入常量数据
import constants as CONS

# 定义玩家类
class Player(pygame.sprite.Sprite):
    # 刹车站立帧
    frame_index = 0

    # 类方法， method
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.setup_state()
        self.setup_timers()
        self.setup_velocities()
        self.load_images()

    # 主角状态
    def setup_state(self):
        # 初始化状态为 "站立"
        self.state = 'stand'
        # 脸朝向为右
        self.face_right = True

    # 各种计时器，以后buff时间，道具使用倒计时
    def setup_timers(self):
        self.walking_timer = 0

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
        running_frames = ['heroLeft1', 'heroLeft2', 'heroLeft3']
        self.right_frames = []
        self.left_frames = []
        for running_frame in running_frames:
            # 向左移动
            left_image = setup.player_graphics[running_frame]
            # 翻转并向右移动
            right_image = pygame.transform.flip(left_image, True, False)
            # 向右叠加图片
            self.right_frames.append(right_image)
            # 向左叠加
            self.left_frames.append(left_image)

        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        # 切换状态
        self.handle_states(keys)

    # 处理各种状态
    def handle_states(self, keys):
        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        # 面向的图片
        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    # 站立
    def stand(self, keys):
        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0
        # 方向右键
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        # 左键
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'
    # 行走
    def walk(self, keys):
        # 定义最大速度和加速度
        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel
        # 如果相应时间大于100毫秒，换帧
        if self.current_time - self.walking_timer > 100:
            if self.frame_index < 2:
                self.frame_index += 1
            else:
                self.frame_index = 0
            self.walking_timer = self.current_time
        # 向左移动
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            # 如果速度小于0，刹车站立帧
            if self.x_vel < 0:
                self.frame_index = 0
                self.x_accel = self.turn_accel
            # 计算速度
            self.x_vel = self.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 0
                self.x_accel = self.turn_accel
            self.x_vel = self.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, False)

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
    # 计算速度，运动的
    def calcu_vel(self, vel, accel, max_vel, is_positive=True):
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)

    def jump(self, keys):
        pass
