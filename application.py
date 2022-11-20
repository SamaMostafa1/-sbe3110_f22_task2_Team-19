""" for each application """
import librosa
import streamlit as st
import os.path
import data
import helpers
from Equalizer import Equalizer
from plots import show_dynamic_plot, show_spectrogram
import pandas as pd
if 'size1' not in st.session_state:
    st.session_state['size1'] =0
if 'start' not in st.session_state:
    st.session_state['start'] =0
if 'play' not in st.session_state:
    st.session_state.play =0
def app(application_type):
    """for the app chosed by the radio button in main.py"""
        
    with open("design.css")as f:
        st.markdown(f"<style>{f.read() }</style>",unsafe_allow_html=True)
    sliders,select=st.columns(2)
    if 'flag' not in st.session_state:
        st.session_state['flag'] = False
    if 'previous_slider_value' not in st.session_state:
            st.session_state['previous_slider_value'] = [] 

    # with open("style.css")as css:
    #     st.markdown(f"<style>{css.read() }</style>", unsafe_allow_html=True)
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
        elif application_type=='animals':
            dictionary= data.animals
        signal_view = st.radio(
            "Modes :", ('dynamic wave', 'spectrogram'), index=0, horizontal=True,
            label_visibility='collapsed')
        columns1 = [1, 1, 1,4]
        col_graph,col_empty=st.columns(2)
        columns2 = [1, 1]
        colu1, colu2 = st.columns(columns2)
        col1, col2,col3,col4 = st.columns(columns1)
        time=[]
        file_name= file_uploaded.name
        extension= os.path.splitext(file_name)[1][1:]
        if application_type == 'ECG' and extension=='csv':
            if file_uploaded is not None:
                global df
                try:
                    df = pd.read_csv(file_uploaded)
                except Exception as e:
                        df = pd.read_excel(file_uploaded)
                st.session_state.uploaded = df
                time = df.iloc[:, 0]
                amplitude = df.iloc[:, 1]
                sampling_rate = time[1]-time[0]
                n_samples = len(time)
                Fs = n_samples/10
                T = 1 / Fs
            current_equalizer = Equalizer(amplitude)
        elif extension=='wav':
            amplitude, sampling_rate = helpers.upload_file(file_uploaded)
            current_equalizer = Equalizer(amplitude, sampling_rate)
        current_equalizer.to_frequency_domain(application_type,time)
        if application_type == 'General Signal' :
            dictionary = helpers.general_signal_dictionary(
                current_equalizer.frequency, dictionary)
        if(current_equalizer):
            value = helpers.create_sliders_dicts(dictionary)
            current_equalizer.equalize_frequency_range(dictionary, value, 100)
            current_equalizer.inverse_frequency_domain()
            new_signal = current_equalizer.signal_temporary_amplitude   
            sound_plot = amplitude[:len(new_signal)]
            # with col1:
            #     pause_btn = st.button("Pause")
            with col2:
                start_btn = st.button("Start")
            # with col3:
            #     resume_btn = st.button("Resume")
            if application_type != 'ECG':
                final_file = helpers.changed_audio(new_signal, sampling_rate)
            with col_graph:
                if 'play' not in st.session_state:
                        st.session_state.play =0
                if signal_view == 'dynamic wave': 
                    show_dynamic_plot(sound_plot, new_signal, start_btn,
                                        sampling_rate,application_type)

                if signal_view == 'spectrogram':
                    if application_type=='ECG':
                        st.write('No spectrogram for ECG signals')
                    else:
                        with colu1:
                            show_spectrogram(file_uploaded)
                        with colu2:
                                show_spectrogram(final_file)