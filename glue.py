#!/usr/bin/python
#The class to connect the game with the random number generator and the control

from ai import AI

class BrainConnection():
    def __init__(self):
        self.ai = AI(realtimeMode=True)

    #we get a directional vector between 0 and 100 which is influenced by the 
    #returned values from the brain interface
    def getDirection():
        print "Hi"

    #returns entropy data depending on the analogue converted data from the brain interface
    def getRandomness():
        print "Not Implemented"

if __name__ == '__main__':
    bc = BrainConnection()
