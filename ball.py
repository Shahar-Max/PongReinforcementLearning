import random

class Ball:
    def __init__(self, x, y):
        self.radius = 5
        self.reset()

    def reset(self):
        self.x = random.random() * 200 + 200
        self.y = random.random() * 200 + 200
        self.dx = random.random() * 9 + 1
        self.dy = random.random() * 9 + 1

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
