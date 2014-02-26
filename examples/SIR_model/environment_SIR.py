'''Environment Agent for SIR model: infects random
agent at timestep 7.

@author: Joe Schaul <joe.schaul@gmail.com>
'''
from ComplexNetworkSim import NetworkAgent, Sim
from agent_SIR import INFECTED, SUSCEPTIBLE, RECOVERED

class SIRenvironment(NetworkAgent):
    
    def __init__(self, state, initialiser):
        NetworkAgent.__init__(self, 0, initialiser)
        
    def Run(self):
        while True:
            yield Sim.hold, self, 7.0
            self.infectRandomInitialAgent()
            yield Sim.passivate, self
            

    def infectRandomInitialAgent(self):        
        target = NetworkAgent.r.choice(self.getAllNodes())
        self.getAgent(target).state = INFECTED
        
#    def infectHighestConnectedAgent(self):
#        import networkx
#        topo = networkx.Graph(self.globalTopology)
#        target = max([topo.degree(i) for i in self.getAllNodes()])
#        self.getAgent(target).state = INFECTED
        
        