import pygame
import constants as CONS

class Info:
    # 用于各个场景的切换
    # For switching between scenes
    def __init__(self, state):
        self.state = state