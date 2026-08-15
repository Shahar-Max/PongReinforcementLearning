import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

def create_dqn_model(state_dim=5, action_dim=3):
    model = nn.Sequential(
        nn.Linear(state_dim, 64),
        nn.ReLU(),
        nn.Linear(64, 64),
        nn.ReLU(),
        nn.Linear(64, action_dim)
    )

    return model

class DQNAgent:
    def __init__(self, state_dim=5, action_dim=3, lr=1e-3, gamma=0.99, target_update_freq=1000):
        self.action_dim = action_dim
        self.gamma = gamma
        self.target_update_freq = target_update_freq
        
        self.policy_net = create_dqn_model(state_dim, action_dim)
        self.target_net = create_dqn_model(state_dim, action_dim)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.steps_done = 0

    def select_action(self, state):
        state_input = np.expand_dims(state, axis=0)
        state_t = torch.tensor(state_input, dtype=torch.float32)
        with torch.no_grad():
            q_values = self.policy_net(state_t)
        return np.argmax(q_values[0].numpy())

    def train_step(self, state, action, reward, next_state, done):
        states_t = torch.tensor(np.expand_dims(state, axis=0), dtype=torch.float32)
        next_states_t = torch.tensor(np.expand_dims(next_state, axis=0), dtype=torch.float32)

        with torch.no_grad():
            next_q_values = self.target_net(next_states_t)
            max_next_q_val = torch.max(next_q_values).item()

        target_q_val = reward + self.gamma * max_next_q_val if not done else 0
        target_q_t = torch.tensor([target_q_val], dtype=torch.float32)

        self.optimizer.zero_grad()
        
        q_values = self.policy_net(states_t)

        current_q_t = q_values[0, action]
        
        loss = torch.mean((target_q_t - current_q_t) ** 2)
        
        loss.backward()
        self.optimizer.step()
        
        self.steps_done += 1
        if self.steps_done % self.target_update_freq == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
            
        return loss.item()

    def save(self, filepath):
        torch.save(self.policy_net.state_dict(), filepath)
        print(f"Model saved to {filepath}")

    def load(self, filepath):
        self.policy_net.load_state_dict(torch.load(filepath))
        self.target_net.load_state_dict(self.policy_net.state_dict())
        print(f"Model loaded from {filepath}")
