#!/usr/bin/env python3
import random
from Game import Game
import time

dimensions = (10, 10)
env = Game(dimensions)
num_actions = 4

episodes = 20
render_period = 1
render = True

for episode in range(episodes):
    state = env.reset()

    while not env.done:
        # render
        if render and (episode % render_period == 0):
            env.render()
            time.sleep(0.1) #helps view game at normal speed

        # get action
        #action = random.randint(0, num_actions-1)
        action = int(input("action: "))

        # preform action and get new state and rewards
        new_state = env.step(action)


        # update state for next loop
        state = new_state

