'''An implementation of an agent following the simple SIR model

@author: Joe Schaul <joe.schaul@gmail.com>
'''

from ComplexNetworkSim import NetworkAgent, Sim

#states:
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

class SIRSimple(NetworkAgent):
    """ an implementation of an agent following the simple SIR model """
    INFECTION_PROB = 0.5 
    TIME = 1.0
        
    def __init__(self, state, initialiser):
        NetworkAgent.__init__(self, state, initialiser)
        self.infection_probability = self.globalSharedParameters['infection_rate']
        self.infection_end = eval(self.globalSharedParameters['inf_dur'])
        
    def Run(self):
        while True:
            if self.state == SUSCEPTIBLE:
                self.maybeBecomeInfected()
                yield Sim.hold, self, NetworkAgent.TIMESTEP_DEFAULT #wait a step
            elif self.state == INFECTED:
                yield Sim.hold, self, self.infection_end  #wait end of infection     
                self.state = RECOVERED
                yield Sim.passivate, self #remove agent from event queue
                
    def maybeBecomeInfected(self):
        infected_neighbours = self.getNeighbouringAgentsIter(state=INFECTED)
        for neighbour in infected_neighbours:
            if SIRSimple.r.random() < self.infection_probability:
                self.state = INFECTED
                break
        
        
        
        
        
        
        
        
        
                    
            