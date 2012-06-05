#!/usr/bin/python
#2012 Bartholomaeus Dedersen
#An AI 
#Takes a seven element array with procentual amount of various
#brain wave patterns and returns a random number depending on
#training from expected outputs

from pybrain import *
import os.path
import optparse
import csv
import numpy
import pprint
from decimal import *

def DEBUG(msg):
    if(options.debugMode):
        print msg

class AI():
    def __init__(self,inputFile=False):
    #Object variables for initialisation
        self.inputFile = inputFile

        if self.inputFile:
            if not os.path.exists(inputFile):
                print "File for CSV parsing does not exist!"
                return
            savedData = self.readCSVData(self.inputFile)


        self.neuralNet = FeedForwardNetwork()
        inLayer = LinearLayer(7)
        hiddenLayer = SigmoidLayer(5)
        outLayer = LinearLayer(1)

        neuralNet.addInputModule(inLayer)
        neuralNet.addModule(hiddenLayer)
        neuralNet.addOutputModule(outLayer)

        neuralNet.addConnection(FullConnection(inLayer,hiddenLayer))
        neuralNet.addConnection(FullConnection(hiddenLayer,outLayer))

        neuralNet.sortModule()

        DEBUG(pprint(neuralNet))


    def readCSVData(self,inputFile):
            lines = sum(1 for line in open(inputFile))
            with open(inputFile, 'rb') as f:
                reader = csv.reader(f)
                valuesRead = 0
#init the multidimensional array
                values = numpy.zeros((lines,7))
                j = 0
                for row in reader:
                    i = 0
                    for cell in row:
                        if i == 6:
                            values[j][i] = Decimal(cell)
                            valuesRead += 1
                            i = 0
                        else:
                            values[j][i] = Decimal(cell)
                            i += 1
                    j += 1

            DEBUG(pprint.pprint(values))


            return values


if __name__ == '__main__':

    #parse command line
    parser = optparse.OptionParser(
     usage = "%prog [options]",
     description = "Neural Network for generating randomness depending on user's brain activity",
     epilog = """ Best used in combination with the default loadout of libraries in the original project
            """)
    parser.add_option("-d", "--debug",
        dest = "debugMode",
        action = "store_true",
        help = "show debug messages",
        default = False)

    parser.add_option("-i", "--input",
    action="store",
    type="string",
    help = "load a CSV file as input",
    metavar="FILE",
    dest="inputFile")

    (options, args) = parser.parse_args()
    ai = AI(options.inputFile)
