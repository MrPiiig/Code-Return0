"""
角色的所有行为
All actions of the character
"""
import setup
import pygame
# 导入常量数据
# Importing constant data
import constants as CONS
import util

#定义攻击类
#Defining the attack class
class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, w, h)


# 定义玩家类
# Defining the player class
class Player(pygame.sprite.Sprite):
    # 类方法， method
    # Defining class methods
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.setup_state()
        self.setup_timers()
        self.setup_velocities()
        self.load_images()
        self.setup_attack()
        self.type = "player"

    # 设定左右侧攻击矩形范围
    # Set left and right side attack rectangle range
    def setup_attack(self):
        self.right_attack = Attack(self.rect.right, self.rect.top, CONS.PLAYER_ATTACK_WIDTH, CONS.PLAYER_ATTACK_HEIGHT)
        self.left_attack = Attack(self.rect.left - CONS.PLAYER_TEXTURE_OFFSET_X, self.rect.top,
                                  CONS.PLAYER_ATTACK_WIDTH, CONS.PLAYER_ATTACK_HEIGHT)

    # 主角状态
    # Main character status
    def setup_state(self):
        # 初始化血量
        # Initialized blood volume
        self.hp = CONS.PLAYER_HP
        # 初始化状态为 "站立"
        # Initialized to "standing"
        self.state = 'stand'
        # 初始化死亡状态
        # Initialising the state of death
        self.dead = False
        # 脸朝向为右
        # Main character facing right
        self.face_right = True
        # 初始帧
        # Initial frame
        self.frame_index = 0
        # 攻击状态判断
        # Attack status determination
        self.is_attacking = False
        # 能否跳跃判断
        # Jumping judgement
        self.can_jump = True
        # 能否攻击判断
        # Able to attack judgment
        self.can_attack = True
        # 判断能否受到攻击
        # Determine if the attack is possible.
        self.can_be_hit = True
        # 正在死亡
        # Dying
        self.dying = True

    # 各种计时器，以后buff时间，道具使用倒计时
    # Various timers, later buff times, prop use countdowns.
    def setup_timers(self):
        # 设定行走状态计时器初值
        # Set initial value of walking timer
        self.walking_timer = 0
        # 设定跳跃状态计时器初值
        # Set initial value of jumping timer
        self.jumping_timer = 0
        # 设定攻击状态计时器初值
        # Set initial value of attack timer
        self.attacking_timer = 0
        # 设定受击状态计时器初值
        # Set initial value of attacked timer
        self.hit_timer = 0
        # 设定死亡状态计时器初值
        # Set initial value of dying timer
        self.death_timer = 0

    # 速度数值
    # Speed values
    def setup_velocities(self):
        # 设定player的x轴速度初始值
        # Set the initial value of the player's x-axis speed
        self.x_vel = 0
        # 设定player的y轴速度初始值
        # Set the initial value of the player's y-axis speed
        self.y_vel = 0
        # 设定行走的最大速度
        # Set the maximum speed of travel
        self.max_walk_vel = CONS.MAX_WALK_SPEED
        # 设定y轴上的最大速度
        # Set the maximum speed of y-axis
        self.max_y_vel = CONS.MAX_Y_SPEED
        # 设定行走的最大加速度
        #Setting the maximum acceleration for travel
        self.walk_accel = CONS.WALK_ACCEL
        # 设定转向时的加速度
        # Set acceleration during steering
        self.turn_accel = CONS.TRUN_ACCEL
        # 设定x轴方向上的最大速度是行走速度
        # Set the maximum speed in the x-axis direction as the travel speed
        self.max_x_vel = self.max_walk_vel
        # 设定x轴方向上的加速度为行走的最大加速度
        # Set the acceleration in the x-axis direction as the maximum acceleration for travel
        self.x_accel = self.walk_accel

    # 帧造型，方便表示出运动的变化
    # A frame shape that conveniently represents the change of movement.
    def load_images(self):
        self.right_frames = []
        self.left_frames = []
        running_frames = ['Move_1', 'Move_2', 'Move_3', 'Move_4', 'Move_5']  # 1~5
        jumping_frames = ['Jump_1', 'Jump_2', 'Jump_3']  # 6, 7, 8
        attacking_frames = ['Attack_1', 'Attack_2', 'Attack_3', 'Attack_4']  # 9~12
        dying_frames = ['Died_1', 'Died_2', 'Died_3', 'Died_4', 'Died_5', 'Died_6'] # 13~18
        left_stand_image = setup.player_graphics['Stand_1']  # 0
        left_stand_image = pygame.transform.scale(left_stand_image, (
            int(left_stand_image.get_width() * 0.4), int(left_stand_image.get_height() * 0.4)))
        right_stand_image = pygame.transform.flip(left_stand_image, True, False)
        self.right_frames.append(right_stand_image)
        self.left_frames.append(left_stand_image)

        for running_frame in running_frames:
            # 向左移动
            # Move to the left
            left_image = setup.player_graphics[running_frame]
            left_image = pygame.transform.scale(left_image,
                                                (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            # 翻转并向右移动
            # Flip and move to the right
            right_image = pygame.transform.flip(left_image, True, False)
            # 向右叠加图片
            # Overlaying images to the right
            self.right_frames.append(right_image)
            # 向左叠加图片
            # Overlay image to the left
            self.left_frames.append(left_image)
        # Loading jump frames
        for jumping_frame in jumping_frames:
            # 向左跳跃
            # Jump to the left
            left_image = setup.player_graphics[jumping_frame]
            left_image = pygame.transform.scale(left_image,
                                                (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            # 向右跳跃
            # Jump to the right
            right_image = pygame.transform.flip(left_image, True, False)
            # 添加图片
            # Add image
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
        # Loading attacking frames
        for attacking_frame in attacking_frames:
            # 向左跳跃
            # Jump to the left
            left_image = setup.player_graphics[attacking_frame]
            left_image = pygame.transform.scale(left_image,
                                                (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            # 向右跳跃
            # Jump to the right
            right_image = pygame.transform.flip(left_image, True, False)
            # 添加图片
            # Add image
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
        # Loading dying frames
        for dying_frame in dying_frames:

            # 向左跳跃
            # Jump to the left
            left_image = setup.player_graphics[dying_frame]
            left_image = pygame.transform.scale(left_image,
                                                (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            # 向右跳跃
            # Jump to the right
            right_image = pygame.transform.flip(left_image, True, False)
            # 添加图片
            # Add image
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)

        left_hit_image = setup.player_graphics['Hit_1']  # 19
        left_hit_image = pygame.transform.scale(left_hit_image, (
            int(left_hit_image.get_width() * 0.4), int(left_hit_image.get_height() * 0.4)))
        right_hit_image = pygame.transform.flip(left_hit_image, True, False)
        self.right_frames.append(right_hit_image)
        self.left_frames.append(left_hit_image)
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = pygame.Rect(0, 0, CONS.PLAYER_RECT_WIDTH, CONS.PLAYER_RECT_HEIGHT)

    # 更新按键状态
    # Update button status
    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        self.update_attack_position()
        # 切换状态
        # Switching status
        self.handle_states(keys)

    # 更新攻击范围的位置
    # Update the location of the attack range
    def update_attack_position(self):
        self.right_attack.rect.x = self.rect.right
        self.left_attack.rect.x = self.rect.left - self.rect.width
        self.right_attack.rect.y = self.rect.top
        self.left_attack.rect.y = self.rect.top

    # 处理各种状态
    # Handling various states
    def handle_states(self, keys):
        self.judge_jump(keys)
        self.judge_attack(keys)
        # 站立状态
        # Standing position

        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'hit':
            self.hit(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'attack':
            self.attack(keys)
        # 死亡
        # Death
        elif self.state == 'die':
            self.die(keys)
        # 面向的图片
        # Pictures of player orientation
        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]


    # 站立
    # Standing
    def stand(self, keys):
        self.frame_index = 0
        # 方向右键
        # Directional right button
        if keys[pygame.K_d]:
            self.face_right = True
            self.state = 'walk'
        # 左键
        # Directional left button
        elif keys[pygame.K_a]:
            self.face_right = False
            self.state = 'walk'
        # 按住K键跳跃
        # Press and hold K to jump
        elif keys[pygame.K_k] and self.can_jump:
            self.y_vel = CONS.MAX_Y_SPEED
            self.state = 'jump'
            self.jumping_timer = self.current_time
            jump_sound = setup.game_sounds['Jump']
            jump_sound.play()


        # 按j键攻击
        # Press j to attack
        elif keys[pygame.K_j] and self.can_attack:
            attack_sound_player = setup.game_sounds['Attack_1']
            attack_sound_player.stop()
            attack_sound_player.play()
            self.state = 'attack'
            self.attacking_timer = self.current_time

    # 行走
    # Walking
    def walk(self, keys):
        # 定义最大速度和加速度
        # Define maximum velocity and acceleration.
        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel
        # 如果相应时间大于100毫秒，换帧
        # If the corresponding time is greater than 100milliseconds, change the frame.
        if self.current_time - self.walking_timer > 100:
            if self.frame_index < 5:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time

        if keys[pygame.K_k] and self.can_jump:
            self.y_vel = CONS.MAX_Y_SPEED
            self.state = 'jump'
            jump_sound = setup.game_sounds['Jump']
            jump_sound.play()
            self.jumping_timer = self.current_time

        # 按z键攻击
        # Press z to attack
        elif keys[pygame.K_j] and self.can_attack:
            attack_sound_player = setup.game_sounds['Attack_1']
            attack_sound_player.stop()
            attack_sound_player.play()
            self.x_vel = 0.4 * self.x_vel
            self.state = 'attack'
            self.attacking_timer = self.current_time

        # 向左移动
        # Move to the left
        elif keys[pygame.K_d]:
            self.face_right = True
            # 如果速度小于0，刹车站立帧
            # If the speed is less than 0, brake the standing frame.
            if self.x_vel < 0:
                self.frame_index = 1
                self.x_accel = self.turn_accel
            # 计算速度
            # Calculation speed
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_a]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 1
                self.x_accel = self.turn_accel
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        # 什么按键都不按，则切换到站立状态
        # If do not press any buttons, player switch to standing
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
    # Jump
    def jump(self, keys):

        self.frame_index = 6
        if keys[pygame.K_d]:
            self.face_right = True
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_a]:
            self.face_right = False
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        if self.current_time - self.jumping_timer > 120:
            self.frame_index += 1
        self.can_jump = False
        self.y_vel += CONS.ANTI_GRAVITY
        if self.y_vel >= 0:
            self.state = 'fall'

    # 下落
    # Fall
    def fall(self, keys):
        if keys[pygame.K_d]:
            self.face_right = True
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_a]:
            self.face_right = False
            self.x_vel = util.calcu_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        self.frame_index = 8
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)

    # 判断是否可以跳跃
    # Determine if a jump is possible.
    def judge_jump(self, keys):
        if not keys[pygame.K_k]:
            self.can_jump = True

    # 攻击
    # Attack
    def attack(self, keys):
        self.can_attack = False
        self.is_attacking = True
        self.frame_index = 9
        if self.current_time - self.attacking_timer > 150:
            self.frame_index = 10
        if self.current_time - self.attacking_timer > 200:
            self.frame_index = 11
        if self.current_time - self.attacking_timer > 250:
            self.frame_index = 12
        if self.current_time - self.attacking_timer > 300:
            self.frame_index = 9
        if self.current_time - self.attacking_timer > 400:
            self.state = 'walk'
            self.is_attacking = False

    # 受到攻击
    # Attacked
    def hit(self, keys):
        if self.can_be_hit:
            attacked_sound = setup.game_sounds['attacked_player']
            attacked_sound.play()
        self.is_attacking = False
        self.frame_index = 19
        self.can_be_hit = False
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)
        if self.current_time - self.hit_timer > 200:
            self.x_vel = 0
        if self.current_time - self.hit_timer > 1000:
            self.can_be_hit = True
            self.state = 'walk'

    # 判断能否攻击
    # Determining whether an attack is possible
    def judge_attack(self, keys):
        if not keys[pygame.K_j]:
            self.can_attack = True

    # 切换死亡状态
    # Switching the state of death
    def go_die(self):
        self.frame_index = 2
        self.state = 'die'
        if self.dying:
            self.death_timer = self.current_time
            self.dying = False

    # 死亡
    # Death
    def die(self, keys):
        self.x_vel = 0
        self.y_vel = 0
        if self.current_time - self.death_timer > 50:
            self.frame_index = 13
        if self.current_time - self.death_timer > 100:
            self.frame_index = 14
        if self.current_time - self.death_timer > 150:
            self.frame_index = 15
        if self.current_time - self.death_timer > 200:
            self.frame_index = 16
        if self.current_time - self.death_timer > 400:
            self.frame_index = 17
        if self.current_time - self.death_timer > 600:
            self.frame_index = 18
        if self.current_time - self.death_timer > 1000:
            self.dead = True


