"""
this file contains helper functions..
"""
################################## Essential imports ###################################
import librosa
import librosa.display
import streamlit as st
from matplotlib import pyplot as plt
import wavio
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
                st.subheader("Input audio:")
                audio_file = open('Input/FileName', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
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
    librosa.display.waveshow(y=sound_amplitude, sr=sampling_rate,x_axis="time" , ax=a_x )
    st.pyplot(fig)
########################################################################################


def changed_audio(signal_changed_amplitude, sampling_rate):
    """_summary_
    Args:
        signal_changed_amplitude (list): the signal amplitude _after processing_
        sampling_rate (number): sample rate
    """
    wavio.write("myfileout.wav", signal_changed_amplitude,
                sampling_rate, sampwidth=1)
    audio_file = open('myfileout.wav', 'rb')
    audio_ = audio_file.read()
    st.audio(audio_, format='audio/wav')
########################################################################################
