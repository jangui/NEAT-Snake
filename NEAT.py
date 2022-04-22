import random
import numpy as np
from collections import deque
from enum import Enum

import copy

class NodeType(Enum):
    INPUT = 1
    OUTPUT = 2
    HIDDEN = 3

class Node:
    """ class for a NEAT node """
    def __init__(self, identification: int, node_type: NodeType):
        self.value = 0
        self.activated = False
        self.id = identification
        self.node_type = node_type
        self.in_connections: set[int] = set()
        self.out_connections: set[int] = set()

    def activation(self, value: int) -> int:
        return 1 / (1 + np.exp(-value))

class Connection:
    """ class for connections between nodes """
    def __init__(self, in_node: Node, out_node: Node, innovation_number: int):
        self.in_node = in_node
        self.out_node = out_node
        self.innovation_number = innovation_number;
        self.weight = random.uniform(-2, 2)
        self.enabled = True

class Agent:
    """ class for a neat agent """
    def __init__(self, num_inputs: int, num_outputs: int):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.nodes: dict[int, Node] = {}
        self.create_initial_nodes(num_inputs, num_outputs)
        self.connections: dict[int, Connection] = {}
        self.fitness = 0

    def get_action(self, state, neat_connections: dict[int, dict[int, int]]):
        """ get an action from the agent given a current game state """
        node_queue = deque()

        # ith input = ith input node value
        for i in range(0, self.num_inputs):
            node = self.nodes[i+1] # node id's start at 1, not 0
            node.value = state[i]

            # add nodes current node is connected to into queue
            for in_node_id in node.out_connections:
                in_node = self.nodes[in_node_id]
                node_queue.append(in_node)

        # process nodes in queue
        self.process_nodes(node_queue, neat_connections)

        # select index of output node with largest value
        action = max(range(len(self.output_nodes)), key=lambda i: self.output_nodes[i].value)

        # reset nodes
        for node_id, node in self.nodes.items():
            node.activated = False

        return action

    def process_nodes(self, node_queue: deque[Node], neat_connections: dict[int, dict[int,int]]):
        """ forward propate and process nodes breath first """
        if len(node_queue) == 0:
            return node_queue

        # get current node
        node = node_queue.popleft()

        # check if already processed
        if node.activated:
            return self.process_nodes(node_queue, neat_connections)

        # get nodes value
        total_value = 0
        for out_node_id in node.in_connections:
            connection_id = neat_connections[out_node_id][node.id]
            connection = self.connections[connection_id]
            total_value += connection.weight * connection.in_node.value

        node.value = node.activation(total_value)
        node.activated = True

        # add nodes current node is connected to into queue
        for in_node_id in node.out_connections:
            in_node = self.nodes[in_node_id]
            if not in_node.activated:
                node_queue.append(in_node)

        return self.process_nodes(node_queue, neat_connections)

    def create_initial_nodes(self, num_inputs: int, num_outputs: int):
        """ create input and output nodes """
        self.output_nodes = []
        for i in range(1, num_inputs+1):
            self.nodes[i] = Node(i, NodeType.INPUT)
        for i in range(1, num_outputs+1):
            output_node = Node(i+num_inputs, NodeType.OUTPUT)
            self.nodes[i+num_inputs] = output_node
            self.output_nodes.append(output_node)

    def add_connection(self, neat_connections: dict[int, dict[int, dict[int,int]]], current_innovation: int) -> int:
        """ add a connection between two existing nodes """
        # select two nodes
        in_node, out_node = self.get_two_random_nodes()

        # check if they already have an existing connection
        while in_node.id in out_node.out_connections:
            # reselect nodes until non connected nodes
            in_node, out_node = self.get_two_random_nodes()

        # get innovation number
        current_innovation, innovation_number = self.update_innovations(in_node, out_node, neat_connections, current_innovation)

        # create connection
        connection = Connection(in_node, out_node, innovation_number)
        self.connections[innovation_number] = connection
        self.add_node_connections(in_node, out_node)
        return current_innovation

    def update_innovations(self, in_node: Node, out_node: Node, neat_connections: dict[int, dict[int,int]], current_innovation: int) -> int:
        """ updates global neat connections and returns the lastest innovation number and innovation number for this connection"""

        # get innovation number
        innovation_number = self.get_innovation_number(neat_connections, in_node, out_node, current_innovation)

        # update innovation if new innovation
        if innovation_number > current_innovation:
            current_innovation = innovation_number

            # add new innovation to neat connections
            if out_node.id not in neat_connections:
                neat_connections[out_node.id] = {in_node.id: innovation_number}
            else:
                neat_connections[out_node.id][in_node.id] = innovation_number

        return current_innovation, innovation_number

    def get_innovation_number(self, neat_connections: list[Connection], in_node: Node, out_node: Node, current_innovation: int) -> int:
        """ get the innovation number for the connection between out node and in node """
        # check if connection exists
        if out_node.id in neat_connections:
            out_node_connections = neat_connections[out_node.id]
            if in_node.id in out_node_connections.keys():
                innovation_number = out_node_connections[in_node.id]
                return innovation_number

        # if connection doesnt exist, then new innovation!
        return current_innovation + 1

    def get_two_random_nodes(self) -> (Node, Node):
        """ select two random nodes """
        node1_id = random.choice(list(self.nodes))
        node2_id = random.choice(list(self.nodes))
        while node2_id == node1_id:
            node2_id = random.choice(list(self.nodes))
        node1 = self.nodes[node1_id]
        node2 = self.nodes[node2_id]
        return (node1, node2)

    def add_node(self, neat_connections: list[Connection], current_innovation: int):
        """
        add a node between two already connected nodes
        disbale the existing connection and add two new connections to and from the new node
        """
        # if no connections, get random nodes
        if len(self.connections) == 0:
            in_node, out_node = self.get_two_random_nodes()
            from_connection_weight = random.uniform(-2, 2)
            to_connection_weight = random.uniform(-2, 2)
        else: # existing connections
            # randomly select and existing connection
            existing_connection_id = random.choice(list(self.connections))
            existing_connection = self.connections[existing_connection_id]
            # reselect connection if its disabled
            while not existing_connection.enabled:
                existing_connection_id = random.choice(list(self.connections))
                existing_connection = self.connections[existing_connection_id]

            from_connection_weight = existing_connection.weight
            to_connection_weight = 1

            # disable connection
            existing_connection.enabled = False

            # get nodes from existing connection
            in_node = existing_connection.in_node
            out_node = existing_connection.out_node

            # remove connection info from nodes
            self.remove_node_connections(in_node, out_node)

        # create new node
        node_id = len(self.nodes) + 1
        new_node = Node(node_id, NodeType.HIDDEN)
        self.nodes[node_id] = new_node

        # create new connection to new node from original out node
        current_innovation, innovation_number = self.update_innovations(new_node, out_node, neat_connections, current_innovation)
        to_connection = Connection(new_node, out_node, innovation_number)
        to_connection.weight = to_connection_weight
        self.connections[innovation_number] = to_connection
        self.add_node_connections(new_node, out_node)

        # create new connection from new node into original in node
        current_innovation, innovation_number = self.update_innovations(in_node, new_node, neat_connections, current_innovation)
        from_connection = Connection(in_node, new_node, innovation_number)
        from_connection.weight = from_connection_weight
        self.connections[innovation_number] = from_connection
        self.add_node_connections(in_node, new_node)

        return current_innovation

    def add_node_connections(self, in_node: Node, out_node: Node):
        in_node.in_connections.add(out_node.id)
        out_node.out_connections.add(in_node.id)

    def remove_node_connections(self, in_node: Node, out_node: Node):
        in_node.in_connections.remove(out_node.id)
        out_node.out_connections.remove(in_node.id)

    def get_newest_innovation(self) -> int:
        """ get the number of new innovation the agent has made """
        newest_innovation = 0
        for innovation_num in self.connections:
            newest_innovation = max(innovation_num, newest_innovation)
        return newest_innovation

    def speciation_difference(self, other_agent: 'Agent', speciation_threshold, speciation_weights: list[int]) -> bool:
        """ get the speciation difference between the other agent and this one """

        # get the cutoff point for excess and disjoint genes
        newest_innovation = self.get_newest_innovation()
        other_agent_newest_innovation = other_agent.get_newest_innovation()
        innovation_cutoff = max(newest_innovation, other_agent_newest_innovation)

        # calc joint, disjoint and excess genes
        joint_genes = 0
        joint_genes_weight_diff = 0
        disjoint_genes = 0
        excess_genes = 0
        for inno_num, conn in self.connections.items():
            if inno_num in other_agent.connections:
                joint_genes += 1
                joint_genes_weight_diff += abs(conn.weight - other_agent.connections[inno_num].weight)
            else:
                if inno_num > innovation_cutoff:
                    excess_genes += 1
                else:
                    disjoint_genes += 1

        for inno_num, conn in other_agent.connections.items():
            if inno_num not in other_agent.connections:
                if inno_num > innovation_cutoff:
                    excess_genes += 1
                else:
                    disjoint_genes += 1


        # calculate average difference for joint genes
        joint_genes_avg_weight_diff = 0
        if joint_genes:
            joint_genes_avg_weight_diff = joint_genes_weight_diff / joint_genes

        # calculate speciation difference
        most_genes = max(len(self.connections), len(other_agent.connections))
        c1, c2, c3 = speciation_weights
        speciation_difference = (((c1*excess_genes) + (c2*disjoint_genes)) / most_genes ) + c3*joint_genes_avg_weight_diff
        return speciation_difference

