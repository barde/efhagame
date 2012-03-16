#!/usr/bin/python
#2012 Bartholomäus Dedersen
#A brain
#Interface for the ZEO Sleep Thingy to give a 
#simple object interface for a game controller
#Honourable mention: http://zeorawdata.sourceforge.net

from ZeoRawData import BaseLink, Parser

class brain():
    def __init__(self):
#Object variables for initialisation
        self.link = Baselink('/dev/ttyUSB0')
        self.parser = Parser()
        self.link.addCallback(parser.updateEvent)
        self.parser.addEventCallback(parser.updateSlice)
        self.link.start()

    def updateSlice(self, slice):
        print "ZeoTimestamp: " + str(slice['ZeoTimestamp'])
        print "Version: " + str(slice['Version'])

        if not slice['SQI'] == None:
            print "SQI: " + str(slice['SQI'])
        else:
            print "SQU NOT AVILABLE!"

        if not slice['Impedance'] == None:
            print "Impendance: " +  str(int(slice['Impedance']))
        else:
            print "Impendance unknown"

        if slice['BadSignal']:
            print "BAD SIGNAL DETECTED"
        else:
            print "Good Signal"

        if not slice['Waveform'] == []:
            print "Waveform: " + (slice['Waveform'])

        if len(slice['FrequencyBins'].values()) == 7:
            f = slice['FrequencyBins']
            bins = [f['2-4'],f['4-8'],f['8-13'],f['11-14'],f['13-18'],f['18-21'],f['30-50']]
            for freq in emumerate(bins):
                print "Bin" + freq  + ": " + bins[i]

    def updateEvent(self, timestamp, version, event):
        print "New Event with timestamp :" + str(timestamp)
        print "Version: " + str(version)
        print "Event: " + event


if __name__ == '__main__':
    while True:
        print "Hi"
    sys.exit(app.exec_())
