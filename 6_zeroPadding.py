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

labelSignalPlot(Plot1_1, "20.5 Hz Cosine Wave\n(Hanning, no 0 padding)")
labelSignalPlot(Plot2_1, "20.5 Hz Cosine Wave\n(Hanning) \\w. 256 Zeros")
labelSignalPlot(Plot3_1, "20.5 Hz Cosine Wave\n(Hanning) \\w. 768 Zeros")

labelFFTPlot(Plot1_2, "Rectangular Window (no window)")
labelFFTPlot(Plot2_2, "Triangular Window")
labelFFTPlot(Plot3_2, "Hanning Window")

# Frequency and sampling
f = 20.5
fs = 80
sampleCount = 256

sinusoid = np.array(getDiscreteSinusoid(f, fs, np.cos,
                                        numberOfSamples=sampleCount))
sinusoid = sinusoid * np.hamming(len(sinusoid))

sinusoidWith256Zeros = sinusoid.tolist() + ([0] * 256)
sinusoidWith768Zeros = sinusoid.tolist() + ([0] * 768)

fftWithoutZeros = scipy.fftpack.fft(sinusoid)
fftWith256Zeros = scipy.fftpack.fft(sinusoidWith256Zeros)
fftWith768Zeros = scipy.fftpack.fft(sinusoidWith768Zeros)

freqAxis = np.arange(0, fs, fs/256)
Plot1_1.plot(sinusoid, 'r.-')
Plot1_2.plot(freqAxis, abs(fftWithoutZeros), 'r.-')

freqAxis = np.arange(0, fs, fs/512)
Plot2_1.plot(sinusoidWith256Zeros, 'r.-')
Plot2_2.plot(freqAxis, abs(fftWith256Zeros), 'r.-')

freqAxis = np.arange(0, fs, fs/1024)
Plot3_1.plot(sinusoidWith768Zeros, 'r.-')
Plot3_2.plot(freqAxis, abs(fftWith768Zeros), 'r.-')

plt.tight_layout()
plt.show()
