"""
the main class
"""
import numpy as np
from helpers import get_arr
from scipy.fft import rfft, irfft, rfftfreq


class Equalizer():
    ###############################################################################################
    def __init__(self, signal_amplitude, sampling_rate=1):
        # self.frequency_ranges=frequency_ranges
        self.signal_amplitude = signal_amplitude
        self.sampling_rate = sampling_rate
        # self.signal_time=signal_time
        self.signal_temporary_amplitude = signal_amplitude
        self.frequency_magnitude = []
        self.frequency_temporary_magnitude = []
        self.frequency_phase = []
        self.frequency = []
###############################################################################################

    def to_frequency_domain(self):
        self.frequency = rfftfreq(
            len(self.signal_amplitude), 1 / self.sampling_rate)
        fft_parameters = rfft(self.signal_amplitude)
        self.frequency_phase = np.angle(fft_parameters)
        self.frequency_magnitude = np.abs(fft_parameters)
        self.frequency_temporary_magnitude = np.abs(fft_parameters)
        # return self.temporary_frequency_magnitude, self.frequency_magnitude
###############################################################################################

    def equalize_frequency_range(self, dictionary, slider_value):
        k = 0
        for key in dictionary:
            arr = get_arr(self.frequency,dictionary[key][0], dictionary[key][1])
            x = np.random.pareto(arr)
            if slider_value[k] > -1:
                for freq in range(len(self.frequency)):
                    if  850< self.frequency[freq] <2800 :
                        self.frequency_temporary_magnitude[freq] = self.frequency_magnitude[freq] * slider_value[k]*x[freq]
            k += 1
###############################################################################################

    def inverse_frequency_domain(self):
        complex_parameters = np.multiply(
            self.frequency_temporary_magnitude, np.exp(np.multiply(1j, self.frequency_phase)))
        self.signal_temporary_amplitude = irfft(complex_parameters)
        signal_temp = self.signal_temporary_amplitude
        return signal_temp
###############################################################################################
