import pygame

class UserInputs:
    def __init__(self):
        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = False
        self.quit_requested = False

    def update(self):
        self.space_pressed = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_requested = True
                elif event.key == pygame.K_SPACE:
                    self.space_pressed = True

        keys = pygame.key.get_pressed()
        self.up_pressed = keys[pygame.K_UP]
        self.down_pressed = keys[pygame.K_DOWN]
