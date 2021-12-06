import pygame


# 物品类
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 触发点
class Checkpoint(Item):
    def __init__(self, x, y, w, h, checkpoint_type, enemy_groupid = None) :
        Item.__init__(self, x, y, w, h)
        self.checkpoint_type = checkpoint_type
        self.enemy_groupid = enemy_groupid

