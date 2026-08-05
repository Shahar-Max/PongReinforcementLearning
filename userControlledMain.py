import pygame
import sys
from game_engine import PongEngine
from user_inputs import UserInputs

def main():
    pygame.init()
    
    # Screen Setup
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong - Wall Challenge")
    clock = pygame.time.Clock()
    FPS = 60

    # Instantiate Engine and Presentation components
    engine = PongEngine(WIDTH, HEIGHT)
    inputs = UserInputs()
    
    # Right Wall Rect for rendering
    wall_rect = pygame.Rect(engine.wall_left, engine.wall_top, 15, engine.height - 20)

    # Font setup
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        # Update user inputs (Pygame dependent)
        inputs.update()
        if inputs.quit_requested:
            running = False

        # Step the core game logic (completely independent of Pygame)
        engine.step(inputs.up_pressed, inputs.down_pressed, inputs.space_pressed)

        # Rendering (Pygame dependent)
        screen.fill((0, 0, 0)) # Clean black background

        # Draw bounds (top line, bottom line, right wall) in simple white
        pygame.draw.line(screen, (255, 255, 255), (10, 10), (WIDTH - 10, 10), 2)
        pygame.draw.line(screen, (255, 255, 255), (10, HEIGHT - 10), (WIDTH - 10, HEIGHT - 10), 2)
        pygame.draw.rect(screen, (255, 255, 255), wall_rect)

        # Draw paddle
        pygame.draw.rect(
            screen, 
            (255, 255, 255), 
            pygame.Rect(engine.paddle.x, engine.paddle.y, engine.paddle.width, engine.paddle.height)
        )
        
        # Draw ball
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(engine.ball.x), int(engine.ball.y)),
            engine.ball.radius
        )

        score_text = font.render(f"Score: {engine.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
