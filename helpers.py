"""
this file contains helper functions..
"""
################################## Essential imports ###################################
import librosa
import librosa.display
import numpy as np
import streamlit as st
import streamlit_vertical_slider as svs
from matplotlib import pyplot as plt
import wavio
import altair as alt
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
    librosa.display.waveshow(
        y=sound_amplitude, sr=sampling_rate, x_axis="time", ax=a_x)
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
def create_sliders(key,number_sliders):
    default_value=20
    slider_value=np.zeros(number_sliders)
    columns=np.zeros(number_sliders)
    columns=st.columns(number_sliders)
    for i in range(number_sliders):
        with columns[i]:
            st.markdown(key[i])
            slider_value[i]=svs.vertical_slider(key=key[i],
                                step=1, 
                                min_value=0, 
                                max_value=100,
                                default_value=default_value,
                                slider_color= 'blue',
                                track_color='lightgray',
                                thumb_color = 'blue' ,
                                )
    return slider_value,default_value


def create_sliders(key, number_sliders):
    slider_value = np.zeros(number_sliders)
    columns = np.zeros(number_sliders)
    columns = st.columns(number_sliders)
    for i in range(number_sliders):
        with columns[i]:
            st.markdown(key[i])
            slider_value[i] = svs.vertical_slider(key=key[i],
                                                  step=1,
                                                  min_value=0,
                                                  max_value=100,
                                                  default_value=0,
                                                  slider_color='blue',
                                                  track_color='lightgray',
                                                  thumb_color='blue',
                                                  )
    return slider_value

def get_dictionary_length(dictionary):
    length=0
    for key in dictionary:
        length+=1
    return length


def create_sliders_dicts(dictionary):
    length = len(dictionary)
    length= get_dictionary_length(dictionary)    
    slider_value = np.zeros(length)
    columns = np.zeros(length)
    columns = st.columns(length)
    column_index=0
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
            column_index= column_index+1
            
    return slider_value
##############################################################################################

def plot_animation(df):
    brush = alt.selection_interval()
    chart1 = alt.Chart(df).mark_line().encode(
            x=alt.X('time', axis=alt.Axis(title='Time')),
            y=alt.Y('amplitude', axis=alt.Axis(title='Amplitude')),
        ).properties(
            width=500,
            height=300
        ).add_selection(
            brush
        )
    chart2 = alt.Chart(df).mark_line().encode(
        x=alt.X('time', axis=alt.Axis(title='Time')),
        y=alt.Y('amplitude after processing', axis=alt.Axis(title='Amplitude after processing')),
    ).properties(
        width=500,
        height=300
    ).add_selection(
        brush
    )
    figure =alt.hconcat(
    chart1,
    chart2
    ).resolve_scale(
        x='shared'
    )
    # print(typeOf(figure))
    return figure



def get_arr(frequency ,lower, upper):
        arr=[]
        for freq in range(len(frequency)):
                if lower< frequency[freq] < upper:
                    arr.append(frequency[freq])
        return arr
