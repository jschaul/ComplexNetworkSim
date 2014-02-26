'''
Unittests to test correct working of some utils methods

@author: Joe
'''
import unittest
import os

from ComplexNetworkSim import utils

TMP_DIRECTORY = "temp_unittests" 
        
class globalTest(object):       
    
    directory = os.path.abspath(TMP_DIRECTORY)
    
    def __init__(self):
        self.globalSetUp()
         
    def globalSetUp(self):
        if not os.path.exists(globalTest.directory):
            os.makedirs(globalTest.directory)           
    
    def globalTearDown(self):
        files = os.listdir(globalTest.directory)       
        print "Deleting... "  
        for file in files:
            if ("." in file and utils.PYTHON_PICKLE_EXTENSION not in file):
                raise Exception("directory contains non anticipated file.")
            path = globalTest.directory + os.sep + file
            print path
            os.remove(path)
        print "Removal of temporary files done."
    


class TestDump(unittest.TestCase):


    def setUp(self):
        self.directory = globalTest.directory
        self.filename = self.directory + os.sep + "test_log"


    
    def test_dump_multiple(self):
        state1 = [1,2,3,4]
        state2 = [3,5,6,99]
        states = []
        states.append(state1)
        states.append(state2)
        
        
        stateV1 = [[1, 1],[27, 8],[34,3]]
        stateV2 = [[1, 1],[27, 8], [999, 9]]
        statesV = []
        statesV.append(stateV1)
        statesV.append(stateV2)
        
        topo1 = [(1,2), (2,3)]
        topo2 = [(1,4), (5,3)]
        topos = []
        topos.append(topo1)
        topos.append(topo2)
        
        utils.logAllToFile(state1, topo1, stateV1, self.directory, 7)
        utils.logAllToFile(state2, topo2, stateV2, self.directory, 9)
        
        states2, topos2, statesV2 = utils.retrieveAllTrialsInDirectory(self.directory)
        self.assertEqual(states, states2)
        self.assertEqual(statesV, statesV2)
        self.assertEqual(topos, topos2)
        
            
    def test_dump_one(self):
        x = [(1,2), (3,4)]
        utils.logToFile(x, self.filename)
        x2 = utils.retrieve(self.filename)
        self.assertEqual(x, x2)
        
        
       
        
        
        
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
    bla = globalTest()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDump)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    bla.globalTearDown()