'''
Module for the generation of visualisations of processes over complex networks
Generates PNG images for each timestep and (if ImageMagick is available) a gif animation file.

@author: Joe Schaul <joe.schaul@gmail.com>
'''

import utils
from matplotlib import pyplot
import networkx as nx
import os    
#dependency: ImageMagick for gif creation. Works without too then only creates PNGs
    
class AnimationCreator(object):
    
    def __init__(self, dir, name, title, mapping, trial=0, delay=100):
        self.name = name
        self.dir = os.path.abspath(dir)
        self.delay = delay
        self.mapping = mapping
        self.trial = trial
        self.title = title
        self.G = nx.Graph()
    
    def create_gif(self, verbose=True):
        if verbose: print "Creating PNGs ...",
        self.createPNGs()        
        
        input = os.path.join(self.dir, self.name + "*.png")
        output = os.path.join(self.dir, self.name + ".gif")
        
        if verbose: print "attempting gif creation ...",
        
        failure = os.system("convert -delay %i -loop 0 \"%s\" \"%s\"" % (self.delay, input, output))
        if failure:
            print "Problem: Could not create gif. \nMaybe ImageMagick not installed correctly, or its 'convert' executable is not on your system path? \nPNG Image files are generated in any case." 
        else:
            print "success! \nAnimation at %s " % str(output)
            
            
    def createPNGs(self):        
        
        states, topos, vector = utils.retrieveTrial(self.dir, self.trial)
                     
        init_topo = topos[0][1]
        if topos[0][0] != 0:
            print "problem - first topology not starting at 0!"
        self.G = init_topo
        self.layout = nx.layout.fruchterman_reingold_layout(self.G)
        self.nodesToDraw = self.G.nodes()
        self.edgesToDraw = self.G.edges()
        self.nodesToDraw.sort()
        self.edgesToDraw.sort()
        i = 1 
        j = 0
        
        
        pyplot.figure()
        for t, s in states:
            
            # start with initial topology, and check the topology tuples
            # each time to make sure to have an up-to-date graph topology
            if len(topos) > i and t == topos[i][0]:                
                self.G = topos[i][1]
                fixednodes = [node for node in self.nodesToDraw if node in self.G.nodes()]                
                self.layout = nx.layout.fruchterman_reingold_layout(self.G, pos=self.layout, fixed=fixednodes)
                i += 1
                
            #convert states to colours and draw a figure
            colours = utils.states_to_colourString(s, self.mapping)            
            pyplot.clf()
            self.nodesToDraw = self.G.nodes()
            self.nodesToDraw.sort()
            self.edgesToDraw = self.G.edges()
            self.edgesToDraw.sort()
        
            nx.draw_networkx_nodes(self.G, nodelist=self.nodesToDraw, pos=self.layout, node_color=colours, with_labels=False)
            nx.draw_networkx_edges(self.G, edgelist=self.edgesToDraw, pos=self.layout, with_labels=False)
            
            pyplot.suptitle("%s\ntime = %i" % (self.title, t))
            pyplot.axis('off')
            
            pyplot.savefig(os.path.join(self.dir, self.name + "%02d.png" % j))
            j += 1
            
            