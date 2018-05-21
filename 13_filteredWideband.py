# Author: Can Metan unwrapping the phase
# GPL v3 License
# ____________________________________________________________________________
# This generates a wideband signal, convolves with two low pass filters.
# One of them is a manually generated low pass filter and
# The other one is generated with remez exchange algorithm.
# They are both windowed with blackman window.
# We will calculate the DFT and phase afterwards.
#
# Green graph is the original signal
# Cyan is the convolution with manually constructed low pass filter
# Black is the convolution with the remez low pass filter
# ____________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
import sys
import common

# Assert that the user is using python above version 3.1
assert sys.version_info >= (3, 1)


# Parameters for the signal
samplingFrequency = 1000
seconds = 2

# First, let's generate the original wideband signal itself.
wideBandSignal = common.generateWidebandNoise(
        samplingFrequency=samplingFrequency,
        seconds=seconds, amplitude=1)


filterLength = 256
numberOfLowPassBins = filterLength//10
cutoffFrequency = common.toFrequency(numberOfLowPassBins,
                                     samplingFrequency,
                                     filterLength)

# MANUALLY CONSTRUCTED LOW PASS FILTER ++++++++++++++++++++++++++++++++++++++++
# Lets generate a low pass filter from our expectation
lowPassFilteredDFT = ([filterLength/2] * numberOfLowPassBins +
                      (filterLength - 2 * numberOfLowPassBins) * [0] +
                      [filterLength/2] * numberOfLowPassBins)

# Time Domain FIR Filter Generation with blackman window
lowPassFiltered = np.multiply(scipy.fftpack.ifft(lowPassFilteredDFT),
                              np.blackman(filterLength))

# Now lets convolve with the signal itself
# lowPassFiltered = common.convolve(lowPassFiltered, wideBandSignal)
lowPassFiltered = scipy.signal.convolve(lowPassFiltered, wideBandSignal)
# Now lets get the FFT of this signal again :)
lowPassFilteredDFT = scipy.fftpack.fft(lowPassFiltered)


# LOW PASS FILTER WITH REMEZ EXCHANGE ALGORITHM++++++++++++++++++++++++++++++++
transitionGap = 0.01

remezFiltered = signal.remez(filterLength,
                             [0, cutoffFrequency,  # Pass band
                              cutoffFrequency + transitionGap,
                              samplingFrequency/2],  # Stop band
                             [1, 0],
                             Hz=samplingFrequency)

#remezFiltered2 = signal.remez(filterLength + len(wideBandSignal) - 1,
#                             [0, transitionGap,
#                              (transitionGap + transitionGap), cutoffFrequency,  # Pass band
#                              cutoffFrequency + transitionGap,
#                              samplingFrequency/2],  # Stop band
#                             [0, 1, 0],
#                             Hz=samplingFrequency)
#remezFilteredDFT2 = scipy.fftpack.fft(remezFiltered2)

# Applying blackman window to the original signal
remezFiltered = np.multiply(remezFiltered,
                            np.blackman(filterLength))
# Now lets convolve with the original signal
# remezFiltered = common.convolve(remezFiltered, wideBandSignal)
remezFiltered = scipy.signal.convolve(remezFiltered, wideBandSignal)
remezFilteredDFT = scipy.fftpack.fft(remezFiltered)

# Variables for plotting
frequencyAxis = np.arange(0, samplingFrequency,
                          samplingFrequency/(filterLength + len(wideBandSignal) - 1))

# Just padding some zeros for plotting the wideband signal with others
wideBandSignal = np.ndarray.tolist(wideBandSignal)
wideBandSignal.extend([0.0] * (filterLength - 1))
wideBandSignalDFT = scipy.fftpack.fft(wideBandSignal)


colorOriginalSignal = 'g.'
colorLowPassBlackman = 'c-'
colorRemezBlackman = 'k-'

labelOriginalSignal = "Original Signal"
labelLowpassBlackman = "Manual"
labelRemezBlackman = "Remez"

# Plotting
fig = plt.figure()

Plot1 = plt.subplot(221)
common.labelSignalPlot(Plot1, "Time Domain Values")
Plot2 = plt.subplot(222)
common.labelFFTPlot(Plot2, "Normalized FFT")
Plot3 = plt.subplot(223)
common.labelLogFFTPlot(Plot3, "FFT on Logarithmic Scale")
Plot4 = plt.subplot(224)
common.labelPhasePlot(Plot4, "Phase Angle Difference")

Plot1.plot(wideBandSignal, colorOriginalSignal, label=labelOriginalSignal)
Plot1.plot(lowPassFiltered, colorLowPassBlackman, label=labelLowpassBlackman)
Plot1.plot(remezFiltered, colorRemezBlackman, label=labelRemezBlackman)
# Place a legend on the graph
Plot1.legend(loc=1)


Plot2.plot(frequencyAxis,
           common.normalizeFromZeroToOne(np.abs(wideBandSignalDFT)),
           colorOriginalSignal)
#Plot2.plot(frequencyAxis,
#           common.normalizeFromZeroToOne(np.abs(remezFilteredDFT2)),
#           colorOriginalSignal)
Plot2.plot(frequencyAxis,
           common.normalizeFromZeroToOne(np.abs(lowPassFilteredDFT)),
           colorLowPassBlackman)
Plot2.plot(frequencyAxis,
           common.normalizeFromZeroToOne(np.abs(remezFilteredDFT)),
           colorRemezBlackman)


Plot3.plot(frequencyAxis,
           common.normalizeFromZeroToOne(np.abs(wideBandSignalDFT)),
           colorOriginalSignal)
Plot3.plot(frequencyAxis,
           common.normalizeFromZeroToOne(np.abs(lowPassFilteredDFT)),
           colorLowPassBlackman)
Plot3.plot(frequencyAxis,
           common.normalizeFromZeroToOne(np.abs(remezFilteredDFT)),
           colorRemezBlackman)
Plot3.set_yscale("log", nonposx='clip')

# We're getting the difference between the phase angle of wideband signal
# with the filtered signals
widebandPhase = abs(np.angle(wideBandSignalDFT, deg=True))

Plot4.plot(frequencyAxis,
           abs(np.angle(lowPassFilteredDFT, deg=True)) - widebandPhase,
           colorLowPassBlackman)
Plot4.plot(frequencyAxis,
           abs(np.angle(remezFilteredDFT, deg=True)) - widebandPhase,
           colorRemezBlackman)


plt.subplots_adjust(wspace=0, hspace=0)

plt.tight_layout()
plt.show()

