# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# This is a demo of FIR filter design. We chose to have two pass bands in this
# filtering design.
#
# Red   graph is our custom pass filter with rectangular window
# Green graph is the custom pass filter with blackman window
# ____________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import sys

# Assert that the user is using python above version 3.1
assert sys.version_info >= (3, 1)


def getDiscreteSinusoid(sinusoidFrequency, samplingFrequency, sinusoid=np.sin,
                        seconds=None, numberOfSamples=None, initialPhase=0,
                        amplitude=1):
    ''' Samples a sinusoid signal with the given parameters. All the
    frequency values are in Hz, phase is in radians.'''
    if (numberOfSamples is not None) & (seconds is None):
        # Generating a sine wave with the given number of samples
        n = np.arange(0, numberOfSamples)
        xOfN = amplitude * sinusoid(initialPhase + 2 * np.pi *
                                    sinusoidFrequency * n / samplingFrequency)
        return xOfN
    elif (seconds is not None) & (numberOfSamples is None):
        # Generating a sine wave with the given time duration
        n = np.arange(0, (samplingFrequency / sinusoidFrequency) * seconds)
        xOfN = amplitude * sinusoid(initialPhase + 2 * np.pi *
                                    sinusoidFrequency * n / samplingFrequency)
        return xOfN
    elif (seconds is not None) & (numberOfSamples is not None):
        print('Either seconds or number of samples can be passed,'
              'but not both.')
        return None
    else:
        print('Either seconds or number of samples needs to be passed.')
        return None


def toFrequency(binIndex, samplingFrequency, N):
    '''Returns the frequency of the bin index in a given DFT'''
    return (binIndex*samplingFrequency/N)


def normalizeFromZeroToOne(data):
    ''' Simply normalizes any value from zero to one. '''
    minData = min(data)
    maxMinDifference = max(data) - min(data)
    data = (data - minData) / maxMinDifference
    return data


def labelSignalPlot(plot, title=''):
    plot.set_xlabel('n')
    plot.set_ylabel('x(n)')
    plot.set_title(title)


def labelFFTPlot(plot, title=''):
    plot.set_xlabel('Frequency (Hz)')
    plot.set_ylabel('X(n)')
    plot.set_title(title)


def labelLogFFTPlot(plot, title=''):
    plot.set_xlabel('Frequency (Hz)')
    plot.set_ylabel('Log10( X(n) )')
    plot.set_title(title)


def labelPhasePlot(plot, title=''):
    plot.set_xlabel('Frequency (Hz)')
    plot.set_ylabel('Angle')
    plot.set_title(title)


def checkParameterValidity(firstPassBandLength, secondPassBandLength,
                           firstPassBandStartBin, secondPassBandStartBin):
    # Basically if one of them is zero, fail the execution
    if(firstPassBandLength == 0):
        print("firstPassBandLength can't be zero!")
        sys.exit()
    elif (secondPassBandLength == 0):
        print("secondPassBandLength can't be zero!")
        sys.exit()
    elif (firstPassBandStartBin == 0):
        print("firstPassBandStartingFrequency can't be zero!")
        sys.exit()
    elif (secondPassBandStartBin == 0):
        print("secondPassBandStartingFrequency can't be zero!")
        sys.exit()
    else:
        return


# GLOBAL VARIABLES
# Time Domain Variables
samplingFrequency = 1000

# Frequency Domain Variables
firFilterSize = 256
# Filter parameters, these are just chosen randomly
firstPassBandLength = firFilterSize//10
secondPassBandLength = firFilterSize//10
firstPassBandStartBin = firFilterSize//8
secondPassBandStartBin = firFilterSize//4
checkParameterValidity(firstPassBandLength, secondPassBandLength,
                       firstPassBandStartBin, secondPassBandStartBin)


# So the frequency equivalent of this would be:
# (BinNumber * SamplingFrequency / N)
# where N is the DFT size.

# Lets generate low pass filter from our frequency response expectation.
# The magnitude of the FFT is (Amplitude * NumberOfSamples) / 2. Two options:
#
# 1) if magnitude on time domain is desired to be 1, then the FFT value should
# be (NumberOfSamples / 2).
#
# 2) If the FFT magnitude is desired to be 1:
# Then the Amplitude of the signal should be (2 / NumberOfSamples)
#
# The Low pass FFT will be N+1 unity values (0th index for DC) and N unity
# towards the end. Remaining is 0.

# Custom two pass band filter  [-__---______---___]
# First point is DC.
# A stop band
# First pass band
# A stop band again
# Second pass band
# Stop band for the rest


halfOfCustomFilterDFT = ([firFilterSize/2] * 1 +  # This is DC
                [0] * int(firstPassBandStartBin - 1) +
                [firFilterSize/2] * firstPassBandLength +
                [0] * int(secondPassBandStartBin - firstPassBandStartBin - (firstPassBandLength)) +
                [firFilterSize/2] * (secondPassBandLength) +
                [0] * int(firFilterSize/2 - secondPassBandStartBin - secondPassBandLength))

# Now reverse the list and append to the end of the low pass filter
customFilterRectangularDFT = (halfOfCustomFilterDFT +
                              halfOfCustomFilterDFT[::-1])


# Construct a low pass filter from the DFT
customFilterRectangular = scipy.fftpack.ifft(customFilterRectangularDFT)
customFilterBlackman = np.multiply(customFilterRectangular,
                                   np.blackman(firFilterSize))
customFilterBlackmanDFT = scipy.fftpack.fft(customFilterBlackman)

# Colors for drawing the plots
colorCustomRectangular = 'r.'
colorCustomBlackman = 'g.'

labelCustomRectangular = "Custom Rectangle"
labelCustomBlackman = "Custom Blackman"

# Variables for Plotting
fig = plt.figure()
frequencyAxis = np.arange(0, samplingFrequency,
                          samplingFrequency/firFilterSize)

Plot1 = plt.subplot(221)
labelSignalPlot(Plot1, "Time Domain Values")
Plot2 = plt.subplot(222)
labelFFTPlot(Plot2, "Normalized FFT")
Plot3 = plt.subplot(223)
labelLogFFTPlot(Plot3, "FFT on Logarithmic Scale")
Plot4 = plt.subplot(224)
labelPhasePlot(Plot4, "Phase Angle")

Plot1.plot(customFilterRectangular, colorCustomRectangular,
           label=labelCustomRectangular)
Plot1.plot(customFilterBlackman, colorCustomBlackman,
           label=labelCustomBlackman)
# Place a legend on the graph
Plot1.legend(loc=1)

Plot2.plot(frequencyAxis,
           normalizeFromZeroToOne(np.abs(customFilterRectangularDFT)),
           colorCustomRectangular)
Plot2.plot(frequencyAxis,
           normalizeFromZeroToOne(np.abs(customFilterBlackmanDFT)),
           colorCustomBlackman)

Plot3.plot(frequencyAxis,
           normalizeFromZeroToOne(np.abs(customFilterRectangularDFT)),
           colorCustomRectangular)

Plot3.plot(frequencyAxis,
           normalizeFromZeroToOne(np.abs(customFilterBlackmanDFT)),
           colorCustomBlackman)

Plot3.set_yscale("log", nonposx='clip')

Plot4.plot(frequencyAxis, abs(np.angle(customFilterRectangularDFT, deg=True)),
           colorCustomRectangular)
Plot4.plot(frequencyAxis, abs(np.angle(customFilterBlackmanDFT, deg=True)),
           colorCustomBlackman)

plt.subplots_adjust(wspace=0, hspace=0)

plt.tight_layout()
plt.show()
