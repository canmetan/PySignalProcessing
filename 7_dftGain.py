# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# Zero padding can be used to increase the fft resolution. Initial signal is
# 256 samples long. Second one was padded with 256 zeros = 512 samples.
# The third signal is padded with 512 additional samples:
# So it is 256 + (256 + 512) = 256 + 768 = 1024 samples long.
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


def labelSignalPlot(plot, title=''):
    plot.set_xlabel('n')
    plot.set_ylabel('x(n)')
    plot.set_title(title)


def labelFFTPlot(plot, title=''):
    plot.set_xlabel('Frequency (Hz)')
    plot.set_ylabel('X(n)')
    plot.set_title(title)


# First, arrange the plots and label them
fig = plt.figure()
plt.suptitle('FFT Resolution With Zero Padding')

Plot1_1 = plt.subplot(231)
Plot1_2 = plt.subplot(234)
Plot2_1 = plt.subplot(232)
Plot2_2 = plt.subplot(235)
Plot3_1 = plt.subplot(233)
Plot3_2 = plt.subplot(236)

labelSignalPlot(Plot1_1, "Noise + 5 Hz Cosine Wave\n 256 points")
labelSignalPlot(Plot2_1, "Noise + 5 Hz Cosine Wave\n 512 points")
labelSignalPlot(Plot3_1, "Noise + 5 Hz Cosine Wave\n 1024 points")

labelFFTPlot(Plot1_2, "256 Point FFT")
labelFFTPlot(Plot2_2, "512 Point FFT")
labelFFTPlot(Plot3_2, "1024 Point FFT")

# ___________________________________________________________________________
# Frequency and sampling
f = 5
fs = 100
noiseAmplitude = 10

signal256 = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=256) + \
            noiseAmplitude * (np.random.rand(256) + np.random.rand(256) - 1)

signal512 = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=512) + \
            noiseAmplitude * (np.random.rand(512) + np.random.rand(512) - 1)
signal1024 = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=1024) + \
            noiseAmplitude * (np.random.rand(1024) + np.random.rand(1024) - 1)

fft256Point = scipy.fftpack.fft(signal256)
fft512Point = scipy.fftpack.fft(signal512)
fft1024Point = scipy.fftpack.fft(signal1024)

fft256 = scipy.fftpack.fft(signal256)
fft512 = scipy.fftpack.fft(signal512)
fft1024 = scipy.fftpack.fft(signal1024)

freqAxis = np.arange(0, fs, fs/256)
Plot1_1.plot(signal256, 'r-')
Plot1_2.plot(freqAxis, abs(fft256Point), 'r.')

freqAxis = np.arange(0, fs, fs/512)
Plot2_1.plot(signal512, 'r-')
Plot2_2.plot(freqAxis, abs(fft512Point), 'r.')

freqAxis = np.arange(0, fs, fs/1024)
Plot3_1.plot(signal1024, 'r-')
Plot3_2.plot(freqAxis, abs(fft1024Point), 'r.')

plt.tight_layout()
plt.show()
