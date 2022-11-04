"""
for each application
"""

import streamlit as st
import helpers
import Equalizer
def app (application_type):
    """for the app chosed by the radio button in main.py"""
    st.write(application_type)
    file_uploaded = st.file_uploader(label="",  type=[ 'wav']) 
    if file_uploaded:
        sound_amplitude,sampling_rate=helpers.upload_file( file_uploaded )
        helpers.plot_signal(sound_amplitude,sampling_rate)
        eq=Equalizer.Equalizer(sound_amplitude,sampling_rate)
        eq.to_frequency_domain()
        value=st.slider('value')
        eq.equalize_frequency_range( 0, 200,value)
        eq.inverse_frequency_domain()
        new_signal=eq.signal_temporary_amplitude
        st.write(new_signal)
        helpers.plot_signal(new_signal,sampling_rate)
        #helpers.changed_audio(new_signal,sampling_rate)