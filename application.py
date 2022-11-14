""" for each application """
import streamlit as st
import data
import helpers
from Equalizer import Equalizer

def app(application_type ):
    global dictionary
    """for the app chosed by the radio button in main.py"""
    with open("style.css")as css:
        st.markdown(f"<style>{css.read() }</style>", unsafe_allow_html=True)
    # st.markdown(application_type)
    file_uploaded = st.sidebar.file_uploader(label="upload", type=['wav'], label_visibility='collapsed')
    if file_uploaded:
        if application_type=='Vowels':
            dictionary=data.VOWEL
        elif application_type=='Music Instruments':
            dictionary= data.INSTRUMENT
        elif application_type=='General Signal':
            dictionary= data.GENERAL
        value = helpers.create_sliders_dicts(dictionary)
        sound_amplitude, sampling_rate = helpers.upload_file(file_uploaded)
        # helpers.plot_signal(sound_amplitude, sampling_rate)
        current_equalizer = Equalizer(sound_amplitude, sampling_rate)
        current_equalizer.to_frequency_domain()
        current_equalizer.equalize_frequency_range(dictionary, value )
        current_equalizer.inverse_frequency_domain()
        new_signal = current_equalizer.signal_temporary_amplitude
        sound_plot = sound_amplitude[:len(new_signal)]
        
        
        with st.expander("Studio"):
            columns1 = [1,1,1]
            col1,col2,col3 = st.columns(columns1)
            with col1:
                start_btn = st.button("Start")
            with col2:
                pause_btn= st.button("Pause")
            with col3:
                resume_btn= st.button("Resume")
            helpers.plotShow(sound_plot , new_signal,start_btn,pause_btn,resume_btn ,sampling_rate)
            helpers.changed_audio(new_signal, sampling_rate)
        