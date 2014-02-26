'''
Simulation support for agents in a complex network.
    
Can run multiple fresh trials with the same input parameters. Writes system
state evolution to file (states & network topologies). Supports addition and
deletion of edges and nodes during simulation

@author: Joe Schaul <joe.schaul@gmail.com>
'''

import os
from SimPy import Simulation as Sim
import networkx as nx

from logging import NetworkLogger
        
class NetworkSimulation(Sim.Simulation):
    """Simulation support for agents in a complex network.
    
    Can run multiple fresh trials with the same input parameters. Writes system
    state evolution to file (states & network topologies) Supports
    addition/deletion of edges and nodes during simulation
    
    Parameters
    ----------
    
    topology: a networkx graph 
    
    states: a list of initial states corresponding to the nodes in the topology
    
    agentClass: the class of agent being activated on each node
            
    directory_name: path to where output should be stored. It is recommended to
    have a different directory per simulation.
    
    maxTime : how long the simulation should run
    
    Optional parameters
    -------------------
    
    no_trials: the number of individual simulation trials 
    
    environmentAgent: the class of agent operating on the network topology
    globally, e.g. by changing the structure externally.
    
    globalSharedParameters: dictionary of additional parameters shared globally
    
    """
    def __init__(self, topology, states, agentClass,
                 directory_name, maxTime, no_trials=3,
                 environmentAgent=None, **globalSharedParameters):
        
        Sim.Simulation.__init__(self)
        
        self.G = nx.convert.convert_to_undirected(topology)
        self.initial_topology = self.G.copy()
        self.id_counter = len(topology.nodes()) 
        self.agentClass = agentClass
        self.no_trials = no_trials
        self.until = maxTime
        self.initial_states = states
        self.directory_name = os.path.abspath(directory_name)        
        self.environmentAgent = environmentAgent
        self.globalSharedParameters = globalSharedParameters
        
    def runSimulation(self):
        print "Starting simulations..."
        
        for i in range(self.no_trials):
            print "---Trial " + str(i) + " ---"
            self.runTrial(i)
            
        print "Simulation completed. "
            
    def runTrial(self, id):
        self.initialize() #Sim.Simulation initialisation
        
        #initialise class variables (that are shared between agents)
        #freshly for each trial (as they may change during simulation)
        self.G = self.initial_topology.copy()
        self.params = self.globalSharedParameters.copy()
        
        print "set up agents..."
        #set up agents
        for i in self.G.nodes():
            agent = self.agentClass(self.initial_states[i], (i, self, self.G, self.params))
            self.G.node[i]['agent'] = agent
            self.activate(agent, agent.Run())            
        
        #set up environment agent
        if self.environmentAgent:
            environment = self.environmentAgent(0, ("env", self, self.G, self.params))
            self.activate(environment, environment.Run(), prior=True)
        
        #set up logging
        logging_interval = 1
        logger = NetworkLogger(self, self.directory_name, logging_interval)
        self.activate(logger, logger.Run(), prior=True)
        
        #run simulation trial
        self.simulate(self.until)
        
        #output to Files
        logger.logTrialToFiles(id)
        
    
    def addNewNode(self, state, agentClass=None):
        """Add new node to network and activate an agent on it"""
        
        if not agentClass:
            agentClass = self.agentClass
        agent = agentClass(state, (self.id_counter, self, self.G, self.params))
        self.G.add_node(self.id_counter, {'agent': agent})
        self.activate(agent, agent.Run())
        self.id_counter += 1
        return self.id_counter - 1
        