class GameState:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.is_playing = False
        self.is_game_over = False

    def increment_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

    def start_game(self):
        self.score = 0
        self.is_playing = True
        self.is_game_over = False

    def end_game(self):
        self.is_playing = False
        self.is_game_over = True
