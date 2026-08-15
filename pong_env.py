import numpy as np
import gymnasium as gym
from gymnasium import spaces
from game_engine import PongEngine

class PongEnv(gym.Env):
    def __init__(self, width=800, height=600):
        super().__init__()
        self.width = width
        self.height = height
        self.total_hits = 0
        
        # Action space: 0 = UP, 1 = DOWN, 2 = STAY
        self.action_space = spaces.Discrete(3)

        # Observation space (normalized)-
        # 1. ball_pos_y
        # 2. ball_pos_x
        # 3. ball_velocity_x
        # 4. ball_velocity_y
        # 5. paddle_y
        self.observation_space = spaces.Box(
            low=np.array([-1.0, -1.0, -1.0, -1.0, -1.0], dtype=np.float32),
            high=np.array([1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32),
            dtype=np.float32
        )
        self.engine = None

    def _get_obs(self):
        obs = np.array([
            2 * (self.engine.ball.y - self.height * 0.5) / self.height,
            2 * (self.engine.ball.x - self.width * 0.5) / self.width,
            self.engine.ball.dx / 20.0,
            self.engine.ball.dy / 20.0,
            2 * (self.engine.paddle.y - self.height * 0.5) / self.height
        ], dtype=np.float32)
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.total_hits = 0
        
        self.engine = PongEngine(self.width, self.height)
        
        observation = self._get_obs()
        return observation

    def step(self, action):
        up_pressed = (action == 0)
        down_pressed = (action == 1)
        
        reward = self.engine.step(up_pressed=up_pressed, down_pressed=down_pressed)
        
        observation = self._get_obs()
        terminated = False

        if reward > 0:
            self.total_hits += 1
        elif self.engine.game_lost:
            terminated = True

        truncated = False
            
        return observation, reward, terminated, truncated, self.total_hits
