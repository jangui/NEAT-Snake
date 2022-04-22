
from NEAT import NEAT

agents = 100
inputs = 100
outputs = 4
neat = NEAT(agents, inputs, outputs)

mutations = 2
neat.speciation_weights = [0.7, 1.2, 0.3]
neat.speciation_threshold = 1.35
for i in range(mutations):
    neat.mutate()


neat.speciate_agents()
for i, specie in enumerate(neat.species):
    print(f'specie #{i} size: {len(specie)}')

gens = 10
for i in range(gens):
    neat.next_generation()
    for i, specie in enumerate(neat.species):
        print(f'specie #{i} size: {len(specie)}')
    print(f'agents: {len(neat.agents)}')
"""


for i, agent in enumerate(neat.agents):
    print(f'agent: {i}')
    print('\tNodes:')
    for _, node in agent.nodes.items():
        print(f'\t\t{node.id} {node.node_type} connections:\n\t\t\tin: {node.in_connections}\n\t\t\tout: {node.out_connections}')
    print('\tConnections:')
    for _, connection in agent.connections.items():
        print(f'\t\tenabled: {connection.enabled} out: {connection.out_node.id} in: {connection.in_node.id} inno: {connection.innovation_number}' )


for out_node, in_conns in neat.connections.items():
    print(f'Node: {out_node} Connections:')
    for in_node, inno_num in in_conns.items():
        print(f'\tIn node: {in_node}, inno_num: {inno_num}')
"""
