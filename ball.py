import random

class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.radius = 5
        self.initial_speed_x = speed_x
        self.initial_speed_y = speed_y
        self.reset()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.dx = self.initial_speed_x
        self.dy = self.initial_speed_y * random.choice([-1, 1])

    def move(self):
        self.x += self.dx
        self.y += self.dy

    @property
    def left(self):
        return self.x - self.radius

    @property
    def right(self):
        return self.x + self.radius

    @property
    def top(self):
        return self.y - self.radius

    @property
    def bottom(self):
        return self.y + self.radius
