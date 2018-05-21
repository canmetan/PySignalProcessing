# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# This is a demo of FIR filter design. We chose to have two pass bands in this
# filtering design.
#
# Blue  graph is the remez filter with rectangular window
# Black graph is the remez with blackman window
# Red graph is the remez filter with nuttall window
# ____________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
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
# Filter adjustments
firstPassBandLength = firFilterSize//10
secondPassBandLength = firFilterSize//10
firstPassBandStartBin = firFilterSize//8
secondPassBandStartBin = firFilterSize//4
checkParameterValidity(firstPassBandLength, secondPassBandLength,
                   firstPassBandStartBin, secondPassBandStartBin)
# Remez specific variables
firstPassBandStartingFrequency = toFrequency(firstPassBandStartBin, samplingFrequency, firFilterSize)
firstPassBandEndingFrequency = toFrequency(firstPassBandStartBin + firstPassBandLength, samplingFrequency, firFilterSize)
secondPassBandStartingFrequency = toFrequency(secondPassBandStartBin, samplingFrequency, firFilterSize)
secondPassBandEndingFrequency = toFrequency(secondPassBandStartBin + secondPassBandLength, samplingFrequency, firFilterSize)
transitionGap = 0.01

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


# TIME DOMAIN FILTERS =========================================================
remezFilterRectangular = signal.remez(firFilterSize,
                                      [0, firstPassBandStartingFrequency - transitionGap,                                  # First Stop Band
                                       firstPassBandStartingFrequency, firstPassBandEndingFrequency,       # First Pass Band
                                       firstPassBandEndingFrequency + transitionGap, secondPassBandStartingFrequency - transitionGap,      # Second Stop Band
                                       secondPassBandStartingFrequency, secondPassBandEndingFrequency,     # Second Pass Band
                                       secondPassBandEndingFrequency + transitionGap , samplingFrequency/2],                # Rest of it is Stop Band
                                      [0, firFilterSize/2, 0, firFilterSize/2, 0], Hz=samplingFrequency)

remezFilterBlackman = np.multiply(remezFilterRectangular,
                                    scipy.signal.blackman(firFilterSize, sym=True))
remezFilterNuttall = np.multiply(remezFilterRectangular,
                                    scipy.signal.nuttall(firFilterSize, sym=True))

remezFilterRectangularDFT = scipy.fftpack.fft(remezFilterRectangular)
remezFilterBlackmanDFT = scipy.fftpack.fft(remezFilterBlackman)
remezFilterNuttallDFT = scipy.fftpack.fft(remezFilterNuttall)

# Colors for drawing the plots
colorRemezRectangular = 'b.'
colorRemezBlackman = 'k.'
colorRemezNuttall = 'r.'

labelRemezRectangular = "Remez Rectangle"
labelRemezBlackman = "Remez Blackman"
labelRemezNuttall = "Remez Nuttall"

# Plotting
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

Plot1.plot(remezFilterRectangular, colorRemezRectangular, label=labelRemezRectangular)
Plot1.plot(remezFilterBlackman, colorRemezBlackman, label=labelRemezBlackman)
Plot1.plot(remezFilterNuttall, colorRemezNuttall, label=labelRemezNuttall)
# Place a legend on the graph
Plot1.legend(loc=1)

Plot2.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(remezFilterRectangularDFT)), colorRemezRectangular)
Plot2.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(remezFilterBlackmanDFT)), colorRemezBlackman)
Plot2.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(remezFilterNuttallDFT)), colorRemezNuttall)

Plot3.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(remezFilterRectangularDFT)), colorRemezRectangular)
Plot3.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(remezFilterBlackmanDFT)), colorRemezBlackman)
Plot3.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(remezFilterNuttallDFT)), colorRemezNuttall)
Plot3.set_yscale("log", nonposx='clip')

Plot4.plot(frequencyAxis, abs(np.angle(remezFilterRectangularDFT, deg=True)), colorRemezRectangular)
Plot4.plot(frequencyAxis, abs(np.angle(remezFilterBlackmanDFT, deg=True)), colorRemezBlackman)
Plot4.plot(frequencyAxis, abs(np.angle(remezFilterRectangularDFT, deg=True)), colorRemezNuttall)

plt.subplots_adjust(wspace=0, hspace=0)

plt.tight_layout()
plt.show()
