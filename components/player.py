import pygame

import setup


class Player(pygame.sprite.Sprite):
    frame_index = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.setup_state()
        self.setup_timers()
        self.setup_velocities()
        self.load_images()

    def setup_state(self):
        self.idling = True
        self.running = False
        self.jumping = False
        self.attacking = False
        self.hitting = False

    def setup_timers(self):
        self.walking_timer = 0

    def setup_velocities(self):
        self.vel = 0

    def load_images(self):
        running_frames = ['heroLeft1', 'heroLeft2', 'heroLeft3']
        self.right_frames = []
        self.left_frames = []
        for running_frame in running_frames:
            left_image = setup.player_graphics[running_frame]
            right_image = pygame.transform.flip(left_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)

        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        if keys[pygame.K_d]:
            print("press d")
            self.vel = 5
            self.frames = self.right_frames
        if keys[pygame.K_a]:
            print("press a")
            self.vel = -5
            self.frames = self.left_frames

        if self.current_time - self.walking_timer > 100:
            self.walking_timer = self.current_time
            self.frame_index += 1
            self.frame_index %= 3
        self.image = self.frames[self.frame_index]