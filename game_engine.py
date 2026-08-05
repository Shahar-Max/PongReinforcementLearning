from paddle import Paddle
from ball import Ball

class PongEngine:
    def __init__(self, width=800, height=600):
        self.score = 0
        self.width = width
        self.height = height
        
        # Instantiate Component
        self.paddle = Paddle(30, self.height // 2 - 45, width=15, height=90, speed=8)
        self.ball = Ball(self.width // 2, self.height // 2)
        
        # Define logical boundaries of the right wall
        self.wall_left = self.width - 40
        self.wall_right = self.wall_left + 15
        self.wall_top = 10
        self.wall_bottom = self.height - 10

    def step(self, up_pressed, down_pressed, space_pressed):
        """
        Steps the game logic forward by one tick.
        """
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
                self.score += 1

        # Miss: ball goes off-screen left
        if self.ball.x - self.ball.radius < 0:
            self.score = 0
            self.ball.reset()
