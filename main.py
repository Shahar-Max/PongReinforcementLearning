import pygame
import sys
import random
import math
import array

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)

# Window Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberPong - Wall Challenge")
clock = pygame.time.Clock()
FPS = 60

# Cyberpunk / Neon Theme Colors
BG_COLOR = (18, 18, 24)  # Deep slate black
PADDLE_COLOR = (57, 255, 20)  # Neon Green
WALL_COLOR = (0, 191, 255)  # Neon Blue
BALL_COLOR = (255, 255, 255)  # Bright White
TEXT_COLOR = (240, 240, 245)  # Off-white
ACCENT_COLOR = (255, 0, 127)  # Neon Pink
GRID_COLOR = (30, 30, 40)  # Dim background grid/accents


# Synthesize audio effects purely in memory
def play_synth_sound(frequency, duration_ms, wave_type="sine"):
    try:
        sample_rate = 22050
        n_samples = int(sample_rate * (duration_ms / 1000.0))
        buf = array.array('h', [0] * n_samples)

        for i in range(n_samples):
            t = i / sample_rate
            # Dynamic frequency sweep for game-over or score events
            freq = frequency
            if wave_type == "descending":
                freq = frequency * (1.0 - 0.7 * (i / n_samples))
            elif wave_type == "rising":
                freq = frequency * (1.0 + 0.3 * (i / n_samples))

            # Sine wave synthesis
            val = math.sin(2 * math.pi * freq * t)

            # Simple ADSR envelope: apply fade out
            fade_start = int(n_samples * 0.7)
            if i > fade_start:
                fade_factor = 1.0 - (i - fade_start) / (n_samples - fade_start)
                val *= fade_factor

            buf[i] = int(32767 * 0.2 * val)

        sound = pygame.mixer.Sound(buffer=buf)
        sound.play()
    except Exception:
        pass


# Particle System for Collision Effects
class Particle:
    def __init__(self, x, y, dx, dy, color, size, lifetime):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        # Slowly shrink size
        self.size = max(0.5, self.size * 0.95)

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int((self.lifetime / self.max_lifetime) * 255)
            # Create a surf with alpha for particle fade
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class ParticleManager:
    def __init__(self):
        self.particles = []

    def spawn_burst(self, x, y, color, count=15):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, 5.0)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            size = random.uniform(2.0, 5.0)
            lifetime = random.randint(20, 45)
            self.particles.append(Particle(x, y, dx, dy, color, size, lifetime))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


# Game Entities
class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.glow_timer = 0

    def move(self, dy):
        self.rect.y += dy * self.speed
        # Boundary collision check
        if self.rect.top < 15:
            self.rect.top = 15
        if self.rect.bottom > HEIGHT - 15:
            self.rect.bottom = HEIGHT - 15

    def draw(self, surface):
        # Draw soft glow behind paddle if hit recently
        if self.glow_timer > 0:
            for i in range(4, 0, -1):
                glow_rect = self.rect.inflate(i * 4, i * 4)
                alpha = int((self.glow_timer / 15) * 50)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*PADDLE_COLOR, alpha), (0, 0, glow_rect.width, glow_rect.height),
                                 border_radius=4)
                surface.blit(glow_surf, glow_rect.topleft)
            self.glow_timer -= 1

        # Draw paddle base
        pygame.draw.rect(surface, PADDLE_COLOR, self.rect, border_radius=4)
        # Inner highlights for sleek look
        pygame.draw.rect(surface, (255, 255, 255), self.rect.inflate(-4, -20), border_radius=2)


class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.reset()
        self.trail = []

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = 6.0
        self.dy = random.choice([-3.0, -2.0, 2.0, 3.0])
        self.trail = []

    def update(self):
        # Save trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

        # Move
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        # Draw trailing path
        for idx, pos in enumerate(self.trail):
            alpha = int((idx / len(self.trail)) * 100)
            radius = int(self.radius * (0.4 + 0.6 * (idx / len(self.trail))))
            trail_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (*PADDLE_COLOR, alpha), (radius, radius), radius)
            surface.blit(trail_surf, (int(pos[0] - radius), int(pos[1] - radius)))

        # Draw core ball
        pygame.draw.circle(surface, BALL_COLOR, (int(self.x), int(self.y)), self.radius)


