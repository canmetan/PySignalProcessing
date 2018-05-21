# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# Non integer multiples of sampling frequency causing leakage.
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


def labelPhasePlot(plot, title=''):
    plot.set_xlabel('Frequency (Hz)')
    plot.set_ylabel('Phase Angle')
    plot.set_title(title)


# First, arrange the plots and label them
fig = plt.figure()
plt.suptitle('FFT LEAK')

Plot1_1 = plt.subplot(331)
Plot1_2 = plt.subplot(334)
Plot1_3 = plt.subplot(337)
Plot2_1 = plt.subplot(332)
Plot2_2 = plt.subplot(335)
Plot2_3 = plt.subplot(338)
Plot3_1 = plt.subplot(333)
Plot3_2 = plt.subplot(336)
Plot3_3 = plt.subplot(339)


labelSignalPlot(Plot1_1, "1 Hz Cosine Wave")
labelSignalPlot(Plot2_1, "2.2 Hz Cosine Wave")
labelSignalPlot(Plot3_1, "7.5 Hz +pi Shifted Sine \n With Max Amplitude of 5")
labelFFTPlot(Plot1_2)
labelFFTPlot(Plot2_2)
labelFFTPlot(Plot3_2)
labelPhasePlot(Plot1_3)
labelPhasePlot(Plot2_3)
labelPhasePlot(Plot3_3)

# First Column _______________________________________________________________
# Frequency and sampling
f = 1
fs = 100
seconds = 1
N = fs * seconds
freqAxis = np.arange(0, fs, fs/N)

sinusoid = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=N)
fftOfSignal = scipy.fftpack.fft(sinusoid)

Plot1_1.plot(sinusoid, 'r.-')
Plot1_2.plot(freqAxis, abs(fftOfSignal), 'r.')
Plot1_3.plot(freqAxis, abs(np.angle(fftOfSignal, deg=True)), 'r.')

# Second Column ______________________________________________________________
# Frequency and sampling
f = 2.2
fs = 100
seconds = 1
N = fs * seconds
freqAxis = np.arange(0, fs, fs/N)

sinusoid = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=N)
fftOfSignal = scipy.fftpack.fft(sinusoid)

Plot2_1.plot(sinusoid, 'r.-')
Plot2_2.plot(freqAxis, abs(fftOfSignal), 'r.')
Plot2_3.plot(freqAxis, abs(np.angle(fftOfSignal, deg=True)), 'r.')

# Third Column _______________________________________________________________
f = 7.5
fs = 100
seconds = 1
N = fs * seconds
freqAxis = np.arange(0, fs, fs/N)

sinusoid = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=N,
                               initialPhase=np.pi, amplitude=5)
fftOfSignal = scipy.fftpack.fft(sinusoid)

Plot3_1.plot(sinusoid, 'r.-')
Plot3_2.plot(freqAxis, abs(fftOfSignal), 'r.')
Plot3_3.plot(freqAxis, abs(np.angle(fftOfSignal, deg=True)), 'r.')

plt.tight_layout()
plt.show()
