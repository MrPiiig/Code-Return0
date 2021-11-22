import sys
import pygame
import random
import os

class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        # 按键
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
        self.state.update(self.screen, self.keys)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                if event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.display.quit()

            self.update()

            pygame.display.update()
            self.clock.tick(60)

# 读取图片
def load_graphics(path):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)

        img = pygame.image.load(os.path.join(path, pic))
        graphics[name] = img

    return graphics

# 计算加速度函数
def calcu_vel(vel, accel, max_vel, is_positive=True):
    if is_positive:
        return min(vel + accel, max_vel)
    else:
        return max(vel - accel, -max_vel)


