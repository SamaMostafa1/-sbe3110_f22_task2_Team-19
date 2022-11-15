"""
this file contains helper functions..
"""
################################## Essential imports ###################################
import librosa
import librosa.display
import numpy as np
import streamlit as st
import streamlit_vertical_slider as svs
import wavio
from matplotlib import pyplot as plt

################################## Functions defination ################################


def upload_file(file_uploaded):
    """_summary_
    Args:
        file_uploaded (_type_):a wav file the user wants to process
    Returns:
        _type_: the signal amplitude and the sample rate
    """
    if file_uploaded:
        file_details = {"FileName": file_uploaded.name,
                        "FileType": file_uploaded.type,
                        "FileSize": file_uploaded.size}
        if file_details['FileType'] == 'audio/wav':
            with open('Input/FileName', 'wb') as file:
                file.write(file_uploaded.getbuffer())
                st.sidebar.subheader("Input audio :")
                audio_file = open('Input/FileName', 'rb')
                audio_bytes = audio_file.read()
                st.sidebar.audio(audio_bytes, format='audio/wav')
                sound_amplitude, sampling_rate = librosa.load('Input/FileName')
                return sound_amplitude, sampling_rate
########################################################################################


def plot_signal(sound_amplitude, sampling_rate):
    """_summary_
    Args:
        sound_amplitude (list): the signal amplitude
        sampling_rate (number): the sample rate
    """
    fig, a_x = plt.subplots()
    librosa.display.waveshow(
        y=sound_amplitude, sr=sampling_rate, x_axis="time", ax=a_x)
    st.pyplot(fig)
########################################################################################


def changed_audio(signal_changed_amplitude, sampling_rate):
    """_summary_
    Args:
        signal_changed_amplitude (list): the signal amplitude _after processing_
        sampling_rate (number): sample rate
    Returns:
        audio_file (wav): the modified file
    """
    wavio.write("myfileout.wav", signal_changed_amplitude,
                sampling_rate, sampwidth=1)
    audio_file = open('myfileout.wav', 'rb')
    st.sidebar.subheader("Output audio :")
    audio_ = audio_file.read()
    st.sidebar.audio(audio_, format='audio/wav')
    return audio_file
########################################################################################


# def create_sliders(key, number_sliders):
#     default_value = 20
#     slider_value = np.zeros(number_sliders)
#     columns = np.zeros(number_sliders)
#     columns = st.columns(number_sliders)
#     for i in range(number_sliders):
#         with columns[i]:
#             st.markdown(key[i])
#             slider_value[i] = svs.vertical_slider(key=key[i],
#                                                   step=1,
#                                                   min_value=0,
#                                                   max_value=100,
#                                                   default_value=default_value,
#                                                   slider_color='blue',
#                                                   track_color='lightgray',
#                                                   thumb_color='blue',
#                                                   )
#     return slider_value, default_value


def create_sliders_dicts(dictionary):
    """_summary_

    Args:
        dictionary (_type_): _description_

    Returns:
        _type_: _description_
    """
    length = len(dictionary)
    slider_value = np.zeros(length)
    columns = np.zeros(length)
    columns = st.columns(length)
    column_index = 0
    # with st.expander("Slider :"):
    for i in dictionary:
        with columns[column_index]:
            st.write(i)
            slider_value[column_index] = svs.vertical_slider(key=i,
                                                             step=1,
                                                             min_value=0,
                                                             max_value=100,
                                                             default_value=0,
                                                             slider_color='blue',
                                                             track_color='lightgray',
                                                             thumb_color='blue'
                                                             )
        column_index = column_index+1

    return slider_value
##############################################################################################
