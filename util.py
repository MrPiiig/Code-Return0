import pygame
import os
import constants as CONS


class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        # 按键
        # get buttons press events
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]
    # 状态更新
    # Status Updates
    def update(self):
        if self.state.finished:
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.init_scene()
        self.state.update(self.screen, self.keys)

    def run(self):
        while True:
            # 监听全局按键
            # listen all keys
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                if event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

            self.update()

            pygame.display.update()
            self.clock.tick(60)


# 读取图片
# Loading images
def load_graphics(path, accept=('.jpg', '.png')):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            graphics[name] = img
    return graphics


# 加载音乐
# Loading music
def load_sounds(path, accept=('.mp3', '.wav')):
    sounds = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            sound = pygame.mixer.Sound(os.path.join(path, pic))
            sounds[name] = sound
    return sounds


# 计算加速度函数
# Calculating acceleration functions
def calcu_vel(vel, accel, max_vel, is_positive=True):
    if is_positive:
        return min(vel + accel, max_vel)
    else:
        return max(vel - accel, -max_vel)


# 文字生成
# Text generation
def creat_info(label, size=40):
    font = pygame.font.Font(CONS.FONT, size)
    # 将文字生成为图片,（层级，是否抗锯齿，颜色rgb)
    # Generate text as a picture, (layers, anti-aliasing or not, colour rgb)
    font_image = font.render(label, 1, (0, 0, 0))

    return font_image
