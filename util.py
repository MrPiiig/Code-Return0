import sys
import pygame
import random
import os

class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def run(self, stage):
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                if event.type == pygame.KEYUP:
                    keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    sys.exit()

            stage.update(self.screen, keys)
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


