#!/usr/bin/env python3
import random
import time

from Game import Game
from NEAT import NEAT

dimensions = (10, 10)
env = Game(dimensions)
num_actions = 4

agents = 100
inputs = dimensions[0] * dimensions[1]
outputs = num_actions
neat = NEAT(agents, inputs, outputs)

generations = 10000
render_period = 1
render = True

for generation in range(generations):
    print(f"### GENERATION {generation} ###")

    # each agent plays a full game
    for i, agent in enumerate(neat.agents):

        # game loop
        state = env.reset()
        while not env.done:
            # get action
            action = agent.get_action(state.flatten(), neat.connections)
            #action = random.randint(0, num_actions-1)
            #action = int(input("action: "))

            # preform action and get new state and rewards
            new_state = env.step(action)

            # update state for next loop
            state = new_state

        agent.fitness = env.points

    neat.next_generation()

    # print data on species
    for i, specie in enumerate(neat.species):
        print(f'specie #{i} size: {len(specie)}')
    print(f'agents: {len(neat.agents)}')

    # showcase best agent every 50 gens
    if generation % 50 == 0:
        # select fittest agent
        max_fitness = -1
        fittest_agent = None
        for agent in neat.agents:
            if agent.fitness > max_fitness:
                max_fitness = agent.fitness
                fittest_agent = agent
        print(f"Best Score: {max_fitness}")

        # showcase fittest agent playing game
        state = env.reset()
        env.render()
        while not env.done:
            env.render()
            time.sleep(0.1) #helps view game at normal speed
            action = fittest_agent.get_action(state.flatten(), neat.connections)
            new_state = env.step(action)
            state = new_state

