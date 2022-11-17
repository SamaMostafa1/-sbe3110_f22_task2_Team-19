""" for each application """
import streamlit as st

import data
import helpers
from equalizer import Equalizer
from plots import show_dynamic_plot, show_spectrogram
import librosa
def app(application_type):
    """for the app chosed by the radio button in main.py"""
        
    with open("design.css")as f:
        st.markdown(f"<style>{f.read() }</style>",unsafe_allow_html=True)
    sliders,select=st.columns(2)
    file_uploaded = st.sidebar.file_uploader(label="upload",
                                            type=['wav','csv'], label_visibility='collapsed')
    if file_uploaded:
        if application_type == 'Vowels':
            dictionary = data.VOWEL
        elif application_type == 'Music Instruments':
            dictionary = data.INSTRUMENT
        elif application_type == 'General Signal':
            dictionary = data.GENERAL
        elif application_type=='ECG':
            dictionary= data.ECG
        elif application_type=='Change voice':
            dictionary= data.Change_voice
        signal_view = st.radio(
            "Modes :", ('dynamic wave', 'spectrogram'), index=0, horizontal=True,
            label_visibility='collapsed')
        columns1 = [1, 1, 1,5]
        col_graph,col_empty=st.columns(2)
        columns2 = [1, 1]
        colu1, colu2 = st.columns(columns2)
        col1, col2,col3,col4 = st.columns(columns1)
        amplitude, sampling_rate = helpers.upload_file(file_uploaded)
        
        if application_type != 'Change voice':
                current_equalizer = Equalizer(amplitude, sampling_rate)
                current_equalizer.to_frequency_domain()
                if application_type == 'General Signal' :
                    dictionary = helpers.general_signal_dictionary(
                        current_equalizer.frequency, dictionary)
                value = helpers.create_sliders_dicts(dictionary)
                current_equalizer.equalize_frequency_range(dictionary, value,20)
                current_equalizer.inverse_frequency_domain()
                new_signal = current_equalizer.signal_temporary_amplitude
                sound_plot = amplitude[:len(new_signal)]
                ECG_plot = amplitude[:len(new_signal)]
        else:
            new_signal = librosa.effects.pitch_shift(amplitude,sr=sampling_rate,n_steps=6)    
            sound_plot = amplitude[:len(new_signal)]

        final_file = helpers.changed_audio(new_signal, sampling_rate)
        with col_graph:
            if signal_view == 'dynamic wave':
                with col1:
                    start_btn = st.button("Start")
                with col2:
                    pause_btn = st.button("Pause")
                with col3:
                    resume_btn = st.button("Resume")
                show_dynamic_plot(sound_plot, new_signal, start_btn,
                                pause_btn, resume_btn, sampling_rate, application_type)  
            if signal_view == 'spectrogram':    
                if application_type=='ECG':
                    st.write('No spectrogram for ECG signals')
                else:
                    with colu1:
                        show_spectrogram(file_uploaded)
                    with colu2:
                            show_spectrogram(final_file)