# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# This is just a demonstration for generating wide band signals.
# Original data, Histogram, FFT and Phase will be displayed.
# ____________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
# from scipy import signal
import common
import sys

# Assert that the user is using python above version 3.1
assert sys.version_info >= (3, 1)

# Parameters for the signal
samplingFrequency = 1000
seconds = 50

wideBandSignal = common.generateWidebandNoise(
        samplingFrequency=samplingFrequency,
        seconds=seconds, amplitude=1)

wideBandSignalFFT = scipy.fftpack.fft(wideBandSignal)

fig = plt.figure()

plotColor = 'g.'

Plot1 = plt.subplot(221)
common.labelSignalPlot(Plot1, "Time Domain Values")
Plot2 = plt.subplot(222)
common.labelFFTPlot(Plot2, "Histogram")
Plot3 = plt.subplot(223)
common.labelLogFFTPlot(Plot3, "Normalized FFT")
Plot4 = plt.subplot(224)
common.labelPhasePlot(Plot4, "Phase Angle")

frequencyAxis = np.arange(0, samplingFrequency, 1/seconds)


Plot1.plot(wideBandSignal, plotColor)
# the histogram of the data
n, bins, patches = Plot2.hist(wideBandSignal, bins=1000, normed=1,
                              facecolor='g', alpha=0.75)

Plot3.plot(frequencyAxis,
           common.normalizeFromZeroToOne(np.abs(wideBandSignalFFT)),
           plotColor)
Plot4.plot(frequencyAxis, abs(np.angle(wideBandSignalFFT, deg=True)),
           plotColor)

plt.subplots_adjust(wspace=0, hspace=0)

plt.tight_layout()
plt.show()
