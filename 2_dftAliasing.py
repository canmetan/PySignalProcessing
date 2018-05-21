# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# Sample execution that shows the aliasing of sinusoids. f + (k * fs) are
# aliased as f. In this example 3 + (2*100) = 203 Hz is aliased as 3 Hz.
# Notice that the magnitude of the FFT is (Amplitude * N) / 2
# ____________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import sys

# Assert that the user is using python above version 3.1
assert sys.version_info >= (3, 1)


def getDiscreteSinusoid(sinusoidFrequency, samplingFrequency, sinusoid=np.sin,
                        seconds=None, numberOfSamples=None):
    ''' Samples a sinusoid signal with the given parameters. All the
    frequency values are in Hz.'''
    if (numberOfSamples is not None) & (seconds is None):
        # Generating a sine wave with the given number of samples
        n = np.arange(0, numberOfSamples)
        xOfN = sinusoid(2 * np.pi * sinusoidFrequency * n / samplingFrequency)
        return xOfN
    elif (seconds is not None) & (numberOfSamples is None):
        # Generating a sine wave with the given time duration
        n = np.arange(0, (samplingFrequency / sinusoidFrequency) * seconds)
        xOfN = sinusoid(2 * np.pi * sinusoidFrequency * n / samplingFrequency)
        return xOfN
    elif (seconds is not None) & (numberOfSamples is not None):
        print('Either seconds or number of samples can be passed,'
              'but not both.')
        return None
    else:
        print('Either seconds or number of samples needs to be passed.')
        return None


# First, arrange the plots and label them
fig = plt.figure()
plt.suptitle('ALIASING')

firstPlot = plt.subplot(221)
secondPlot = plt.subplot(223)
thirdPlot = plt.subplot(222)
fourthPlot = plt.subplot(224)

firstPlot.set_xlabel('n')
firstPlot.set_ylabel('x(n)')
firstPlot.set_title('3 Hz Signal, \nSampled @ 100 Hz')

secondPlot.set_xlabel('Frequency (Hz)')
secondPlot.set_ylabel('X(n)')

thirdPlot.set_xlabel('n')
thirdPlot.set_ylabel('x(n)')
thirdPlot.set_title('203 Hz Aliased Signal,\nSampled @ 100 Hz'
                    '[f = f + (k * fs)]')

fourthPlot.set_xlabel('Frequency (Hz)')
fourthPlot.set_ylabel('X(n)')

# Generate the first two plots
f = 3
fs = 100
seconds = 1
N = fs * seconds  # One extra sample
freqAxis = np.arange(0, fs, fs/N)

sinusoid = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=N)
fftOfSignal = abs(scipy.fftpack.fft(sinusoid))

firstPlot.plot(sinusoid, 'r.-')
secondPlot.plot(freqAxis, fftOfSignal, 'r.')

# Generate the second two plots
# ----- NOTICE THE ALIASING OF f = f + (k * fs)  ------
fs = 100
f = 203
seconds = 1
N = fs * seconds
freqAxis = np.arange(0, fs, fs/N)

sinusoid = getDiscreteSinusoid(f, fs, np.cos, numberOfSamples=N)
fftOfSignal = abs(scipy.fftpack.fft(sinusoid))

thirdPlot.plot(sinusoid, 'r.-')
fourthPlot.plot(freqAxis, fftOfSignal, 'r.')

plt.tight_layout()
plt.show()
