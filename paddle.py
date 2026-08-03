class Paddle:
    def __init__(self, x, y, width=15, height=90, speed=8):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    def move_up(self, boundary_top=0):
        self.y -= self.speed
        if self.y < boundary_top:
            self.y = boundary_top

    def move_down(self, boundary_bottom=600):
        self.y += self.speed
        if self.y + self.height > boundary_bottom:
            self.y = boundary_bottom - self.height
