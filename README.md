# Pong Reinforcement Learning
Basic reinforcement learning testing-field

A small-scale machine learning experiment using a simple task of Pong,
with the goal being to grasp the basic concepts of reinforcement learning.

The task itself is relatively easy to replace by switching the environment.
Another goal of the project is to evaluate the effectiveness of this approach when 
handling tasks that are more convoluted and in other domains,
as well as to further test other algorithms and approaches.

The current model (although trained with limited hardware) 
manages to score 189.8 on average, with the testing environment capping scores at 1000 to prevent deadlocks.
It reaches the maximum score in roughly 17% of the games, 
which accounts for the majority of the score-sum.

Play using the trained model:
python modelControlledMain.py --play

Train the model (or a new one by deleting the current one and or specifying --model-path):
python modelControlledMain.py --train

This mvp version deliberately avoids epsilon exploration & decay/a replay buffer/gpu utilization/parallelization 
for the sake of simplicity, although some features significantly improved performance when tested.

The main inputs are ball coordinates (x, y), paddle coordinates (y), and ball velocity (vertical and horizontal).

The reward is only granted upon a ball hit or a ball miss, purposely avoiding more straightforward rewards such
as a reward for moving closer to the ball, as such simple heuristics simplify the problem too much and may not 
be easily transferrable to other domains.


