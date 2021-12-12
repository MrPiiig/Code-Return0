from components import info
import pygame

#定义一个加载场景类
class LoadScene:
    def __init__(self):
        self.finished = False
        self.next = 'main_scene'
        # 阶段的持续时间
        self.duration = 2000
        self.timer = 0
        self.info = info.Info('load_scene')

    def update(self, surface, keys):
        self.draw(surface)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished = True
            self.timer = 0

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.info.draw(surface)


class GameOver(LoadScene):
    def __init__(self):
        LoadScene.__init__(self)
        self.next = 'main_scene'
        self.duration = 4000
        self.info = info.Info('game_over')

    def draw(self, surface):
        surface.fill((255, 0, 0))
        self.info.draw(surface)