import numpy as np
import bottleneck as bn
from scipy import optimize
from scipy import signal
from scipy import delete
import matplotlib.pyplot as plt
import math

# fileLoc = input('Enter the name of file with extension .txt : ')
csv = np.genfromtxt('Data_Raman2.txt')
rangeData = csv[:, 0]
data = csv[:, 1]


# ############# Guess functions #############
# peakind = signal.argrelextrema(data, np.greater)
# peakind = np.delete(peakind, 1, 1)
# peakind = peakind.transpose()
# maxpeak1 = np.argmax(data[peakind])
# maxloc1 = peakind[maxpeak1]
# max1 = data[maxloc1]
# print data[peakind]
# data[maxloc1]=0
# diff = 20
# maxr2 = 0
# maxlocr2 = 0
# maxloc2 = 0
# max2 = 0
# maxpeakr2 = np.argmax(data[peakind[maxpeak1 + diff:]])
# maxlocr2 = peakind[maxpeakr2]
# maxr2 = data[maxlocr2]
# print maxr2
# maxloc2 = maxlocr2
# max2 = maxr2
# print max2

def gaussian(x, height, center, width, offset):
    return height * np.exp(-(x - center) ** 2 / (2 * width ** 2)) + offset


def two_gaussians(x, h1, c1, w1, h2, c2, w2, offset):
    return gaussian(x, h1, c1, w1, offset=0) + gaussian(x, h2, c2, w2, offset=0) + offset


errfunc = lambda p, rangeData, data: np.array((two_gaussians(rangeData, *p) - data) ** 2)

guess = np.array([900, 1300, 20, 800, 1600, 15, -40])

results, success = optimize.leastsq(errfunc, guess[:], args=(rangeData, data))
print results

plt.plot(rangeData, data, lw=5, c='g', label='measurement')
plt.plot(rangeData, two_gaussians(rangeData, *results), lw=3, c='b', label='fit of 2 Gaussians')
plt.legend(loc='best')
plt.show()

########## Integrate ###############

h1, c1, w1, h2, c2, w2, offset = results
suml=0
for i in rangeData:
    suml += gaussian(i, h1, c1, w1, 0)
sumr = 0
for i in rangeData:
    sumr += gaussian(i, h2, c2, w2, 0)
print suml
print sumr
