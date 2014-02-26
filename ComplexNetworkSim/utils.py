'''
Module with a range of utility methods, such as storing and retrieving states
and topologies. 

@author: Joe Schaul <joe.schaul@gmail.com>
'''

from cPickle import Pickler, Unpickler
import os 
import glob
import networkx as nx

from customexceptions import *

PYTHON_PICKLE_EXTENSION = ".pickled"
TOPO = "_topology"
STATE = "_states"
STATEVECTOR = "_statevectors"
BASE = os.sep + "log_trial_"


def states_to_colourString(states, mapping=None):
    '''
    takes a list of states (integers) and a mapping, e.g.
    
    mapping = { 0 : "g",
                1 : "r",
                2 : "k"}
                
    Returns a list of colours to use in animation. Assumes matplotlib style
    colour strings. Defaults to black ("k") if state not found in mapping, and
    defaults to all nodes being black if no mapping defined.
    '''
    return [mapping.get(state, "k") for state in states]

          
            
#def create_copy_without_data(G):
#    """Return a copy of the graph G with all of the data
#    removed.
#    """
#    H=G.__class__()
#    H.name='graphOnlyOf '+G.name
#    H.add_nodes_from(G.nodes())
#    H.add_edges_from(G.edges())
#    
#    return H

def create_copy_without_data(G):
    """Return a copy of the graph G with all of the data
    removed. More efficient than above.
    """
    H = nx.Graph(G)
    for i in H.nodes_iter():
        H.node[i] = {} 
    return H
                
    
def makeFileNameState(dir, id):
    return dir + BASE + str(id) + STATE + PYTHON_PICKLE_EXTENSION
def makeFileNameStateVector(dir, id):
    return dir + BASE + str(id) + STATEVECTOR + PYTHON_PICKLE_EXTENSION
def makeFileNameTopo(dir, id):
    return dir + BASE + str(id) + TOPO + PYTHON_PICKLE_EXTENSION
    
def retrieveTrial(directory, trial_number):
    ''' For a specific trial in a given directory, retrieve states, topologies
    and statevectors.
    '''    
    states = retrieve(makeFileNameState(directory, trial_number))
    topos = retrieve(makeFileNameTopo(directory, trial_number))
    stateVectors = retrieve(makeFileNameStateVector(directory, trial_number))
    return states, topos, stateVectors

def retrieveAllTrialsInDirectory(directory):
    '''Retrieves all trials in a directory '''
    file_list = glob.glob(os.path.join(directory, "*" + PYTHON_PICKLE_EXTENSION))
    states = []
    stateVectors = []
    topos = []
    for f in file_list:
        if TOPO in f:
            topos.append(f)
        elif STATE in f:
            states.append(f)
        elif STATEVECTOR in f:
            stateVectors.append(f)
                

    state_list = [retrieve(f) for f in states]
    topo_list = [retrieve(f) for f in topos]
    stateVector_list = [retrieve(f) for f in stateVectors]
    
    return (state_list, topo_list, stateVector_list)  

def logAllToFile(stateTuples, topoTuples, stateVectorTuples, directory, trial_id):
    '''Store states, topologies and statevectors to pickled files'''
    logToFile(stateTuples, makeFileNameState(directory, str(trial_id)))
    logToFile(topoTuples, makeFileNameTopo(directory, str(trial_id)))
    logToFile(stateVectorTuples, makeFileNameStateVector(directory, str(trial_id)))
            
                
            
def logToFile(stuff, filename, verbose=True):   
    ''' Store one item (e.g. state list or networkx graph) to file. '''
    filename = os.path.normcase(filename)   
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
            os.makedirs(directory)
       
    f = open(filename, 'wb')
    p = Pickler(f, protocol=2)
    p.dump(stuff)
    f.close()
    if verbose:
        total = len(stuff)
        print "Written %i items to pickled binary file: %s" % (total, filename) 
    return filename
    
    
def retrieve(filename): 
    ''' Retrieve a pickled object (e.g. state list or networkx graph) from file
    '''
    filename = os.path.normcase(filename)  
    try:      
        f = open(filename, 'rb')   
        u = Unpickler(f)
        stuff = u.load()
        f.close()
        return stuff
    except IOError:
        raise LogOpeningError("No file found for %s" % filename, filename)


