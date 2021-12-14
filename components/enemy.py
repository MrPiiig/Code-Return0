import pygame
import setup
import util
import constants as CONS
from components import player



# 生成敌人实例，player是enemy的对象
# Generate an enemy instance, player is the target of enemy.
def create_enemy(enemy_data, player):
    enemy_type = enemy_data['type']
    if enemy_type == 0:
        enemy = Enemy(enemy_data['x'], enemy_data['y'], enemy_data['width'], enemy_data['height'], enemy_data['left'], enemy_data['right'], player)
        return enemy


# 敌人基类
# Enemy Superclass
class Enemy(pygame.sprite.Sprite):
    walk_left = 0
    walk_right = 0
    def __init__(self, x, y, w, h,left, right, target):
        pygame.sprite.Sprite.__init__(self)
        self.setup_state()
        self.setup_timer()
        self.setup_velocities(x, y)
        self.setup_box(x, y, w, h, left, right)
        self.setup_attack()
        self.load_images()
        #设定索敌对象(player)
        self.target = target


    # 初始化碰撞盒子
    # Initialize the collision box.
    def setup_box(self, x, y, w, h, left, right):
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.x = x
        self.rect.bottom = y
        self.walk_left = left
        self.walk_right = right

    # 初始化各类状态判断
    # Initialisation of various status judgements.
    def setup_state(self):
        self.state = "walk"
        self.face_right = False
        self.hit_from_right = True
        self.can_be_hit = True
        self.frame_index = 0
        self.type = 'enemy'
        self.hp = CONS.ENEMY_HP

    # 初始化各类计时器
    # Initialisation of the various timers.
    def setup_timer(self):
        self.timer = 0
        # 受击计时器，计算受击时间
        # Strike timer to calculate the time taken.
        self.hit_timer = 0
        # 死亡计时器，计算死亡时间
        # Death timer to calculate the time of death.
        self.death_timer = 0
        # 获取当前时间
        # Get the current time
        self.current_time = pygame.time.get_ticks()

    # 初始化速度相关属性
    # Initialize speed-related attributes.
    def setup_velocities(self, x, y):
        self.x_vel = -1 * CONS.ENEMY_WALK_SPEED
        self.y_vel = 0



    # 初始化攻击范围
    # Initialize the attack range
    def setup_attack(self):
        pass
        self.right_attack = player.Attack(self.rect.right, self.rect.top, CONS.PLAYER_ATTACK_WIDTH, CONS.PLAYER_ATTACK_HEIGHT)
        self.left_attack = player.Attack(self.rect.left - CONS.PLAYER_TEXTURE_OFFSET_X, self.rect.top,
                                  CONS.PLAYER_ATTACK_WIDTH, CONS.PLAYER_ATTACK_HEIGHT)
    # 绘制血条
    # Drawing health strips
    def draw_hp(self, surface):
        hp_percent = self.hp / CONS.ENEMY_HP
        hp_black = setup.enemy_graphics['enemy_hp_black']
        hp_red = setup.enemy_graphics['enemy_hp_red']
        hp_red = pygame.transform.scale(hp_red, (int(hp_red.get_width() * hp_percent), int(hp_red.get_height())))
        surface.blit(hp_red, (self.rect.x + 18, self.rect.y - 20))
        surface.blit(hp_black, (self.rect.x + 8, self.rect.y - 20))

    # 加载图片
    # Loading images
    def load_images(self):
        self.right_frames = []
        self.left_frames = []
        running_frames = ["Enemy_Move_1", "Enemy_Move_2", "Enemy_Move_3", "Enemy_Move_4", "Enemy_Move_5"] #  0~4
        attack_frames = ["Enemy_Attack_1", "Enemy_Attack_2", "Enemy_Attack_3", "Enemy_Attack_4"]  # 5~8
        dying_frames = ["Enemy_Dead_1", "Enemy_Dead_2", "Enemy_Dead_3", "Enemy_Dead_4"]  # 9~12

        # 载入跑步帧
        # load running frames
        for running_frames in running_frames:
            left_image = setup.enemy_graphics[running_frames]
            left_image = pygame.transform.scale(left_image, (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
        # 载入攻击帧
        # load attack frames
        for attack_frame in attack_frames:
            left_image = setup.enemy_graphics[attack_frame]
            left_image = pygame.transform.scale(left_image,
                                                (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
        #载入死亡帧
        # load dying frames
        for dying_frame in dying_frames:
            left_image = setup.enemy_graphics[dying_frame]
            left_image = pygame.transform.scale(left_image,
                                                (int(left_image.get_width() * 0.4), int(left_image.get_height() * 0.4)))
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)

        #载入受击帧
        # load attacked frames
        left_hit_image = setup.enemy_graphics['Enemy_Hit_1']  # 13
        left_hit_image = pygame.transform.scale(left_hit_image, (
            int(left_hit_image.get_width() * 0.4), int(left_hit_image.get_height() * 0.4)))
        right_hit_image = pygame.transform.flip(left_hit_image, True, False)
        self.right_frames.append(right_hit_image)
        self.left_frames.append(left_hit_image)

        self.frames = self.left_frames
        self.image = self.frames[self.frame_index]

    # 更新函数
    # Update functions
    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.update_attack_position()
        self.handle_states()

    # 更新攻击范围
    def update_attack_position(self):
        self.right_attack.rect.x = self.rect.right
        self.left_attack.rect.x = self.rect.left - self.rect.width
        self.right_attack.rect.y = self.rect.top
        self.left_attack.rect.y = self.rect.top

    # 状态机
    # Status machines
    def handle_states(self):
        if self.state == 'walk':
            self.walk()
        elif self.state == 'stand':
            self.stand()
        elif self.state == "die":
            self.die()
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
    # Standing
    def stand(self):
        self.x_vel = 0
        self.frame_index = 1
        

    # 坠落
    # Falling
    def fall(self):
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)


    # 敌人巡逻
    # Enemy patrols
    def walk(self):
        if abs(self.target.rect.x - self.rect.x) < 300 and abs(self.rect.y - self.target.rect.y) < 100:
            self.state = "follow_player"
        if self.current_time - self.timer > 150:
            self.frame_index += 1
            self.frame_index %= 5
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time
        #如果到达巡逻左边界或巡逻右边界，敌人掉头
        #If patrol left border or patrol right border is reached, enemy turns around
        if self.rect.x < self.walk_left:
            self.face_right = True
            self.x_vel = 1 * CONS.ENEMY_WALK_SPEED
        elif self.rect.x > self.walk_right:
            self.face_right = False
            self.x_vel = -1 * CONS.ENEMY_WALK_SPEED

    # 敌人追击
    # Enemy in pursuit
    def follow_player(self):
        if self.current_time - self.timer > 100:
            self.frame_index += 1
            self.frame_index %= 5
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time
        if abs(self.rect.x - self.target.rect.x) > 300 or abs(self.rect.y - self.target.rect.y) > 100:
            self.state = "walk"
        if abs(self.rect.x - self.target.rect.x) < 150 and abs(self.rect.y - self.target.rect.y) < 100:
            self.state = "attack"

        if self.target.rect.x < self.rect.x:
            self.face_right = False
            self.x_vel = -1 * CONS.ENEMY_FOLLOW_SPEED

        elif self.target.rect.x > self.rect.x:
            self.face_right = True
            self.x_vel = 1 * CONS.ENEMY_FOLLOW_SPEED



    # 敌人攻击
    # Enemy attack
    def attack(self):
        self.x_vel = 0
        self.frame_index = 5
        if 400 < self.current_time - self.timer < 550:
            self.check_attack_player_collisions()
        if self.current_time - self.timer > 400:
            self.frame_index = 6
        if self.current_time - self.timer > 450:
            self.frame_index = 7
        if self.current_time - self.timer > 500:
            self.frame_index = 8
        if self.current_time - self.timer > 550:
            self.frame_index = 5
        if self.current_time - self.timer > 1500:
            self.state = 'follow_player'


    # 检测攻击与玩家碰撞
    # Detects attacks colliding with the player.
    def check_attack_player_collisions(self):
        if self.face_right:
            # 如果enemy面朝右侧且目标可以被攻击，执行以下操作
            # If the enemy is facing right and the target can be attacked, do the following
            if pygame.sprite.collide_rect(self.right_attack, self.target) and self.target.can_be_hit:
                attack_sound = setup.game_sounds['Attack_2']
                attack_sound.stop()
                attack_sound.play()
                self.target.state = 'hit'
                self.target.x_vel = 3
                self.target.y_vel = -2
                self.target.hp -= CONS.ENEMY_ATTACK_VALUE
                if self.target.hp < 0:
                    self.target.hp =0
                self.target.hit_timer = self.current_time
                self.target.face_right = False

        else:
            # 如果enemy面朝左侧且目标可以被攻击，执行以下操作
            # If the enemy is facing left and the target can be attacked, do the following
            if pygame.sprite.collide_rect(self.left_attack, self.target) and self.target.can_be_hit:
                attack_sound = setup.game_sounds['Attack_2']
                attack_sound.stop()
                attack_sound.play()
                self.target.state = 'hit'
                self.target.x_vel = -3
                self.target.y_vel = -2
                self.target.hp -= CONS.ENEMY_ATTACK_VALUE
                if self.target.hp < 0:
                    self.target.hp = 0
                self.target.hit_timer = self.current_time
                self.target.face_right = True

    # 受到攻击
    # Attacked
    def hit(self):
        if self.can_be_hit:
            attacked_sound = setup.game_sounds['attacked_enemy']
            attacked_sound.play()
        self.frame_index = 13
        self.can_be_hit = False
        # 受到攻击时，改变x轴方向上的速度值，形成击退效果
        # When attacked, changes the speed value in the x-axis direction, creating a knockback effect
        if self.hit_from_right:
            self.x_vel = -2
        else:
            self.x_vel = 2
        self.y_vel = util.calcu_vel(self.y_vel, CONS.GRAVITY, -CONS.MAX_Y_SPEED)
        if self.current_time - self.hit_timer > 200:
            self.x_vel = 0
        if self.current_time - self.hit_timer > 1000:
            self.can_be_hit = True
            if self.hit_from_right:
                self.x_vel = 1
            else:
                self.x_vel = -1
            self.state = "follow_player"

    def die(self):
        self.can_be_hit = False
        # 如果当前的时间减去死亡时间大于设定值，逐帧加载死亡效果帧
        # If the current time minus the death time is greater than the set value, load the death effect frame by frame
        if self.current_time - self.death_timer > 50:
            self.frame_index = 9
        if self.current_time - self.death_timer > 100:
            self.frame_index = 10
        if self.current_time - self.death_timer > 200:
            self.frame_index = 11
        if self.current_time - self.death_timer > 300:
            self.frame_index = 12
        if self.current_time - self.death_timer > 330:
            self.enemy_group.remove(self)
            self.enemy_dead_group.add(self)


    def go_die(self, enemy_group, enemy_dead_group):
        # 使得enemy状态机进入die状态
        # Enables the enemy state machine to enter 'die' state
        self.x_vel = 0
        self.state = 'die'
        self.death_timer = self.current_time
        self.enemy_group = enemy_group
        self.enemy_dead_group = enemy_dead_group


