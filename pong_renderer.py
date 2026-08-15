import pygame

class PongRenderer:
    def __init__(self, width=800, height=600, caption="Pong"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def render(self, engine, score_label, score_val):
        # Clean black background
        self.screen.fill((0, 0, 0))

        # Right Wall Rect
        wall_rect = pygame.Rect(engine.wall_left, engine.wall_top, 15, engine.height - 20)

        # Draw bounds (top line, bottom line, right wall) in simple white
        pygame.draw.line(self.screen, (255, 255, 255), (10, 10), (self.width - 10, 10), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (10, self.height - 10), (self.width - 10, self.height - 10), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), wall_rect)

        # Draw paddle
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            pygame.Rect(engine.paddle.x, engine.paddle.y, engine.paddle.width, engine.paddle.height)
        )

        # Draw ball
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (int(engine.ball.x), int(engine.ball.y)),
            engine.ball.radius
        )

        # Draw Score HUD
        score_text = self.font.render(f"{score_label}: {score_val}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

        pygame.display.flip()

    def tick(self, fps=60):
        self.clock.tick(fps)

    def check_events(self):
        """
        Polls Pygame events and queries keyboard status.
        Returns:
            quit_requested (bool): True if the window was closed or ESC was pressed.
            up_pressed (bool): True if the UP arrow key is pressed.
            down_pressed (bool): True if the DOWN arrow key is pressed.
        """
        quit_requested = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_requested = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_requested = True

        keys = pygame.key.get_pressed()
        up_pressed = keys[pygame.K_UP]
        down_pressed = keys[pygame.K_DOWN]

        return quit_requested, up_pressed, down_pressed

    def close(self):
        pygame.quit()
