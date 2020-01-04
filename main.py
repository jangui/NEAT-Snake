#!/usr/bin/env python3
import random
from Game import Game
import time

env = Game()
num_actions = env.num_actions

episodes = 20
render_period = 1
render = True

for episode in range(episodes):
    state = env.reset()

    while not env.done:
        action = random.randint(0, num_actions)
        new_state, reward = env.step(action)
        if render and (episode % render_period == 0):
            env.render()
            #time.sleep(0.1) #helps view game at normal speed

        state = new_state

"""
state is a tuple containing the coordinates
of the snake's body and the coordinates of
the food's location
"""
