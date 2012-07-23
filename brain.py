#!/usr/bin/python
#2012 Bartholomaeus Dedersen
#A brain
#Interface for the ZEO Sleep Thingy to give a 
#simple object interface for a game controller
#Honourable mention: http://zeorawdata.sourceforge.net

from ZeoRawData import BaseLink, Parser
import pprint
import optparse
import csv
import os.path
from decimal import *

def DEBUG(msg):
    if 'options' in locals():
        if(options.debugMode):
            print msg



class Brain():
    def __init__(self,verbose=False,outputFile=False,simMode=False,csvData=False,debug=False):
#Object variables for initialisation
        self.verbose = verbose
        self.outputFile = outputFile
        self.debug = debug
        if csvData:
            csvData = self.meanSavedData(csvData)
            pprint.pprint(csvData)
            self.printGraph(csvData)
        if not simMode:
            #self.link = BaseLink.BaseLink('/dev/ttyUSB0')
            self.link = BaseLink.BaseLink('/dev/ttyO2')
            self.parser = Parser.Parser()
            self.link.addCallback(self.parser.update)
            self.parser.addEventCallback(self.updateEvent)
            self.parser.addSliceCallback(self.updateSlice)
            self.link.start()



#slices arrive every second and carry all important data, mostly
    def updateSlice(self, slice):
        self.sqi = slice['SQI']

        f = slice['FrequencyBins']
        self.bins = [f['2-4'],f['4-8'],f['8-13'],f['11-14'],f['13-18'],f['18-21'],f['30-50']]


        if self.outputFile:
            binWriter = csv.writer(open(self.outputFile, 'ab'))
            if len(slice['FrequencyBins'].values()) == 7:
                f = slice['FrequencyBins']
                bins = [f['2-4'],f['4-8'],f['8-13'],f['11-14'],f['13-18'],f['18-21'],f['30-50']]
                binWriter.writerow(bins)

#debugging params normally not needed but for bugfixing
        if self.debug:
            print "----------------------------"
            print "ZeoTimestamp: " + str(slice['ZeoTimestamp'])
            print "Version: " + str(slice['Version'])

            if not slice['SQI'] == None:
                print "SQI: " + str(slice['SQI'])
            else: print "SQI NOT AVILABLE!"

            if not slice['Impedance'] == None:
                print "Impendance: " +  str(int(slice['Impedance']))
            else:
                print "Impendance unknown"

            if slice['BadSignal']:
                print "BAD SIGNAL DETECTED"
            else:
                print "Good Signal"

            if not slice['Waveform'] == []:
                pprint.pprint(slice['Waveform'])

#print out the fractions of waves
        if self.verbose:
            if len(slice['FrequencyBins'].values()) == 7:
                f = slice['FrequencyBins']
                bins = [f['2-4'],f['4-8'],f['8-13'],f['11-14'],f['13-18'],f['18-21'],f['30-50']]
                for bin in bins:
                    print bin,
                print ""

#timestamps carry important data, seldomly
    def updateEvent(self, timestamp, timestamp_subsec, version, event):
        if self.debug:
            print "New Event with timestamp :" + str(timestamp)
            print "Version: " + str(version)
            print "Event: " + event

#get the mean of a whole dataset
    def meanSavedData(self, csvFile):
        if not os.path.exists(csvFile):
            print "File for CSV parsing does not exist!"
            return
        with open(csvFile, 'rb') as f:
            reader = csv.reader(f)
            valuesRead = 0
            values = [0] * 7
            for row in reader:
                i = 0
                for cell in row:
                    if i == 6:
                        e6Value = Decimal(cell) * 100
                        values[i] += long(e6Value)
                        DEBUG("new line")
                        DEBUG("values read: ")
                        DEBUG(valuesRead)
                        valuesRead += 1
                        i = 0
                    else:
                        DEBUG("reading")
                        e6Value = Decimal(cell) * 100
                        values[i] += long(e6Value)
                        i += 1
            for p in range(0,6):
                DEBUG(" values read: ")
                DEBUG(valuesRead)
#get mean of all values
                values[p] /= valuesRead
            return values

#some graphical magic to visualize data
    def printGraph(self, csvData):
        from pylab import *
        # make a square figure and axes
        figure(1, figsize=(8,8))
        ax = axes([0.1, 0.1, 0.8, 0.8])

        labels = '$Delta$', '$Theta$', '$Alpha$', '$Beta_1$', '$Beta_2$', '$Beta_3$'

        explode=(0, 0, 0, 0, 0, 0)
        del csvData[-1]
        pie(csvData, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        title('', bbox={'facecolor':'0.8', 'pad':5})

        show()



if __name__ == '__main__':

    #parse command line
    parser = optparse.OptionParser(
     usage = "%prog [options]",
     description = "Brain interface for efhagame",
     epilog = """ Just a small class to encapsulate the ZEO Raw Data library for proper access to control the protagonist in efhagame.
            """)

    parser.add_option("-v", "--verbose",
        dest = "verbose",
        action = "store_true",
        help = "be more verbose",
        default = False)

    parser.add_option("-s", "--sim",
        dest = "simMode",
        action = "store_true",
        help = "simulation mode - no real device needed on ttyUSB0",
        default = False)

    parser.add_option("-d", "--debug",
        dest = "debug",
        action = "store_true",
        help = "view all debug messages",
        default = False)

    parser.add_option("-o", "--output",
    action="store",
    type="string",
    help = "put all output bins to FILE",
    metavar="FILE",
    dest="outputFile")

    parser.add_option("-r", "--readCSV",
    action="store",
    type="string",
    help = "read CSV data from file with seven values per row",
    metavar="FILE",
    dest="csvData")


    (options, args) = parser.parse_args()


    brain = Brain(options.verbose, options.outputFile, options.simMode, options.csvData, options.debug)
    if not options.simMode:
        while True:
            i =+ 1
