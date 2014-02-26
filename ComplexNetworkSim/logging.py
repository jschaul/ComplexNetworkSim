'''
Special agent automatically initialised by the simulation that logs network
states and topologies at every defined timestep.

@author: Joe Schaul <joe.schaul@gmail.com>
'''

import networkx as nx
from SimPy import Simulation as Sim

import utils

class NetworkLogger(Sim.Process):
        
    def __init__(self, sim, directory, logging_interval):
        Sim.Process.__init__(self, sim=sim)
        self.sim = sim
        self.directory = directory
        self.interval = logging_interval
        self.stateTuples = []
        self.stateVectorTuples = []
        self.topology = nx.Graph()
        self.topoTuples = []  
        
    def Run(self):
        while True:
            self.logCurrentState()
            yield Sim.hold, self, self.interval
            
    def logCurrentState(self):
        
        nodes = self.sim.G.nodes(data=True)
        states = [node[1]['agent'].state for node in nodes]
        stateVectors = [node[1]['agent'].stateVector for node in nodes]
        
        #log states
        self.stateTuples.append((self.sim.now(), states))
        self.stateVectorTuples.append((self.sim.now(), stateVectors))

        #log new topology if it changed.
        if not nx.fast_could_be_isomorphic(self.topology, nx.Graph(self.sim.G)):
            self.topology = utils.create_copy_without_data(self.sim.G)
            self.topoTuples.append((self.sim.now(), self.topology))
            

    def logTrialToFiles(self, id): 
        if not self.topoTuples:
            self.topoTuples.append((0, self.topology))
        #write states, topologies, and state vectors to file       
        utils.logAllToFile(self.stateTuples, self.topoTuples, 
                           self.stateVectorTuples, self.directory, id)
        
        
        
        