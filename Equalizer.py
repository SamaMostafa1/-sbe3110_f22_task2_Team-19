"""
the main class
"""
import numpy as np

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
        self.frequency = np.fft.rfftfreq(len(
            self.signal_amplitude), 1 / self.sampling_rate)[:len(self.signal_amplitude)//2]
        fft_parameters = np.fft.fft(self.signal_amplitude)[
            :len(self.signal_amplitude)//2]
        self.frequency_phase = np.angle(fft_parameters)
        self.frequency_magnitude = np.abs(fft_parameters)[
            :len(self.signal_amplitude)//2]
        self.frequency_temporary_magnitude = np.abs(
            fft_parameters)[:len(self.signal_amplitude)//2]
        # return self.temporary_frequency_magnitude, self.frequency_magnitude
###############################################################################################

    def equalize_frequency_range(self, start , end , slider_value):
        for freq in range(len(self.frequency)):
            if start< self.frequency[freq] < end:
                self.frequency_temporary_magnitude[freq] = self.frequency_magnitude[freq]*slider_value
###############################################################################################

    def inverse_frequency_domain(self):
        complex_parameters = np.multiply(
        self.frequency_temporary_magnitude, np.exp(np.multiply(1j, self.frequency_phase)))
        self.signal_temporary_amplitude = np.fft.irfft(complex_parameters)
        signal_temp=self.signal_temporary_amplitude
        return signal_temp
###############################################################################################