def main():
    # Fonts
    try:
        font_large = pygame.font.SysFont("Outfit", 64, bold=True)
        font_medium = pygame.font.SysFont("Outfit", 32, bold=True)
        font_small = pygame.font.SysFont("Outfit", 20)
    except:
        # Fallback to sans
        font_large = pygame.font.Font(None, 74)
        font_medium = pygame.font.Font(None, 40)
        font_small = pygame.font.Font(None, 24)

    # Initialize game objects
    paddle = Paddle(30, HEIGHT // 2 - 45, 16, 90, 8)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 8)
    particles = ParticleManager()

    # Wall info (right side)
    wall_rect = pygame.Rect(WIDTH - 40, 15, 16, HEIGHT - 30)

    # State variables
    game_state = "START"
    score = 0
    high_score = 0

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == "START":
                    if event.key == pygame.K_SPACE:
                        game_state = "PLAYING"
                        score = 0
                        ball.reset()
                        play_synth_sound(523, 150, "rising")  # Start chime
                elif game_state == "GAME_OVER":
                    if event.key == pygame.K_SPACE:
                        game_state = "PLAYING"
                        score = 0
                        ball.reset()
                        play_synth_sound(523, 150, "rising")

        # 2. Logic Updates
        if game_state == "PLAYING":
            # Keyboard inputs for paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                paddle.move(-1)
            if keys[pygame.K_DOWN]:
                paddle.move(1)

            # Update Ball
            ball.update()

            # Collision: Top and Bottom bounds
            if ball.y - ball.radius < 15:
                ball.y = 15 + ball.radius
                ball.dy *= -1
                particles.spawn_burst(ball.x, ball.y, WALL_COLOR, 8)
                play_synth_sound(300, 60)
            elif ball.y + ball.radius > HEIGHT - 15:
                ball.y = HEIGHT - 15 - ball.radius
                ball.dy *= -1
                particles.spawn_burst(ball.x, ball.y, WALL_COLOR, 8)
                play_synth_sound(300, 60)

            # Collision: Right Wall
            if ball.x + ball.radius > wall_rect.left:
                # Inside wall horizontal span
                if wall_rect.top <= ball.y <= wall_rect.bottom:
                    ball.x = wall_rect.left - ball.radius
                    ball.dx *= -1
                    # Spawn particles with wall color (blue)
                    particles.spawn_burst(ball.x, ball.y, WALL_COLOR, 15)
                    play_synth_sound(440, 80)

            # Collision: Left Paddle
            if ball.dx < 0:  # Ball moving left
                # Horizontal collision check
                if paddle.rect.left <= ball.x - ball.radius <= paddle.rect.right:
                    # Vertical overlap check
                    if paddle.rect.top <= ball.y <= paddle.rect.bottom:
                        ball.x = paddle.rect.right + ball.radius

                        # Deflection math based on where the ball hit the paddle
                        relative_intersect_y = (paddle.rect.y + paddle.rect.height / 2) - ball.y
                        normalized_intersect_y = relative_intersect_y / (paddle.rect.height / 2)
                        bounce_angle = normalized_intersect_y * (math.pi / 3)  # max 60 deg deflection

                        # Calculate speed (with gradual increase)
                        speed = math.sqrt(ball.dx ** 2 + ball.dy ** 2)
                        speed = min(18.0, speed * 1.05)  # Cap speed

                        ball.dx = speed * math.cos(bounce_angle)
                        ball.dy = -speed * math.sin(bounce_angle)

                        # Score increment
                        score += 1
                        if score > high_score:
                            high_score = score

                        paddle.glow_timer = 15
                        particles.spawn_burst(ball.x, ball.y, PADDLE_COLOR, 18)
                        play_synth_sound(600, 100, "rising")

            # Miss: Ball goes off-screen left
            if ball.x - ball.radius < 0:
                game_state = "GAME_OVER"
                play_synth_sound(220, 400, "descending")
                # Spawn large explosion
                particles.spawn_burst(ball.x, ball.y, ACCENT_COLOR, 30)

        # Update Particle System
        particles.update()

        # 3. Drawingf
        screen.fill(BG_COLOR)

        # Draw decorative background grid/frame
        pygame.draw.rect(screen, GRID_COLOR, (15, 15, WIDTH - 30, HEIGHT - 30), 2)
        # Center dividing dotted line
        for y in range(25, HEIGHT - 20, 30):
            pygame.draw.line(screen, GRID_COLOR, (WIDTH // 2, y), (WIDTH // 2, y + 15), 1)

        # Draw right neon wall
        pygame.draw.rect(screen, WALL_COLOR, wall_rect, border_radius=4)
        # Inner glow line on wall
        pygame.draw.line(screen, (255, 255, 255), (wall_rect.left + 2, wall_rect.top + 8),
                         (wall_rect.left + 2, wall_rect.bottom - 8), 2)

        # Draw paddle, ball and particles
        paddle.draw(screen)
        if game_state == "PLAYING":
            ball.draw(screen)
        particles.draw(screen)

        # HUD / UI overlay
        if game_state == "START":
            # Start screen overlay
            title_text = font_large.render("CYBERPONG", True, ACCENT_COLOR)
            subtitle_text = font_medium.render("WALL CHALLENGE", True, TEXT_COLOR)
            instruct_text = font_small.render("Press SPACE to play  |  UP & DOWN arrows to move", True, WALL_COLOR)

            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3 - 30))
            screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 3 + 40))
            screen.blit(instruct_text, (WIDTH // 2 - instruct_text.get_width() // 2, HEIGHT // 2 + 50))

        elif game_state == "PLAYING":
            # Display Score
            score_text = font_large.render(str(score), True, TEXT_COLOR)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 40))

        elif game_state == "GAME_OVER":
            # Game over screen overlay
            over_title = font_large.render("GAME OVER", True, ACCENT_COLOR)
            score_summary = font_medium.render(f"Score: {score}  |  Best: {high_score}", True, TEXT_COLOR)
            restart_text = font_small.render("Press SPACE to Play Again", True, PADDLE_COLOR)

            screen.blit(over_title, (WIDTH // 2 - over_title.get_width() // 2, HEIGHT // 3 - 30))
            screen.blit(score_summary, (WIDTH // 2 - score_summary.get_width() // 2, HEIGHT // 3 + 40))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        # Present Frame
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()