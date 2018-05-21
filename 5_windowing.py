# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# Effects of windowing on signals that have spectral leakage. Other types of
# signals can also be used.
# ____________________________________________________________________________


# Peaks of the spectral leakage isn't equal, why??

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


def applyTriangularWindow(signal, startVal=0.05):
    ''' Applies triangular function to the original signal.
    Value starts from 0.05 instead of 0 and ends at 0.05.'''
    halfLength = len(signal) // 2
    counter = 0

    for x in np.linspace(startVal, 1.0, halfLength, endpoint=False):
        signal[counter] = signal[counter] * x
        counter += 1

    for x in np.linspace(1.0, startVal, halfLength, endpoint=True):
        signal[counter] = signal[counter] * x
        counter += 1

    return signal


def getTriangularWindow(length, startVal=0.05):
    ''' Applies triangular function to the original signal.
    Value starts from 0.05 instead of 0 and ends at 0.05.'''
    halfLength = length // 2
    window = []

    for x in np.linspace(startVal, 1.0, halfLength, endpoint=False):
        window.append(x)

    for x in np.linspace(1.0, startVal, halfLength, endpoint=True):
        window.append(x)

    return np.array(window)


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
plt.suptitle('Windowing for FFT Leakage')

Plot1_1 = plt.subplot(231)
Plot1_2 = plt.subplot(234)
Plot2_1 = plt.subplot(232)
Plot2_2 = plt.subplot(235)
Plot3_1 = plt.subplot(233)
Plot3_2 = plt.subplot(236)


labelSignalPlot(Plot1_1, "20.5 Hz Cosine Wave\n(Rectangular)")
labelSignalPlot(Plot2_1, "20.5 Hz Cosine Wave\n(Triangular)")
labelSignalPlot(Plot3_1, "20.5 Hz Cosine Wave\n(Hanning)")

labelFFTPlot(Plot1_2, "Rectangular Window (no window)")
labelFFTPlot(Plot2_2, "Triangular Window")
labelFFTPlot(Plot3_2, "Hanning Window")

# First Column _______________________________________________________________
# Frequency and sampling
f = 20.5
fs = 100
seconds = 1
N = fs * seconds
freqAxis = np.arange(0, fs, fs/N)

sinusoid = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=N)
sinusoidWithTriangular = np.array(sinusoid) * \
                         getTriangularWindow(len(sinusoid))
sinusoidWithHamming = np.array(sinusoid) * np.hamming(len(sinusoid))

fftWithoutWindowing = scipy.fftpack.fft(sinusoid)
fftWithTriangular = scipy.fftpack.fft(sinusoidWithTriangular)
fftWithHamming = scipy.fftpack.fft(sinusoidWithHamming)

Plot1_1.plot(sinusoid, 'r.-')
Plot1_2.plot(freqAxis, abs(fftWithoutWindowing), 'r.')
Plot2_1.plot(sinusoidWithTriangular, 'r.-')
Plot2_2.plot(freqAxis, abs(fftWithTriangular), 'r.')
Plot3_1.plot(sinusoidWithHamming, 'r.-')
Plot3_2.plot(freqAxis, abs(fftWithHamming), 'r.')

plt.tight_layout()
plt.show()
