#!/usr/bin/python
import sys
from pylab import *
import numpy
import csv
import glob
from decimal import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pprint import pprint

datalen = 20

def readCSVData(inputFile):
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

fig = plt.figure(1)

i = numpy.arange(0, datalen, 1)

ax_delta = plt.subplot(111)
divider = make_axes_locatable(ax_delta)

ax_theta = divider.new_horizontal("100%", pad=0.0, sharey=ax_delta)
fig.add_axes(ax_theta)

ax_alpha = divider.new_horizontal("100%", pad=0.0, sharey=ax_delta)
fig.add_axes(ax_alpha)

ax_beta1 = divider.new_horizontal("100%", pad=0.0, sharey=ax_delta)
fig.add_axes(ax_beta1)

ax_beta2 = divider.new_horizontal("100%", pad=0.0, sharey=ax_delta)
fig.add_axes(ax_beta2)

ax_beta3 = divider.new_horizontal("100%", pad=0.0, sharey=ax_delta)
fig.add_axes(ax_beta3)

#
#ax_gamma = divider.new_horizontal("100%", pad=0.0, sharey=ax_delta)
#fig.add_axes(ax_gamma)

for files in glob.glob("*"):
    data = readCSVData(files)
    ax_delta.plot(i, data[:datalen,0])
    ax_theta.plot(i, data[:datalen,1])
    ax_alpha.plot(i, data[:datalen,2])
    ax_beta1.plot(i, data[:datalen,3])
    ax_beta2.plot(i, data[:datalen,4])
    ax_beta3.plot(i, data[:datalen,5])
#    ax_gamma.plot(i, data[:datalen,6])

#xlabel(r"Number of Data Samples", fontsize=20) 

#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#ax.legend(('$Delta$ ', '$Theta$', '$Alpha$', '$Beta_1$', '$Beta_2$', '$Beta_3$', '$Gamma$', '$Target$'),loc='center left', bbox_to_anchor=(1, 0.5),    fancybox=True, shadow=True)

plt.setp(ax_delta.get_xticklabels(), visible=False)
plt.setp(ax_theta.get_xticklabels(), visible=False)
plt.setp(ax_theta.get_yticklabels(), visible=False)
plt.setp(ax_alpha.get_xticklabels(), visible=False)
plt.setp(ax_alpha.get_yticklabels(), visible=False)
plt.setp(ax_beta1.get_xticklabels(), visible=False)
plt.setp(ax_beta1.get_yticklabels(), visible=False)
plt.setp(ax_beta2.get_xticklabels(), visible=False)
plt.setp(ax_beta2.get_yticklabels(), visible=False)
plt.setp(ax_beta3.get_xticklabels(), visible=False)
plt.setp(ax_beta3.get_yticklabels(), visible=False)
#plt.setp(ax_gamma.get_xticklabels(), visible=False)
#plt.setp(ax_gamma.get_yticklabels(), visible=False)

show()
