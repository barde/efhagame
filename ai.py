#!/usr/bin/python
#2012 Bartholomaeus Dedersen
#An AI 
#Takes a seven element array with procentual amount of various
#brain wave patterns and returns a random number depending on
#training from expected outputs

from pybrain import *
import optparse

def DEBUG(msg):
    if(options.debugMode):
        print msg

class AI():
    def __init__(self,inputFile=False):
#Object variables for initialisation
        self.verbose = verbose

        if self.inputFile:
            if not os.path.exists(inputFile):
                print "File for CSV parsing does not exist!"
                return
            savedData = readCSVData(self.inputFile)
            


    def readCSVData(inputFile):
            lines = sum(1 for line in open(inputFile))
            with open(inputFile, 'rb') as f:
                reader = csv.reader(f)
                valuesRead = 0
                values = zeros(lines,7)
                j = 0
                for row in reader:
                    i = 0
                    for cell in row:
                        if i == 6:
                            e6Value = Decimal(cell) * 100
                            values[j][i] = long(e6Value)
                            DEBUG("new line")
                            DEBUG("values read: ")
                            DEBUG(valuesRead)
                            valuesRead += 1
                            i = 0
                        else:
                            DEBUG("reading")
                            e6Value = Decimal(cell) * 100
                            values[j][i] = long(e6Value)
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
    parser.add_option("-v", "--verbose",
        dest = "verbose",
        action = "store_true",
        help = "be more verbose",
        default = False)

    parser.add_option("-i", "--input",
    action="store",
    type="string",
    help = "load a CSV file as input",
    metavar="FILE",
    dest="inputFile")

    (options, args) = parser.parse_args()
    ai = AI(options.verbose,options.inputFile)
