"""
this file contains helper functions..
"""
import math

################################## Essential imports ###################################
import librosa
import librosa.display
import numpy as np
import streamlit as st
import streamlit_vertical_slider as svs
import wavio
import pandas as pd
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
                amplitude, sampling_rate = librosa.load('Input/FileName')
                return amplitude, sampling_rate
            
        else :
                df = pd.read_csv(file_uploaded)
                st.session_state.uploaded = df
                time = st.session_state.uploaded.iloc[:, 0]
                amplitude = st.session_state.uploaded.iloc[:, 1]
                sampling_rate = time[1]-time[0]
                n_samples = len(time)
                sampling_rate = n_samples/10
                # T = 1 / Fs
                return amplitude, sampling_rate
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
def general_signal_dictionary (frequency ,dictionary ) :
    """_summary_

    Args:
        frequency (_type_): _description_
        dictionary (_type_): _description_

    Returns:
        _type_: _description_
    """
    bin_max_frequency_value = math.ceil(len(frequency)/11)
    i=10
    for key in dictionary:
        dictionary[key][0].append(frequency[(i-1)*bin_max_frequency_value])
        dictionary[key][0].append(frequency[(i)*bin_max_frequency_value])
        i-=1
    return dictionary


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
                                                            default_value=20,
                                                            slider_color='blue',
                                                            track_color='lightgray',
                                                            thumb_color='blue'
                                                            )
        column_index = column_index+1

    return slider_value
##############################################################################################