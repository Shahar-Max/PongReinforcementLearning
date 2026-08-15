import os
import sys
import argparse
import numpy as np

from pong_env import PongEnv
from dqn_agent import DQNAgent
from pong_renderer import PongRenderer

def run_agent(episodes, model_path, learn=True, render=False, lr=1e-3, target_update=1000):
    env = PongEnv()
    agent = DQNAgent(
        state_dim=5, 
        action_dim=3, 
        lr=lr, 
        target_update_freq=target_update
    )
    
    if os.path.exists(model_path):
        try:
            agent.load(model_path)
        except Exception as e:
            print(f"Error loading model weights: {e}")
            if not learn:
                return
    elif not learn:
        print(f"Error: Model file {model_path} does not exist. Cannot play without a trained model.")
        return

    renderer = None
    if render:
        renderer = PongRenderer(width=env.width, height=env.height, caption="Pong - AI Agent")

    total_steps = 0

    if learn:
        print(f"Starting training for {episodes} episodes...")
    else:
        print("Starting agent evaluation. Close window or press ESC to exit.")

    for episode in range(1, episodes + 1):
        state = env.reset()
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, terminated, truncated, score = env.step(action)
            done = terminated or truncated

            if learn:
                agent.train_step(state, action, reward, next_state, done)

            state = next_state
            total_steps += 1

            if renderer is not None:
                renderer.render(env.engine, "Cumulative Score", env.total_hits)
                renderer.tick(60)

            if learn and score > 50: # prevent deadlocks caused by good agents or over-rewarding in easy circumstances
                done = True
                
        if learn:
            print(f"Episode {episode} | Steps: {total_steps} | Score: {score} ")
            if episode % 10 == 0:
                agent.save(model_path)
        else:
            print(f"Game Over! Agent scored: {score}")
            
    if learn:
        agent.save(model_path)
        print("Training finished!")
        
    if renderer is not None:
        renderer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--train", action="store_true")
    group.add_argument("--play", action="store_true")

    parser.add_argument("--model-path", type=str, default="dqn_pong.pth")
    parser.add_argument("--episodes", type=int, default=5000)
    
    args = parser.parse_args()
        
    if args.train:
        run_agent(episodes=args.episodes, model_path=args.model_path, learn=True, render=False)
    elif args.play:
        run_agent(episodes=1, model_path=args.model_path, learn=False, render=True)
