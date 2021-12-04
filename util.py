import sys
import pygame
import random
import os
import constants as CONS


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
def load_graphics(path, accept=('.jpg', '.png')):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            graphics[name] = img

    return graphics

# 计算加速度函数
def calcu_vel(vel, accel, max_vel, is_positive=True):
    if is_positive:
        return min(vel + accel, max_vel)
    else:
        return max(vel - accel, -max_vel)



#文字生成
def creat_info(label,size=40,width_size=1,heigtt_size=1):
    font=pygame.font.Font(CONS.FONT,size)
    #将文字生成为图片,（层级，是否抗锯齿，颜色rgb)
    font_image=font.render(label,1,(0,0,0))

    return font_image