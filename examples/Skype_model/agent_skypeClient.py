'''Implementation of a Skype-like Peer-2-Peer network agent

@author: Joe Schaul <joe.schaul@gmail.com>
'''

from ComplexNetworkSim import NetworkAgent, Sim

#states:
DISABLED = 0
ENABLED = 1
ENABLED_S = 2
DISABLED_S = 3
DEAD = 4

#type:
NODE = 0
SUPERNODE = 1


class Skype(NetworkAgent):
    """ agent behaviour for Skype-like Peer-2-Peer network simulation"""

    #class constants (shared between all instances)
    TIME = 1.0    
        
    
    def __init__(self, state, initialiser):
        NetworkAgent.__init__(self, state, initialiser)
        self.threshold = self.globalSharedParameters['threshold']
        self.currentSupernodeID = -1
        self.connected = False
        #note the "eval(" - parameter has to be a string of executable Python code        
        self.restartTime = eval(self.globalSharedParameters['restart_time'])        
        self.knownSupernodes = []
        self.knownSupernodesDistribute = []
        self.supers = []        
        self.connections = 0
        
        
    def Run(self):        
        self.setInitialNodeType()
        while True:           
            
            #regular node behaviour
            if self.nodeType == NODE:
                if not self.connected or self.getAgent(self.currentSupernodeID).state >= DISABLED_S:
                    self.state = DISABLED
                    self.reconnect()                    
                
            #supernode behaviour            
            elif self.nodeType == SUPERNODE:      
                if self.state == DEAD:
                    yield Sim.passivate, self
                     
                if not self.knownSupernodes:   
                    self.computeKnownSupernodes()
                  
                if self.tooManyConnections() or self.state==DISABLED_S:
                    self.deactivate()
                    yield Sim.hold, self, self.restartTime
                    self.state = ENABLED_S
                else:
                    pass

            #in any case:
            yield Sim.hold, self, NetworkAgent.TIMESTEP_DEFAULT       

    def computeKnownSupernodes(self):#        
        self.knownSupernodes = self.globalSharedParameters['supernodes']        
        self.knownSupernodesDistribute = self.knownSupernodes[:] #a copy
        
    def deactivate(self):
        self.state = DISABLED_S
        self.connections = 0
        
    def deactivate_permanently(self):
        self.deactivate()
        self.state = DEAD


    def reconnect(self):
        
        if self.connected:
            self.globalTopology.remove_edge(self.id, self.currentSupernodeID)
            self.connected = False
         
        if self.supers:      
            self.currentSupernodeID = Skype.r.choice(self.supers)
            
            superagent = self.getAgent(self.currentSupernodeID)
            if superagent.state == ENABLED_S:
                superagent.connections += 1
                if superagent.connections > self.globalSharedParameters['threshold']:
                    superagent.deactivate()
                                
                self.globalTopology.add_edge(self.id, self.currentSupernodeID)
                self.state = ENABLED
                self.connected = True
        else:            
            self.queryNode(self.globalSharedParameters['permanent_supernodes'][0])        
        
    
    def queryNode(self, id):
        i = 0
        while i < self.globalSharedParameters['cache_size']:
            agent = self.getAgent(id)
            if agent.state >= DISABLED_S:
                return
            if agent.knownSupernodesDistribute:
                self.supers.append(agent.knownSupernodesDistribute.pop())
            else:
                self.r.shuffle(agent.knownSupernodes)
                agent.knownSupernodesDistribute = agent.knownSupernodes[:] #a copy
                self.supers.append(agent.knownSupernodesDistribute.pop())
            i += 1        
        
    def setInitialNodeType(self):
                            
        if len(self.getNeighbouringNodes()) > 2:
            self.nodeType = SUPERNODE
            self.state = ENABLED_S
        else:
            self.nodeType = NODE    
                       
    def tooManyConnections(self):
        ''' return true if node has too many connections,
        false otherwise'''
        return len(self.getNeighbouringNodes()) > \
               (self.globalSharedParameters['threshold'] + len(self.knownSupernodes))            