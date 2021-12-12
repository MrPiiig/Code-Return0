import pygame


# 物品类
# Items
# 基本的物品类，包含底板，平台等
# Basic items, including baseboards, platforms, etc.
class Item(pygame.sprite.Sprite):
    # 初始化了一透明物品（地板）
    # Initialized a transparent item (floor)
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 触发点
# checkpoint class
class Checkpoint(Item):
    def __init__(self, x, y, w, h, checkpoint_type, enemy_groupid = None) :
        Item.__init__(self, x, y, w, h)
        self.checkpoint_type = checkpoint_type
        self.enemy_groupid = enemy_groupid

