"""
the main class
"""
import numpy as np

# import scipy
# from scipy.fft import irfft, rfft, rfftfreq


class Equalizer():
    """ for the main functionality to equalize the inout signal
    """

    def __init__(self, signal_amplitude, sampling_rate=1):
        self.signal_amplitude = signal_amplitude
        self.sampling_rate = sampling_rate
        self.signal_temporary_amplitude = signal_amplitude
        self.frequency_magnitude = []
        self.frequency_temporary_magnitude = []
        self.frequency_phase = []
        self.frequency = []
        self.fft_parameters = []
###############################################################################################

    def inverse_frequency_domain(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        complex_parameters = np.multiply(
            self.frequency_temporary_magnitude, np.exp(np.multiply(1j, self.frequency_phase)))
        self.signal_temporary_amplitude = np.fft.irfft(complex_parameters)
        signal_temp = self.signal_temporary_amplitude
        return signal_temp
###############################################################################################

    def to_frequency_domain(self):
        """_summary_
        """
        self.frequency = np.fft.rfftfreq(
            len(self.signal_amplitude), 1 / self.sampling_rate)
        fft_parameters = np.fft.rfft(self.signal_amplitude)
        self.frequency_phase = np.angle(fft_parameters)
        self.frequency_magnitude = np.abs(fft_parameters)
        self.frequency_temporary_magnitude = np.abs(fft_parameters)
###############################################################################################

    def equalize_frequency_range(self, dictionary, slider_value,previous_value,default_value):
        """_summary_
        Args:
            dictionary (_type_): _description_
            slider_value (_type_): _description_
        """
        for slider_index, (key, value) in enumerate(dictionary.items()):
            for slider_index, (key ,value) in enumerate(dictionary.items()):
                for range in value:
                    if slider_value[slider_index]>-1:
                        if(slider_value[slider_index]<default_value):
                            index=np.where((self.frequency>range[0])&(self.frequency<range[1]))
                            hanning_window=((slider_value[slider_index])*np.hanning(range[1]-range[0]))
                            for i ,itr in zip(index,hanning_window):
                                self.frequency_temporary_magnitude[i]=  self.frequency_magnitude[i]*itr
                        elif (slider_value[slider_index]<default_value):
                            index=np.where((self.frequency>range[0])&(self.frequency<range[1]))
                            for i in zip(index):
                                self.frequency_temporary_magnitude[i]=  self.frequency_magnitude[i]*slider_value[slider_index]
 ##############################################################################################
