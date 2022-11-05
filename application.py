"""
for each application
"""

import streamlit as st
import helpers
from Equalizer import Equalizer
import numpy as np

def app(application_type):
    with open("style.css")as f:
        st.markdown(f"<style>{f.read() }</style>",unsafe_allow_html=True)
    """for the app chosed by the radio button in main.py"""
    st.write(application_type)
    file_uploaded = st.file_uploader(label="upload", type=['wav'], label_visibility='collapsed')
    names=['a','b','c','d','e','f','g','h','i','j']
    #value=np.zeros(10)
    if file_uploaded:
        value=helpers.create_sliders(names,10)
        sound_amplitude, sampling_rate = helpers.upload_file(file_uploaded)
        helpers.plot_signal(sound_amplitude, sampling_rate)
        current_equalizer = Equalizer(sound_amplitude, sampling_rate)
        current_equalizer.to_frequency_domain()
        current_equalizer.equalize_frequency_range(0 , 4000 , value[0])
        current_equalizer.inverse_frequency_domain()
        new_signal = current_equalizer.signal_temporary_amplitude
        helpers.plot_signal(new_signal, sampling_rate)
        helpers.changed_audio(new_signal,sampling_rate)
