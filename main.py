#!/usr/bin/env python3
import random
from Game import Game
import time

env = Game()
#num_actions = env.num_actions
num_actions = 4
#observation_space = env.observation_space.shape

episode_rewards = [] #for collecting stats

episodes = 1
render_period = 1
render = True

for episode in range(episodes):
    state = env.reset()
    #episode_reward = 0 #for collecting stats

    while not env.done:
        action = random.randint(0, num_actions)
        new_state, reward = env.step(action)
        if render and (episode % render_period == 0):
            env.render()
            time.sleep(0.1)

        state = new_state
        #episode_reward += reward

"""
    ##### STATS #####
    episode_rewards.append(episode_reward)

    if episode > ro
"""
