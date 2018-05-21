# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# Shows the phase shift doesn't change the fft of a signal.
# sin(x) = cos(x - pi/2) ---> Cos right shift by pi/2
# Notice that the phase shift doens't change the FFT.
# ____________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import sys

# Assert that the user is using python above version 3.1
assert sys.version_info >= (3, 1)


# Now signal can have an initial phase and amplitude!
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
plt.suptitle('PHASE SHIFT')

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
labelSignalPlot(Plot2_1, "1 Hz Sine Wave")
labelSignalPlot(Plot3_1, "1 Hz +pi Shifted Cosine \n With Max Amplitude of 5")
labelFFTPlot(Plot1_2)
labelFFTPlot(Plot2_2)
labelFFTPlot(Plot3_2)
labelPhasePlot(Plot1_3)
labelPhasePlot(Plot2_3)
labelPhasePlot(Plot3_3)

# Frequency and sampling is the same for all of the plots
f = 1
fs = 200
seconds = 1
N = fs * seconds
freqAxis = np.arange(0, fs, fs/N)

# First Column _______________________________________________________________
sinusoid = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=N)
fftOfSignal = scipy.fftpack.fft(sinusoid)

Plot1_1.plot(sinusoid, 'r.-')
Plot1_2.plot(freqAxis, abs(fftOfSignal), 'r.')
Plot1_3.plot(freqAxis, abs(np.angle(fftOfSignal, deg=True)), 'r.')

# Second Column ______________________________________________________________
sinusoid = getDiscreteSinusoid(f, fs, np.sin, numberOfSamples=N)
fftOfSignal = scipy.fftpack.fft(sinusoid)

Plot2_1.plot(sinusoid, 'r.-')
Plot2_2.plot(freqAxis, abs(fftOfSignal), 'r.')
Plot2_3.plot(freqAxis, abs(np.angle(fftOfSignal, deg=True)), 'r.')

# Third Column _______________________________________________________________
sinusoid = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=N,
                               initialPhase=np.pi, amplitude=5)
fftOfSignal = scipy.fftpack.fft(sinusoid)

Plot3_1.plot(sinusoid, 'r.-')
Plot3_2.plot(freqAxis, abs(fftOfSignal), 'r.')
Plot3_3.plot(freqAxis, abs(np.angle(fftOfSignal, deg=True)), 'r.')


plt.tight_layout()
plt.show()
