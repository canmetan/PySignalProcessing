# Author: Can Metan
# GPL v3 License
# ____________________________________________________________________________
# In this script, we will manually convolve two signals. The manual convolution
# code is in the "common.py" file. So this script checks the integrity of the
# function and compares with the speed of the convolution provided by numpy.
# ____________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
import sys
import common
import time

# Assert that the user is using python above version 3.1
assert sys.version_info >= (3, 1)


# Testing code from the Richard Lyons Signal Processing book version 3.
xk = [1.0, 2.0, 3.0]
hk = [1.0, 1.0, 1.0, 1.0]

resultingList = common.convolve(hk, xk)
print('Convolving x(k): ', xk)
print('with h(k): ', hk)
print("\nIn-house convolution function result: ", resultingList)
print("\nStandard convolution function result: ", np.convolve(xk, hk).tolist())

print('\nTime it takes to run 1000000 in-house convolutions:')
start_time = time.time()
i = 0
while (i < 1000000):
    resultingList = common.convolve(hk, xk)
    i += 1
print(time.time() - start_time)


print('\nTime it takes to run 1000000 standard convolutions:')
start_time = time.time()
i = 0
while (i < 1000000):
    resultingList = np.convolve(xk, hk).tolist()
    i += 1
print(time.time() - start_time)

print('\nWeird!')
