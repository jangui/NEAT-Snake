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
        self.in_connections: set[int] = {}
        self.out_connections: set[int] = {}

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
        self.connections: dict[int, dict[int, int]] = {}
        self.create_agents(num_inputs, num_outputs)
        self.current_innovation = 0

        # hyperparameters
        self.node_mutation_rate = 0.01
        self.connection_mutation_rate = 0.01
        self.kill_off_rate = 0.5

    def next_generation(self):
        """ take the required steps for advancing a generation """
        self.speciate_agents()
        self.select_fit_agents()
        #self.crossover()
        self.mutate()

    def create_agents(self, num_inputs: int, num_outputs: int):
        """ create original agents """
        self.agents: list[Agents] = []

        for i in range(self.num_agents):
            agent = Agent(num_inputs, num_outputs)

            # give agent a random mutation
            if random.random() > 0.5:
                self.innovation_number = agent.add_connection(self.connections, self.innovation_number)
            else:
                agent.add_node(self.connections)

            self.agents.append()

    def speciate_agents(self):
        """ seperate agents into species """
        self.species: list[list[Agents]] = []

        for agent in agents:
            new_specie = True
            # check if agent is part of an existing specie
            for specie in species:
                representative_specie = specie[0]
                speciation_difference = agent.speciate_difference(representative_specie)
                if speciation_difference < self.speciation_threshold:
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

    def mutate(self, current_innovation):
        """ mutate agents based on mutation rates """
        for agent in agents:
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


    def add_connection(self, connections: dict[int, set[int]], current_innovation: int) -> int:
        """ add a connection between two existing nodes """
        # select two nodes
        in_node, out_node = self.get_two_random_nodes()

        # check if they already have an existing connection
        while in_node.identifier in out_node.out_connections:
            # reselect nodes until non connected nodes
            in_node, out_node = self.get_two_random_nodes()


        # get innovation number
        innovation_number = self.get_innovation_number(connections, in_node, out_node, current_innovation)

        # set the innovation number for this connection
        connections[out_node.identifer][in_node.identifier] = innovation_number

        # create connection
        connection = Connection(in_node, out_node, innovation_number)
        self.connections.append(connection)
        return innovation_number

    def get_innovation_number(self, connections: list[Connection], in_node: Node, out_node: Node, current_innovation: int) -> int:
        """ get the innovation number for the connection between out node and in node """
        out_node_connections = connections[out_node.identifier]

        # check if connection exists
        if in_node.identifier in out_node_connections.keys():
            innovation_number = out_node_connections[in_node.identifier]
            return innovation_number

        # if connection doesnt exist, then new innovation!
        return current_innovation + 1

    def get_two_random_nodes(self) -> (Node, Node):
        """ select two random nodes """
        node1_index = random.randint(0, len(self.nodes))
        node2_index = random.randin(0, len(self.nodes))
        while node2_index == node1_index:
            node2_index = random.randin(0, len(self.nodes))
        node1 = self.nodes[node1_index]
        node2 = self.nodes[node2_index]
        return (node1, node2)

    def add_node(self, connections: list[Connection], current_innovation: int):
        """
        add a node between two already connected nodes
        disbale the existing connection and add two new connections to and from the new node
        """
        # randomly select and existing connection
        existing_connection_index = random.randint(0, len(self.connections))
        existing_connection = self.connections[existing_connection_index]

        # disable connection
        existing_connection.enabled = False

        # get nodes from existing connection
        in_node = existing_connection.in_node
        out_node = existing_connection.out_node

        # create new node
        node_id = len(self.nodes) + 1
        new_node = Node(node_id, NodeType.HIDDEN)

        # create new connection to new node from original out node
        innovation_number = self.get_innovation_number(connections, new_node, out_node, current_innovation)
        to_connection = Connection(new_node, out_node, innovation_number)
        to_connection.weight = 1 # implementation detail from original NEAT paper
        self.connections.append(to_connection)

        # create new connection from new node into original in node
        innovation_number = self.get_innovation_number(connections, in_node, new_node, current_innovation)
        from_connection = Connection(new_node, out_node, innovation_number)
        from_connection.weight = existing_connection.weight # implementation detail from original NEAT paper
        self.connections.append(from_connection)

    def speciation_difference(self, other_agent: Agent, speciation_weights: list[int]) -> bool:
        """ get the speciation difference between the other agent and this one """
        # get the max number of genes between the two species
        maximum_genes = max(len(self.connections), len(other_agent.connections))

        # get the total excess genes
        last_innovation = self.connections[-1].innovation_number
        other_agent_last_innovation = other_agent[-1].innovation_number
        excess_genes = abs(last_innovation - other_agent_last_innovation)

        # get the agent without excess genes
        non_excess_agent = self
        excess_agent = other_agent
        if excess_genes == other_agent_last_innovation:
            non_excess_agent = other_agent
            excess_agent = self

        # get the disjoin and weight difference between genes
        disjoint_genes = 0
        joint_genes = 0
        joint_genes_weight_diff = 0
        for i in range(len(non_excess_agent.connections)):
            agent1_connection = non_excess_agent.connections[i]
            agent2_connection = excess_agent.connections[i]

            if agent1_connection.innovation_number == agent2_connection.innovaton_number:
                difference = agent1_connection.innovation_number - agent2_connection.innovation_number
                joint_genes_weight_diff += abs(difference)
                joint_genes += 1
            else:
                disjoint_genes += 1

        # calculate speciation difference
        joint_genes_avg_weight_diff = joint_genes_weight_diff / joint_genes
        c1, c2, c3 = speciation_weights
        excess_genes_difference =
        speciation_difference = (((c1*excess_genes) + (c2*disjoint_genes)) / maximum_genes ) + c3*joint_genes_avg_weight_diff
        return speciation_difference



