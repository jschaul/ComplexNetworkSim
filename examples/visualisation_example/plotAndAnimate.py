'''
Example module for running plotting and/or animations
on simulation files generated from a previous simulation.
Copy/change code to fit your own simulations.
@author: Joe Schaul <joe.schaul@gmail.com>
'''
from ComplexNetworkSim import AnimationCreator, PlotCreator

#states:
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

def main():
    
    #directory containing simulation output files (relative or absolute path)
    directory = 'exampleSimulation'
    filenames = "SIR"    
    plotStates = True #set to False if you only want the visualisation  
    animate = True #set to False if you only want the plotting
    
    # Parameters for plotting of system states  
    # define those states you wish to appear on the plot,
    # along with their colour and label
    statesToMonitor = [INFECTED, SUSCEPTIBLE]
    colours = ["r", "g"]
    labels = ["Infected", "Susceptible"]
    titlePlot = "Simulation of agent-based simple SIR"
    
    # Parameters for animated visualisations
    # define a mapping from state to colour
    # define the specific trial you wish to visualise. Default=0, first trial
    mapping = {SUSCEPTIBLE:"w", INFECTED:"r", RECOVERED:"0.4"}
    titleVisual = "Simulation of agent-based simple SIR"    
    trialToVisualise = 0

    if animate: #run visualisation  
        visualiser = AnimationCreator(directory, filenames, titleVisual, mapping, trial=trialToVisualise)
        visualiser.create_gif(verbose=True)
    
    if plotStates: #plot results
        p = PlotCreator(directory, filenames, titlePlot, statesToMonitor, colours, labels)   
        p.plotSimulation(show=False)

if __name__ == '__main__':
    main()