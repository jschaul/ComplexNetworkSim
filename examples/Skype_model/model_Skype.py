'''Example model specification for a Skype-like system

@author: Joe Schaul <joe.schaul@gmail.com>
'''
import networkx as nx

from ComplexNetworkSim import NetworkSimulation, AnimationCreator, PlotCreator
from agent_skypeClient import DISABLED, ENABLED, ENABLED_S, DISABLED_S
from agent_skypeClient import Skype 
from environment_Skype import crash 

# Simulation constants    
MAX_SIMULATION_TIME = 50.0
TRIALS = 1

def main():    
    combs = []
    
    combs.append({})    
    combs[0]["nodes"] = 600 
    combs[0]["supernodes"] = 100
    combs[0]["permanent_supernodes"] = 1
    combs[0]['threshold'] = 12
    combs[0]['cache_size'] = 50
    combs[0]['kills'] = 40
    combs[0]['restart_time'] = "self.r.expovariate(1/4.0)"
    combs[0]['restart_time_str'] = "exp"
    combs[0]['agentClass'] = Skype
    combs[0]['environmentAgent'] = crash
    
    combs.append(combs[0].copy())  
    combs[1]['cache_size'] = 3
    
    combs.append(combs[0].copy())  
    combs[2]['kills'] = 60
    
    combs.append(combs[0].copy())  
    combs[3]['kills'] = 60
    combs[3]['cache_size'] = 3
    
#    combs.append(combs[0].copy())  
#    combs[4]['kills'] = 40
#    combs[4]['cache_size'] = 1
#    
#    combs.append(combs[0].copy())  
#    combs[4]['kills'] = 60
#    combs[4]['cache_size'] = 1
    
    fixes = []
    for c in combs:
        fixes.append(c.copy())
    for fix in fixes:
        fix['restart_time'] = "4"
        fix['restart_time_str'] = "fix"
        
    gausses = []
    for c in combs:
        gausses.append(c.copy())
    for gauss in gausses:        
        gauss['restart_time'] = "abs(self.r.gauss(4, 1))"
        gauss['restart_time_str'] = "gauss"
    
    
    parameter_combinations = []    
    parameter_combinations.extend(combs)
    parameter_combinations.extend(fixes)
    parameter_combinations.extend(gausses)
    
    for parameters in parameter_combinations:
        dir = '_'.join(("skype600-", 
                       str(parameters['supernodes']), 
                       str(parameters['restart_time_str']),
                       str(parameters['threshold']),
                       str(parameters['cache_size']),
                       str(parameters['kills']),
                       ))
        parameters['directory'] = dir
        simulate(**parameters)
        

def simulate(**kwargs):        
    
    # Model parameters
    directory = kwargs.get("directory", 'skype')    
    agentClass = kwargs.get("agentClass", Skype)    
    environmentAgent = kwargs.get("environmentAgent", crash)
    NUMBER_SUPERNODES = kwargs.get("supernodes", 90)
    NUMBER_NODES = kwargs.get("nodes", 600)
    NUMBER_PERMANENT_SUPERNODES = kwargs.get("permanent_supernodes", 1)    
    globalSharedParameters = {} 
    globalSharedParameters['supernodes'] = range(NUMBER_SUPERNODES) 
    globalSharedParameters['permanent_supernodes'] = range(NUMBER_PERMANENT_SUPERNODES) 
    globalSharedParameters['threshold'] = kwargs.get("threshold", 12)
    globalSharedParameters['cache_size'] = kwargs.get("cache_size", 20)
    globalSharedParameters['kills'] = kwargs.get("kills", 30)
    globalSharedParameters['restart_time'] = kwargs.get('restart_time', "4.0")
    
    
    # Output Parameters    
    statesToMonitor = [ENABLED, ENABLED_S]
    colours = ["g", "^b", "0.5"]
    mapping = {ENABLED:"g", ENABLED_S: "b", DISABLED:"0.2", DISABLED_S: "0.4"}
    labels = ["Online nodes", "Online supernodes", "Offline"]
    name = "skype"
    titlePlot = "Skype simulation, %i trials, threshold=%i, cacheSize=%i \n supernode_restart_distr=%s" % \
      (TRIALS, globalSharedParameters['threshold'], globalSharedParameters['cache_size'],
       str(globalSharedParameters['restart_time']))
    titleVisual = "Skype visualisation"
    
    
#####topology####
    G = nx.Graph(nx.complete_graph(NUMBER_SUPERNODES))
    G.add_nodes_from(xrange(NUMBER_SUPERNODES,NUMBER_NODES+NUMBER_SUPERNODES))
    
    states = [DISABLED for node in G.nodes_iter()]
    
    
    # run simulation
    simulation = NetworkSimulation(G,
                                   states,
                                   agentClass,
                                   directory,
                                   MAX_SIMULATION_TIME,
                                   TRIALS,
                                   environmentAgent,
                                   **globalSharedParameters)
    simulation.runSimulation()

#    # run visualisation    
#    gif = AnimationCreator(directory, name, titleVisual, mapping)
#    gif.create_gif()

    # plot results
    p = PlotCreator(directory, name, titlePlot, statesToMonitor, 
                    colours, labels) 
    p.plotSimulation()

if __name__ == '__main__':
    main()
