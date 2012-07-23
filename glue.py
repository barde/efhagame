#!/usr/bin/python
#The class to connect the game with the random number generator and the control

from ai import AI
import random

class BrainConnection():
    def __init__(self):
        self.ai = AI(realtimeMode=True)
        random.seed(self.ai.getRandomness())
        self.getRandomness()

    #we get a directional vector between 0 and 100 which is influenced by the 
    #returned values from the brain interface
    def getDirection():
        print "Hi"

    #returns entropy data depending on the analogue converted data from the brain interface
    def getRandomness(self):
        print random.random()

if __name__ == '__main__':
    bc = BrainConnection()
