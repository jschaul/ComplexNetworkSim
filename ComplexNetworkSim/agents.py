'''
Module for the NetworkAgent class that can be subclassed by agents.

@author: Joe Schaul <joe.schaul@gmail.com>
'''

from SimPy import Simulation as Sim
import networkx as nx
import random

SEED = 123456789

ADD_EDGE = "add edge"
REMOVE_EDGE = "remove edge"
ADD_NODE = "add node"
REMOVE_NODE = "remove node"


class NetworkAgent(Sim.Process):
    '''NetworkAgent class that can be subclassed by agents. '''
    
    #class variables, shared between all instances of this class
    r = random.Random(SEED)
    TIMESTEP_DEFAULT = 1.0

    def __init__(self, state, initialiser, stateVector=[], name='network_process', **stateParameters):
        Sim.Process.__init__(self, name)
        self.state = state
        self.stateVector = stateVector
        self.stateParameters = stateParameters
        self.initialize(*initialiser)
        
        
    def initialize(self, id, sim, globalTopo, globalParams):
        ''' this gets called automatically '''        
        self.id = id
        self.sim = sim
        self.globalTopology = globalTopo
        self.globalSharedParameters = globalParams
        
    def getAllNodes(self):
        return self.globalTopology.nodes()
    
    def getAllAgents(self, state=None):
        neighs = self.getAllNodes()
        if state is not None:
            return [self.globalTopology.node[n]['agent'] for n in neighs 
                      if self.globalTopology.node[n]['agent'].state == state]
        else:
            return [self.globalTopology.node[n]['agent'] for n in neighs]
        
        
        
    def getNeighbouringAgents(self, state=None):
        ''' returns list of neighbours, but as agents, not nodes.
        so e.g. one can set result[0].state = INFECTED '''
        neighs = self.globalTopology.neighbors(self.id)
        if state is not None:
            return [self.globalTopology.node[n]['agent'] for n in neighs 
                      if self.globalTopology.node[n]['agent'].state == state]
        else:
            return [self.globalTopology.node[n]['agent'] for n in neighs]
        
    def getNeighbouringAgentsIter(self, state=None):
        '''same as getNeighbouringAgents, but returns generator expression, 
        not list.
        '''
        neighs = self.globalTopology.neighbors(self.id)
        if state is not None:
            return (self.globalTopology.node[n]['agent'] for n in neighs 
                      if self.globalTopology.node[n]['agent'].state == state)
        else:
            return (self.globalTopology.node[n]['agent'] for n in neighs)
    
    def getNeighbouringNodes(self):
        ''' returns list of neighbours as nodes. 
        Call self.getAgent() on one of them to get the agent.'''
        return self.globalTopology.neighbors(self.id)
    
    def getAgent(self, id):
        '''returns agent of specified ID.'''   
        return self.globalTopology.node[id]['agent']
        
    def addNewNode(self, state):
        #add & activate new agent
        return self.sim.addNewNode(state) 
        
        #add a random edge
        #u = NetworkAgent.r.choice(self.globalTopology.nodes())
        #self.globalTopology.add_edge(u, id)
        
    def die(self):
        self.removeNode(self.id)        
        
    def removeNode(self, id):
#        cancel ? self.getAgent(id)
        self.globalTopology.remove_node(id)
        
    def removeEdge(self, node1, node2):
        
        self.globalTopology.remove_edge(self.id, self.currentSupernodeID)
        self.logTopoChange(REMOVE_EDGE, node1, node2)
        
        
    def addEdge(self, node1, node2):        
        self.globalTopology.add_edge(self.id, self.currentSupernodeID)
        self.logTopoChange(ADD_EDGE, node1, node2)
        
        
    def logTopoChange(self, action, node, node2=None):
        #TODO: test, add this to netlogger...
        print action, node, node2
        
        
    
    
    
    
    
    
        
        
    