# PySignalProcessing
This is just a personal project for implementing some of the signal processing concepts in python.

This is useful for:
- Beginners: so that they can get a grasp on some of the basic theories of signal processing. Play around with variables, see the effects of certain changes and get a solid foundation.
- Experts: who are either transitioning from Matlab into Python or simply for people who needs a recap in the basics.

This is not a single "project" per se. Each number coded python file is executable and will either plot or display some output.

### Comments
#### 1_sinusoids) Sample execution for sampling sinusoids
#### 2_dftAliasing) Sample execution that shows the aliasing of sinusoids. f + (k * fs) are aliased as f. In this example 3 + (2*100) = 203 Hz is aliased as 3 Hz. Notice that the magnitude of the FFT is (Amplitude * N) / 2
#### 3_phase) Shows the phase shift doesn't change the fft of a signal. sin(x) = cos(x - pi/2) ---> Cos right shift by pi/2 Notice that the phase shift doens't change the FFT.
#### 4_fftLeak) Non integer multiples of sampling frequency causing leakage.
#### 5_windowing) Effects of windowing on signals that have spectral leakage. Other types of signals can also be used.
#### 6_zeroPadding) Zero padding can be used to increase the fft resolution. Initial signal is 256 samples long. Second one was padded with 256 zeros = 512 samples. The third signal is padded with 512 additional samples: So it is 256 + (256 + 512) = 256 + 768 = 1024 samples long.
#### 7_dftGain) When we increase the size of the window, we can easily see the frequencies with a wider window even when there is noise. DFT magnitude will be higher.
#### 8_primitiveFilters) This is a demo of various filters and their frequency response. All filters contain the same number of samples with padded zeros if necessary. Green graph is a low-pass filter. Black graph is a band-pass filter. Red graph is a high-pass filter.
#### 9_filterWindowing) This is a demo of FIR filter design. We chose to have two pass bands in this filtering design. Red graph is our custom pass filter with rectangular window. Green graph is the custom pass filter with blackman window.
#### 10_remezWindowing) This is a demo of FIR filter design. We chose to have two pass bands in this filtering design. Blue  graph is the remez filter with rectangular window. Black graph is the remez with blackman window. Red graph is the remez filter with nuttall window.
#### 11_widebandSignal) This is just a demonstration for generating wide band signals.
# Original data, Histogram, FFT and Phase will be displayed.
#### 12_manualConvolution) In this script, we will manually convolve two signals. The manual convolution code is in the "common.py" file. So this script checks the integrity of the function and compares with the speed of the convolution provided by numpy (ours is faster).
#### 13_filteredWideband) This generates a wideband signal, convolves with two low pass filters. One of them is a manually generated low pass filter and the other one is generated with remez exchange algorithm. They are both windowed with blackman window. We will calculate the DFT and phase afterwards. Green graph is the original signal. Cyan is the convolution with manually constructed low pass filter. Black is the convolution with the remez low pass filter.