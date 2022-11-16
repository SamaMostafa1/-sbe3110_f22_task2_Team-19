""" for each application """
import streamlit as st

import data
import helpers
from Equalizer import Equalizer
from plots import show_dynamic_plot, show_spectrogram
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
                                            type=['wav'], label_visibility='collapsed')
    if file_uploaded:
        if application_type == 'Vowels':
            dictionary = data.VOWEL
        elif application_type == 'Music Instruments':
            dictionary = data.INSTRUMENT
        elif application_type == 'General Signal':
            dictionary = data.GENERAL
        signal_view = st.radio(
            "Modes :", ('dynamic wave', 'spectrogram'), index=0, horizontal=True,
            label_visibility='collapsed')
        columns1 = [1, 1, 1]
        col_graph,col_empty=st.columns(2)
        columns2 = [1, 1]
        colu1, colu2 = st.columns(columns2)
        col1, col2,col3 = st.columns(columns1)
        sound_amplitude, sampling_rate = helpers.upload_file(file_uploaded)
        current_equalizer = Equalizer(sound_amplitude, sampling_rate)
        current_equalizer.to_frequency_domain()
        if application_type == 'General Signal' and st.session_state.flag is False:
            dictionary = helpers.general_signal_dictionary(
                current_equalizer.frequency, dictionary)
            st.session_state.flag = True
        value = helpers.create_sliders_dicts(dictionary)
        st.write(value )
        st.session_state.previous_slider_value=st.session_state.previous_slider_value
        st.write(st.session_state.previous_slider_value)
        current_equalizer.equalize_frequency_range(dictionary, value,st.session_state.previous_slider_value,20)
        st.session_state.previous_slider_value=value
        current_equalizer.inverse_frequency_domain()
        new_signal = current_equalizer.signal_temporary_amplitude
        sound_plot = sound_amplitude[:len(new_signal)]
        with col1:
            pause_btn = st.button("Pause")
        with col2:
            start_btn = st.button("Start")
        with col3:
            resume_btn = st.button("Resume")

        final_file = helpers.changed_audio(new_signal, sampling_rate)
        with col_graph:
            if signal_view == 'dynamic wave':
                show_dynamic_plot(sound_plot, new_signal, start_btn,
                                pause_btn, resume_btn, sampling_rate)

            if signal_view == 'spectrogram':

                with colu1:
                    show_spectrogram(file_uploaded)
                with colu2:
                        show_spectrogram(final_file)
