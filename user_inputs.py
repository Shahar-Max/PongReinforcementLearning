import pygame

class UserInputs:
    def __init__(self):
        self.up_pressed = False
        self.down_pressed = False
        self.quit_requested = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_requested = True

        keys = pygame.key.get_pressed()
        self.up_pressed = keys[pygame.K_UP]
        self.down_pressed = keys[pygame.K_DOWN]
