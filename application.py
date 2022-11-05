"""
for each application
"""

import streamlit as st
import helpers
from equalizer import Equalizer


def app(application_type):
    """for the app chosed by the radio button in main.py"""
    st.write(application_type)
    file_uploaded = st.file_uploader(label="upload", type=['wav'], label_visibility='collapsed')
    if file_uploaded:
        sound_amplitude, sampling_rate = helpers.upload_file(file_uploaded)
        helpers.plot_signal(sound_amplitude, sampling_rate)
        current_equalizer = Equalizer(sound_amplitude, sampling_rate)
        current_equalizer.to_frequency_domain()
        value = st.slider('value',0,200)
        current_equalizer.equalize_frequency_range(0 , 2000 , value)
        current_equalizer.inverse_frequency_domain()
        new_signal = current_equalizer.signal_temporary_amplitude
        helpers.plot_signal(new_signal, sampling_rate)
        helpers.changed_audio(new_signal,sampling_rate)
