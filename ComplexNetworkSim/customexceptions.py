'''
Custom exceptions when handling files to be more precise about the error
that occurred. 

@author: Joe Schaul <joe.schaul@gmail.com>
'''

class LogOpeningError(Exception):   
    """Error happening when trying to open multiple simulation logs"""
    
    
    def __init__(self, value, logs):
        self.value = value
        self.logs = logs
        
    def __str__(self):
        return repr(self.value)
    
    
        