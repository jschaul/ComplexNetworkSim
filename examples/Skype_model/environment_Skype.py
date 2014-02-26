'''Environment Agent for Skype-like system.

Simulates different types of sudden crash behaviour.
@author: Joe Schaul <joe.schaul@gmail.com>
'''

from ComplexNetworkSim import NetworkAgent, Sim

            
class crash(NetworkAgent):
    
    def __init__(self, state, initialiser):
        NetworkAgent.__init__(self, 0, initialiser)
        
    def Run(self):
        while True:
            yield Sim.hold, self, 10.0
            if self.sim.now() == 10.0:
                self.killSomeNodes()
            
    def killSomeNodes(self):
        for node in range(self.globalSharedParameters['kills']):
            self.getAgent(node).deactivate_permanently()  