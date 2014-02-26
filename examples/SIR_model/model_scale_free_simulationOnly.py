'''Example model specification for SIR over a scale-free network. 

This module only executes a simulation and no plotting. 
See model_scale_free.py for combined behaviour.

@author: Joe Schaul <joe.schaul@gmail.com>
'''
import networkx as nx

from ComplexNetworkSim import NetworkSimulation
from agent_SIR import INFECTED, RECOVERED, SUSCEPTIBLE
from agent_SIR import SIRSimple as agentClass
from environment_SIR import SIRenvironment as environmentAgent

# Simulation constants    
MAX_SIMULATION_TIME = 25.0
TRIALS = 2 

def main(nodes=30):         
    # Model parameters
    directory = 'test'
    globalSharedParameters = {} 
    globalSharedParameters['infection_rate'] = 0.3
    globalSharedParameters['inf_dur'] = "7"
        
    # Network and initial states
    G = nx.scale_free_graph(nodes)    
    states = [SUSCEPTIBLE for n in G.nodes()]       
    
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

if __name__ == '__main__':
    main()
