"""
for each application
"""

import streamlit as st
import helpers
from equalizer import Equalizer
import data

def app(application_type ):
    """for the app chosed by the radio button in main.py"""
    with open("style.css")as css:
        st.markdown(f"<style>{css.read() }</style>", unsafe_allow_html=True)
    st.write(application_type)
    file_uploaded = st.file_uploader(
        label="upload", type=['wav'], label_visibility='collapsed')
    # names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    # value=np.zeros(10)
    if file_uploaded:
        # value = helpers.create_sliders_dicts(names, 10)
        data_range = data.INSTRUMENT_FREQRANGE_DICTIONARY
        value = helpers.create_sliders_dicts(data_range)
        sound_amplitude, sampling_rate = helpers.upload_file(file_uploaded)
        helpers.plot_signal(sound_amplitude, sampling_rate)
        current_equalizer = Equalizer(sound_amplitude, sampling_rate)
        current_equalizer.to_frequency_domain()
        current_equalizer.equalize_frequency_range(data_range, value)
    
        # current_equalizer.equalize_frequency_range(data.INSTRUMENT_FREQRANGE_DICTIONARY, value[0])
        current_equalizer.inverse_frequency_domain()
        new_signal = current_equalizer.signal_temporary_amplitude
        helpers.plot_signal(new_signal, sampling_rate)
        helpers.changed_audio(new_signal, sampling_rate)
        