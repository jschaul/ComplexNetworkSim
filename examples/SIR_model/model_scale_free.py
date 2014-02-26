'''Example model specification for SIR over a scale-free network. 

@author: Joe Schaul <joe.schaul@gmail.com>
'''
import networkx as nx

from ComplexNetworkSim import NetworkSimulation, AnimationCreator, PlotCreator
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
    globalSharedParameters['inf_dur'] = "self.r.gauss(7, 2)"
    
    # Output Parameters    
    statesToMonitor = [INFECTED, SUSCEPTIBLE, RECOVERED]
    colours = ["r", "--g", ":k"]
    mapping = {SUSCEPTIBLE:"w", INFECTED:"r", RECOVERED:"0.4"}
    labels = ["Infected", "Susceptible", "Recovered"]
    name = "SIR_scale_free"
    titlePlot = "Simulation on scale free graph, %i trials, %i%% infection prob" \
                    % (TRIALS, 100 * globalSharedParameters['infection_rate'])
    titleVisual = ""   
    
    # Network
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

    # run visualisation    
    gif = AnimationCreator(directory, name, titleVisual, mapping)
    gif.create_gif()

    # plot results
    p = PlotCreator(directory, name, titlePlot, statesToMonitor, 
                    colours, labels) 
    p.plotSimulation()

if __name__ == '__main__':
    main()
