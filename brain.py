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



class Brain():
    def __init__(self,verbose=False,outputFile=False,simMode=False):
#Object variables for initialisation
        self.verbose = verbose
        self.outputFile = outputFile
        if not simMode:
            self.link = BaseLink.BaseLink('/dev/ttyUSB0')
            self.parser = Parser.Parser()
            self.link.addCallback(self.parser.update)
            self.parser.addEventCallback(self.updateEvent)
            self.parser.addSliceCallback(self.updateSlice)
            self.link.start()



    def updateSlice(self, slice):
        if self.outputFile:
            binWriter = csv.writer(open(self.outputFile, 'ab'))
            if len(slice['FrequencyBins'].values()) == 7:
                f = slice['FrequencyBins']
                bins = [f['2-4'],f['4-8'],f['8-13'],f['11-14'],f['13-18'],f['18-21'],f['30-50']]
                binWriter.writerow(bins)
        if self.verbose:
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

            if len(slice['FrequencyBins'].values()) == 7:
                f = slice['FrequencyBins']
                bins = [f['2-4'],f['4-8'],f['8-13'],f['11-14'],f['13-18'],f['18-21'],f['30-50']]
                #pprint.pprint(f)
                pprint.pprint(bins)
                #for freq in emumerate(bins):
                #    print "Bin" + freq  + ": " + bins[i]

    def updateEvent(self, timestamp, timestamp_subsec, version, event):
        if self.verbose:
            print "New Event with timestamp :" + str(timestamp)
            print "Version: " + str(version)
            print "Event: " + event

    def meanSavedData(self, csvFile):
        if not os.path.exists(csvFile):
            print "File for CSV parsing does not exist!"
            return
        with open(csvFile, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                print row

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

    parser.add_option("-o", "--output",
    action="store",
    type="string",
    help = "put all output FFT bins to FILE",
    metavar="FILE",
    dest="outputFile")

    (options, args) = parser.parse_args()


    brain = Brain(options.verbose, options.outputFile)
    while True:
        i =+ 1
    sys.exit(app.exec_())
