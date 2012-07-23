#!/usr/bin/python
#The class to connect the game with the random number generator and the control

from ai import AI
import random

class BrainConnection():
    def __init__(self):
        self.ai = AI(realtimeMode=True)
        random.seed(self.ai.getRandomness())
        self.lastValue = self.ai.getNeuralResult()
        self.directionValue = 50

        #while True:
        #    print self.getDirection()

    #we get a directional vector between 0 and 100 which is influenced by the 
    #returned values from the brain interface
    def getDirection(self):
        currentValue = self.ai.getNeuralResult()
        if currentValue == self.lastValue:
            return self.directionValue

        if self.lastValue > currentValue:
            if self.directionValue != 100:
                self.directionValue += 10
        else:
            if self.directionValue != 0:
                self.directionValue -= 10
        self.lastValue = currentValue
        return self.directionValue


    #returns entropy data depending on the analogue converted data from the brain interface
    def getRandomness(self,randrange):
        return random.randrange(randrange)


if __name__ == '__main__':
    bc = BrainConnection()
