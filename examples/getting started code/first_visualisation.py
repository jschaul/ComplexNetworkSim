'''
Complete code file only from ComplexNetworkSim's  "getting started" documentation section, for visualising a simulation. For explanations refer to the documentation page.
Current link: http://complexnetworksim.0sites.net/start.html (documentation hosting may change place - see the PyPi index page.)

@author: Joe Schaul <joe.schaul@gmail.com>
'''

from ComplexNetworkSim import PlotCreator, AnimationCreator

directory = 'test' #location of simulation result files    
myName = "SIR" #name that you wish to give your image output files    
title = "Simulation of agent-based simple SIR"

#define three simulation-specific constants:
SUSCEPTIBLE = 0    
INFECTED = 1    
RECOVERED = 2

statesToMonitor = [INFECTED, SUSCEPTIBLE] #even if we have states 0,1,2,3,... plot only 1 and 0
colours = ["r", "g"] #state 1 in red, state 0 in green
labels = ["Infected", "Susceptible"] #state 1 named 'Infected', 0 named 'Susceptible'
mapping = {SUSCEPTIBLE:"w", INFECTED:"r", RECOVERED:"0.4"}
trialToVisualise = 0

p = PlotCreator(directory, myName, title, statesToMonitor, colours, labels)   
p.plotSimulation(show=False) 
#show=True shows the graph directly, 
#otherwise only a png file is created in the directory defined above.

visualiser = AnimationCreator(directory, myName, title, mapping, trial=trialToVisualise)
#gif speed can be changed by giving a parameter 'delay' (default=100) to AnimationCreator
visualiser.create_gif(verbose=True)