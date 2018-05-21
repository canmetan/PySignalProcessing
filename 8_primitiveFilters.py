# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# This is a demo of various filters and their frequency response. All filters
# contain the same number of samples with padded zeros if necessary.
#
# Green graph is a low-pass filter
# Black graph is a band-pass filter
# Red graph is a high-pass filter
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


# GLOBAL VARIABLES
# Time Domain Variables
samplingFrequency = 1000

# Frequency Domain Variables
firFilterSize = 256
halfOfBandPassBins = 12
bandpassCenterFrequencyBin = 35
highPassCenterFrequencyBin = firFilterSize/2
# print(highPassCenterFrequencyBin)

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

lowPassFilterDFT = ([firFilterSize/2] * (halfOfBandPassBins + 1) +
                    [0] * (firFilterSize - 1 - (2 * halfOfBandPassBins)) +
                    [firFilterSize/2] * (halfOfBandPassBins))

# Construct a low pass filter from the DFT
lowPassFilter = scipy.fftpack.ifft(lowPassFilterDFT)

# Multiplying the low pass filter with the phase shifting sinusoid should yield
# to a shifted pass band for the lowpass filter = band pass filter.
# Frequency of this sinusoid should be:
# (bandpassCenterFrequencyBin * samplingFrequency / firFilterSize)
bandShiftSinusoid = getDiscreteSinusoid(
        (bandpassCenterFrequencyBin * samplingFrequency / firFilterSize),
        samplingFrequency, numberOfSamples=firFilterSize)

# High Pass filter works in a similar fashion
highPassSinusoid = getDiscreteSinusoid(
        (highPassCenterFrequencyBin * samplingFrequency / firFilterSize),
        samplingFrequency, numberOfSamples=firFilterSize, initialPhase=np.pi/2)

#highPassSinusoid = getDiscreteSinusoid(
#        (highPassCenterFrequencyBin * samplingFrequency / firFilterSize),
#        samplingFrequency, numberOfSamples=firFilterSize)

bandPassFilter = lowPassFilter * bandShiftSinusoid
highPassFilter = lowPassFilter * highPassSinusoid

bandPassFilterDFT = scipy.fftpack.fft(bandPassFilter)
highPassFilterDFT = scipy.fftpack.fft(highPassFilter)

# Colors for drawing the plots
colorLowPass = 'r.'
colorBandPass = 'g.'
colorHighPass = 'b.'

labelLowPass = "Low Pass"
labelBandPass = "Band Pass"
labelHighPass = "High Pass"

# Plotting
fig = plt.figure()

# Since the filter size and sampling frequency is the same, frequency axis
# is also the same for everyone.
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

Plot1.plot(lowPassFilter, colorLowPass, label=labelLowPass)
Plot1.plot(bandPassFilter, colorBandPass, label=labelBandPass)
Plot1.plot(highPassFilter, colorHighPass, label=labelHighPass)
# Place a legend on the graph
Plot1.legend(loc=1)

Plot2.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(lowPassFilterDFT)),
           colorLowPass)
Plot2.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(bandPassFilterDFT)),
           colorBandPass)
Plot2.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(highPassFilterDFT)),
           colorHighPass)

#Plot2.plot(frequencyAxis, np.abs(lowPassFilterDFT),  colorLowPass)
#Plot2.plot(frequencyAxis, np.abs(bandPassFilterDFT), colorBandPass)
#Plot2.plot(frequencyAxis, np.abs(highPassFilterDFT), colorHighPass)

Plot3.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(lowPassFilterDFT)),
           colorLowPass)
Plot3.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(bandPassFilterDFT)),
           colorBandPass)
Plot3.plot(frequencyAxis, normalizeFromZeroToOne(np.abs(highPassFilterDFT)),
           colorHighPass)
Plot3.set_yscale("log", nonposx='clip')


Plot4.plot(frequencyAxis, abs(np.angle(lowPassFilter, deg=True)),
           colorLowPass)
Plot4.plot(frequencyAxis, abs(np.angle(bandPassFilter, deg=True)),
           colorBandPass)
Plot4.plot(frequencyAxis, abs(np.angle(highPassFilter, deg=True)),
           colorHighPass)

plt.subplots_adjust(wspace=0, hspace=0)

plt.tight_layout()
plt.show()
