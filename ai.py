#!/usr/bin/python
#2012 Bartholomaeus Dedersen
#An AI 
#Takes a seven element array with procentual amount of various
#brain wave patterns and returns a random number depending on
#training from expected outputs

from pybrain import *
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
import os.path
import optparse
import time
import csv
from decimal import *
from pylab import *
import numpy

from brain import Brain

def DEBUG(msg):
    if 'options' in locals():
        if(options.debugMode):
            print msg

class AI():
    def __init__(self,inputFile=False,trainMode=False,realtimeMode=False,loadNeuralNetwork=False):
    #Object variables for initialisation
        self.inputFile = inputFile
        self.trainMode = trainMode
        self.realtimeMode = realtimeMode
        self.loadNeuralNetwork = loadNeuralNetwork



        self.neuralNet = FeedForwardNetwork()
        inLayer = LinearLayer(7)
        hiddenLayer = SigmoidLayer(5)
        outLayer = LinearLayer(1)

        self.neuralNet.addInputModule(inLayer)
        self.neuralNet.addModule(hiddenLayer)
        self.neuralNet.addOutputModule(outLayer)

        self.neuralNet.addConnection(FullConnection(inLayer,hiddenLayer))
        self.neuralNet.addConnection(FullConnection(hiddenLayer,outLayer))

        self.neuralNet.sortModules()

        DEBUG("Neural Network:")
        DEBUG(self.neuralNet)
        DEBUG("--------")


        if self.loadNeuralNetwork:
            self.neuralNet = NetworkReader.readFrom('lastNetwork.xml')

        if self.inputFile:
            if not os.path.exists(inputFile):
                print "File for CSV parsing does not exist!"
                return
            savedData = self.readCSVData(self.inputFile)

#train upon the given data
            if self.trainMode:
                ds = self.makeTrainingSet(savedData)
                for inpt,target in ds:
                    DEBUG("Input Values from training:")
                    DEBUG(inpt)
                    DEBUG("Correction factor from training:")
                    DEBUG(target)
                trainer = BackpropTrainer(self.neuralNet,ds,verbose=True)
                trainer.trainUntilConvergence(maxEpochs=10)
                self.printGraph(ds)
                NetworkWriter.writeToFile(self.neuralNet, "lastNetwork.xml")

#read the saved data and use it in the network
            for line in savedData:
                DEBUG("Used Data: ")
                DEBUG(line)
                result = self.neuralNet.activate(line)
                DEBUG(result)
            DEBUG("Final weigths:")
            DEBUG(self.neuralNet.params)

#now fun begins. this is the standard mode this module runs in.
        if self.realtimeMode:
            print "We should start now!"
            self.brain = Brain()
            if os.path.isfile("lastNetwork.xml"):
                while True:
                    lines = self.brain.getBins()
                    print(lines)
            else:
#we do a realtime training of the neural network
                print "No trained network exists!"
                time.sleep(1)
                print "Will do on-line training!"
                time.sleep(1)
                print "Hold tight for 10 seconds"

                tempBinWriter = csv.writer(open("temp.csv", 'ab'))

                for i in range (1,10):
                    time.sleep(1)
                    bins = self.brain.getBins()
                    print bins
                    tempBinWriter.writerow(bins)


                tempSavedData = self.readCSVData("temp.csv")

                ds = self.makeTrainingSet(tempSavedData)
                trainer = BackpropTrainer(self.neuralNet,ds,verbose=True)
                trainer.trainUntilConvergence(maxEpochs=10)

    def getRandomness(self):
        if self.realtimeMode:
            bins = self.brain.getBins()
            rand = 1
            for i in range(7):
                rand *= bins[i] * 100
        return rand

    def getNeuralResult(self):
        return self.neuralNet.activate(self.brain.getBins())




    def makeTrainingSet(self,savedData):
#init a dataset with seven input and one output value
        ds = SupervisedDataSet(7,1)
        meanValue = self.getMeanValue(savedData)
        correctionFactor = 0
        for line in savedData:
#intelligent changing value for training a neural network
            correctionFactor += (line[0] - meanValue[0]) * 3
            correctionFactor += (line[1] - meanValue[1]) * 2
            correctionFactor += (line[2] - meanValue[2])
            correctionFactor += (meanValue[3] - line[3])
            correctionFactor += (meanValue[4] - line[4]) * 2
            correctionFactor += (meanValue[5] - line[5]) * 3
            correctionFactor += (meanValue[6] - line[6]) * 6
            DEBUG("Correction Factor:")
            DEBUG(correctionFactor)
#copy values of current line for comparision
            ds.addSample(line,correctionFactor)
            correctionFactor = 0
        return ds

    def getMeanValue(self,savedData):
        meanValues = [0] * 7
        lines = 0
        for line in savedData:
            lines += 1
            valuePosition = 0
            for value in line:
                meanValues[valuePosition] += value
                valuePosition += 1
        for i in range(7):
            meanValues[i] /= lines
        return meanValues

    def printGraph(self, dataSet):

        i = numpy.arange(0, len(dataSet['target']), 1)
        wavePercentage = dataSet['input'][i]
        correctionFactor = dataSet['target'][i]

        ax = plt.subplot(111)

        plt.plot(i, wavePercentage)
        plt.plot(i, correctionFactor + 0.15, c=cm.summer(0), linewidth=2)
        xlabel(r"Number of Data Samples", fontsize=20) 

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(('$Delta$ ', '$Theta$', '$Alpha$', '$Beta_1$', '$Beta_2$', '$Beta_3$', '$Gamma$', '$Target$'),loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)


        show()



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

    parser.add_option("-t", "--train",
        dest = "trainMode",
        action = "store_true",
        help = "train the network",
        default = False)

    parser.add_option("-r", "--realtime",
        dest = "realtimeMode",
        action = "store_true",
        help = "draws realtime outputs from brain wave measurment interface",
        default = False)

    parser.add_option("-n", "--network",
        dest = "loadNeuralNetwork",
        action = "store_true",
        help = "load trained neural network from last training",
        default = False)


    parser.add_option("-i", "--input",
    action="store",
    type="string",
    help = "load a CSV file as input",
    metavar="FILE",
    dest="inputFile")

    (options, args) = parser.parse_args()
    ai = AI(options.inputFile,options.trainMode,options.realtimeMode,options.loadNeuralNetwork)
