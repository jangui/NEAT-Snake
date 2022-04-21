import random
import numpy as np
from collections import deque
from enum import Enum

class NodeType(Enum):
    INPUT = 1
    OUTPUT = 2
    HIDDEN = 3

class Node:
    """ class for a NEAT node """
    def __init__(self, number: int, node_type: NodeType):
        self.value = 0
        self.activated = False
        self.identification = identification
        self.node_type = node_type
        self.in_connections = []
        self.out_connections = []



class Connection:
    """ class for connections between nodes """
    def __init__(self, in_node: Node, out_node: Node, innovation_number: int):
        self.in_node = in_node
        self.out_node = out_node
        self.innovation_number = innovation_number;
        self.weight = random.uniform(-2, 2)
        self.enabled = True

class NEAT:
    def __init__(self, num_agents: int, num_inputs: int, num_outputs: int):
        """ init for neat algorithm """
        self.num_agents = num_agents
        self.connections: dict[int, set[int]] = {}
        self.create_agents(num_inputs, num_outputs)

        # hyperparameters
        self.node_mutation_rate = 0.01
        self.connection_mutation_rate = 0.01
        self.kill_off_rate = 0.5

    def next_generation(self):
        """ take the required steps for advancing a generation """
        self.speciate_agents()
        self.select_fit_agents()
        self.crossover()
        self.mutate()

    def create_agents(self, num_inputs: int, num_outputs: int):
        """ create original agents """
        self.agents: list[Agents] = []
        for i in range(self.num_agents):
            agent = Agent(num_inputs, num_outputs)
            agent.mutate()
            self.agents.append()

    def speciate_agents(self):
        """ seperate agents into species """
        self.species: list[list[Agents]] = []

        for agent in agents:
            new_specie = True
            # check if agent is part of an existing specie
            for specie in species:
                if agent.is_same_species(specie[0]):
                    specie.append(agent)
                    new_specie = False
                    break

            # if agent does not belong to any specie, create new
            if new_specie:
                species.append([ agent ])

    def select_fit_agents(self):
        """ select the fittest agents from each species """
        fit_species: list[list[Agents]] = []
        fit_agents = []
        for specie in self.species:
            specie.sort(key=lambda agent: agent.fitness)
            fittest_agents = specie[:len(specie)//2]
            fit_species.append(fittest_agents)
            git_agents += fittest_agents
        self.species = fit_species
        self.agents = fit_agents

    def mutate(self):
        """ mutate agents based on mutation rates """
        for agent in agents:
            if random.random() > self.node_mutation_rate:
                agent.add_node(self.connections)
            if random.random() > self.connection_mutation_rate:
                agent.add_connection(self.connections)

    def crossover(self):
        """ cross over agents from same species """
        for specie in self.species:
            new_agents = []
            for i in range(1, len(specie)):
                agent = specie[i]
                prev_agent = specie[i-1]
                new_agent = prev_agent.crossover(agent)
                new_agents.append(new_agent)
            specie += new_agents

class Agent:
    """ class for a neat agent """
    def __init__(self, num_inputs: int, num_outputs: int):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.input_nodes = self.create_input_nodes(num_inputs)
        self.output_nodes = self.create_output_nodes(num_inputs, num_outputs)
        self.nodes = self.input_nodes + self.output_nodes
        self.connections = []
        self.fitness = 0

    def get_action(self, state):
        """ get an action from the agent given a current game state """
        node_queue = deque()
        # set input nodes value and add their connected nodes to a node queue
        for i in range(len(self.input_nodes)):
            node = self.input_nodes[i]
            node.value = state[i]
            for connection in node.out_connections:
                node_queue.append(connection.in_node)

        # process nodes in queue
        self.process_nodes(node_queue)

        # select index of output node with largest value
        action = np.argmax(self.output_nodes)

        # reset nodes
        for node in self.nodes:
            node.activated = False

        return action

    def process_nodes(self, node_queue: deque[Node]):
        """ forward propate and process nodes breath first """
        if len(node_queue) == 0:
            return node_queue

        # get current node
        node = node_queue.popleft()

        # check if already processed
        if node.activated:
            return process_nodes(node_queue)

        # get nodes value
        total_value = 0
        for connection in node.in_connections:
            total_value += connection.weight * connection.in_node.value

        node.value = node.activation(total_value)
        node.activated = True

        # add nodes outward connections to node queue
        for connection in node.out_connections:
            node_queue.append(connection.in_node)

        return self.process_nodes(node_queue)

    def create_input_nodes(self, num_inputs: int) -> [Node]:
        """ create input nodes """
        nodes = []
        for i in range(1, num_inputs+1):
            nodes.append(Node(i, NodeType.INPUT))
        return nodes

    def create_output_nodes(self, num_inputs: int, num_outputs: int) -> [Node]:
        """ create output nodes """
        nodes = []
        for i in range(1, num_outputs+1):
            nodes.append(Node(i+num_inputs, NodeType.INPUT))
        return nodes

    def mutate(self):
        """ mutate agent. either add node or connection """
        if random.random() > 0.5:
            self.add_connection()
        else:
            self.add_node()

    def add_connection(self,connections: dict[int, set[int]]):
        """ add a connection between two existing nodes """

        return True

    def add_node(self):
        """ add a node between two already connected nodes """

        # check for existing connection
        existing_connection = None
        for connection in inNode.inConnections:
            if connection.outNode.identification == outNode.identification:
                existing_connection = connection

        # fail to add node between nodes that aren't connected
        if not existing_connection:
            return False

        # create new node
        new_node_id = len(self.nodes)+1
        new_node = Node(new_node_id, NodeType.HIDDEN)
        self.nodes.append(new_node)

        # disable old connection
        existing_connection.enabled = False

        # add in connection
        innovation_number = len(self.connections) + 1
        inConnection = Connection(newNode, outNode, innovation_number)
        inConnection.weight = 1
        new_node.inConnections.append(inConnection)
        out_node.outConnections.append(inConnection)

        # add out connection
        innovation_number += 1
        outConnection = Connection(newNode, outNode, innovation_number)
        outConnection.weight = 1
        new_node.outConnections.append(outConnection)
        inNode.inConnections.append(outConnection)