class NEAT:
    def __init__(self, num_agents: int, num_inputs: int, num_outputs: int):
        """ init for neat algorithm """
        self.num_agents = num_agents
        self.connections: dict[int, dict[int, int]] = {}
        self.current_innovation = 0
        self.create_agents(num_inputs, num_outputs)
        self.species = []

        # hyperparameters
        self.node_mutation_rate = 0.1
        self.connection_mutation_rate = 0.1
        self.kill_off_rate = 0.5
        self.speciation_weights = [0.7, 1.2, 0.3]
        self.speciation_threshold = 1.35

    def next_generation(self):
        """ take the required steps for advancing a generation """
        self.speciate_agents()
        self.select_fit_agents()
        #self.crossover()
        self.agents = self.agents + copy.deepcopy(self.agents) # TODO cross over instead of this garbage
        if len(self.agents) < 80:
            new_agents = copy.deepcopy(self.agents)
            innovation_number = -1
            for agent in new_agents:
                if random.random() > self.node_mutation_rate:
                    innovation_number = agent.add_node(self.connections, self.current_innovation)
                if random.random() > self.connection_mutation_rate:
                    innovation_number = agent.add_connection(self.connections, self.current_innovation)

                # update innovation number
                if innovation_number > self.current_innovation:
                    self.current_innovation = innovation_number
            self.agents += new_agents

        self.mutate()

    def create_agents(self, num_inputs: int, num_outputs: int):
        """ create original agents """
        self.agents: list[Agents] = []

        for i in range(self.num_agents):
            agent = Agent(num_inputs, num_outputs)

            # give agent a random mutation
            if random.random() > 0.5:
                innovation_num = agent.add_connection(self.connections, self.current_innovation)
            else:
                innovation_num = agent.add_node(self.connections, self.current_innovation)

            # update innovation number
            if innovation_num > self.current_innovation:
                self.current_innovation = innovation_num

            self.agents.append(agent)

    def speciate_agents(self):
        """ seperate agents into species """
        self.species: list[list[Agents]] = []

        for agent in self.agents:
            new_specie = True
            # check if agent is part of an existing specie
            for specie in self.species:
                representative_specie = specie[0]
                speciation_difference = agent.speciation_difference(representative_specie, self.speciation_threshold, self.speciation_weights)
                #print("sp diff:",speciation_difference, self.speciation_threshold) # TODO remove only for debuggin
                if speciation_difference < self.speciation_threshold:
                    specie.append(agent)
                    new_specie = False
                    break

            # if agent does not belong to any specie, create new
            if new_specie:
                self.species.append([ agent ])

    def select_fit_agents(self):
        """ select the fittest agents from each species """
        fit_species: list[list[Agents]] = []
        fit_agents = []
        for specie in self.species:
            specie.sort(key=lambda agent: agent.fitness)
            fittest_agents = specie[:len(specie)//2]
            fit_species.append(fittest_agents)
            fit_agents += fittest_agents
        self.species = fit_species
        self.agents = fit_agents

    def mutate(self):
        """ mutate agents based on mutation rates """
        innovation_number = -1
        for agent in self.agents:
            if random.random() > self.node_mutation_rate:
                innovation_number = agent.add_node(self.connections, self.current_innovation)
            if random.random() > self.connection_mutation_rate:
                innovation_number = agent.add_connection(self.connections, self.current_innovation)

            # update innovation number
            if innovation_number > self.current_innovation:
                self.current_innovation = innovation_number

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




