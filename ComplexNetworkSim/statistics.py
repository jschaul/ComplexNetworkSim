'''
Module for basic averaging of system states across multiple trials.
Used in plotting.

@author: Joe Schaul <joe.schaul@gmail.com>
'''

class TrialState(object):

    def __init__(self, trial_id, times, systemStates, uniqueStates, stateCounterForStateX):
        self.trial_id = trial_id
        self.times = times
        self.systemStates = systemStates
        self.uniqueStates = uniqueStates
        self.stateCounterForStateX = stateCounterForStateX
    

class TrialStats(object):

    def __init__(self, allTrialStateTuples, allTrialTopologyTuples):
        self.stateTuples = allTrialStateTuples
        self.topoTuples = allTrialTopologyTuples
        self.trialstates = []
        self.trialAverage = None
        
        self.calculateAllStateCounts()
        self.calculateAverageStateCount()
        
    def calculateAllStateCounts(self):
        
        for trial in range(len(self.stateTuples)):    
            times = [t for (t,s) in self.stateTuples[trial]]
            systemStates = [s for (t,s) in self.stateTuples[trial]]
            uniqueStates = reduce(lambda x, y: set(y).union(set(x)), systemStates)
            stateCounterDict = {}
            for x in uniqueStates:
                stateXCounts = [state.count(x) for state in systemStates]
                stateCounterDict[x] = stateXCounts
            #store info about this trial
            self.trialstates.append(TrialState(trial, times, systemStates, uniqueStates, stateCounterDict))
    
    def calculateAverageStateCount(self):
        times = self.trialstates[0].times
        uniqueStates = self.trialstates[0].uniqueStates
        for trial in self.trialstates:
            try:
                uniqueStates  = set(trial.uniqueStates).union(set(uniqueStates))
            except:
                pass
              
        stateCounterDict = {}
        dummy = [0 for x in trial.systemStates]
        for x in uniqueStates:
            array = [trial.stateCounterForStateX.get(x, dummy) for trial in self.trialstates]
            averages = [sum(value)/len(self.trialstates) for value in zip(*array)]
            stateCounterDict[x] = averages
            
        self.trialAverage = TrialState(-1, times, None, uniqueStates, stateCounterDict)
        
    
    
    