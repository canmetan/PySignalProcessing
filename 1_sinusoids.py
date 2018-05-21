# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# Sample execution for sampling sinusoids
# ____________________________________________________________________________


import numpy as np
import matplotlib.pyplot as plt
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


def setSinusoidGraphLabels(graphName):
    graphName.set_xlabel('n')
    graphName.set_ylabel('x(n)')


# An example execution
fig = plt.figure()
plt.suptitle("SAMPLING")

firstPlot = plt.subplot(211)
secondPlot = plt.subplot(212)

setSinusoidGraphLabels(firstPlot)
setSinusoidGraphLabels(secondPlot)

# 1 Hz signal 20 Hz sampling, taking 20 samples (=1 period) in total
firstPlot.set_title('1 Hz Signal, sampled @ 20 Hz, 1 second')
firstPlot.plot(getDiscreteSinusoid(1, 20, np.sin, numberOfSamples=20), 'r.-')

# 2 Hz signal 20 Hz sampling, taking 6 seconds of data (=6 period) in total
secondPlot.set_title('2 Hz Signal, sampled @ 20 Hz, 6 second')
secondPlot.plot(getDiscreteSinusoid(2, 25, np.sin, seconds=6), 'r.-')

plt.tight_layout()
plt.show()
