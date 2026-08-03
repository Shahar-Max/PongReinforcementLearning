from paddle import Paddle
from ball import Ball
from gamestate import GameState

class PongEngine:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        
        # Instantiate Component
        self.paddle = Paddle(30, self.height // 2 - 45, width=15, height=90, speed=8)
        self.ball = Ball(self.width // 2, self.height // 2, speed_x=5, speed_y=4)
        self.game_state = GameState()
        
        # Define logical boundaries of the right wall
        # wall_rect = pygame.Rect(WIDTH - 40, 10, 15, HEIGHT - 20)
        self.wall_left = self.width - 40
        self.wall_right = self.wall_left + 15
        self.wall_top = 10
        self.wall_bottom = self.height - 10

    def step(self, up_pressed, down_pressed, space_pressed):
        """
        Steps the game logic forward by one tick.
        """
        # Game Logic Updates
        if self.game_state.is_playing:
            # Paddle movement
            if up_pressed:
                self.paddle.move_up(boundary_top=10)
            if down_pressed:
                self.paddle.move_down(boundary_bottom=self.height - 10)

            # Ball movement
            self.ball.move()

            # Collision: Top and Bottom boundary lines
            if self.ball.y - self.ball.radius < 10:
                self.ball.y = 10 + self.ball.radius
                self.ball.dy *= -1
            elif self.ball.y + self.ball.radius > self.height - 10:
                self.ball.y = self.height - 10 - self.ball.radius
                self.ball.dy *= -1

            # Collision: Right Wall
            if self.ball.x + self.ball.radius > self.wall_left:
                if self.wall_top <= self.ball.y <= self.wall_bottom:
                    self.ball.x = self.wall_left - self.ball.radius
                    self.ball.dx *= -1

            # Collision: Left Paddle
            if self.ball.dx < 0:  # Ball moving left
                # Simple AABB collision check between Ball's bounding box and Paddle
                if (self.ball.left < self.paddle.right and 
                        self.ball.right > self.paddle.left and 
                        self.ball.top < self.paddle.bottom and 
                        self.ball.bottom > self.paddle.top):
                    self.ball.x = self.paddle.right + self.ball.radius
                    self.ball.dx *= -1
                    self.game_state.increment_score()

            # Miss: ball goes off-screen left
            if self.ball.x - self.ball.radius < 0:
                self.game_state.end_game()
        else:
            # Menu / Game Over State
            if space_pressed:
                self.game_state.start_game()
                self.ball.reset()
