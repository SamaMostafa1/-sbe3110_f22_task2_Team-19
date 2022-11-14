"""
this file contains helper functions..
"""
import time

import altair as alt
################################## Essential imports ###################################
import librosa
import librosa.display
import numpy as np
import pandas as pd
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
    final = st.sidebar.audio(audio_, format='audio/wav')
    return audio_file
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

def create_sliders_dicts(dictionary):
    length = len(dictionary)
    slider_value = np.zeros(length)
    columns = np.zeros(length)
    columns = st.columns(length)
    column_index=0
    # with st.expander("Slider :"):
    for i in dictionary:
        with columns[column_index]:
                st.write(i)
                slider_value[column_index] = svs.vertical_slider(key=i,
                                                  step=1,
                                                  min_value=0,
                                                  max_value=100,
                                                  default_value=50,
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
            # y=alt.Y('amplitude', axis=alt.Axis(title='Amplitude')),
        ).properties(
            width=500,
            height=300
        ).add_selection(
            brush).interactive()
    
    figure = chart1.encode(
                  y=alt.Y('amplitude',axis=alt.Axis(title='Amplitude')))| chart1.encode(
                  y=alt.Y('amplitude after processing',axis=alt.Axis(title='Amplitude after'))).add_selection(
            brush)

    return figure


def plotShow(data, idata,start_btn,pause_btn,resume_btn,sr):

    if 'start' not in st.session_state:
        st.session_state['start']=0
    if 'size1' not in st.session_state:
        st.session_state['size1']=0
    if 'flag' not in st.session_state:
        st.session_state['flag']=1

    time1 = len(data)/(sr)
    if time1>1:
        time1 = int(time1)
    time1 = np.linspace(0,time1,len(data))   
    df = pd.DataFrame({'time': time1[::300], 
                        'amplitude': data[:: 300],
                        'amplitude after processing': idata[::300]}, columns=[
                        'time', 'amplitude','amplitude after processing'])
    N = df.shape[0]  # number of elements in the dataframe
    burst = 10      # number of elements (months) to add to the plot
    size = burst 
    
    step_df = df.iloc[0:st.session_state.size1]
    if st.session_state.size1 ==0:
        step_df = df.iloc[0:N]

    lines = plot_animation(step_df)
    line_plot = st.altair_chart(lines)
    line_plot= line_plot.altair_chart(lines)

    # lines = plot_animation(df)
    # line_plot = st.altair_chart(lines)
    N = df.shape[0]  # number of elements in the dataframe
    burst = 10      # number of elements (months) to add to the plot
    size = burst    #   size of the current dataset
    if start_btn:
        st.session_state.flag = 1
        for i in range(1, N):
            st.session_state.start=i
            step_df = df.iloc[0:size]
            lines = plot_animation(step_df)
            line_plot = line_plot.altair_chart(lines)
            size = i + burst 
            st.session_state.size1 = size
            time.sleep(.1)

    elif resume_btn: 
            st.session_state.flag = 1
            for i in range( st.session_state.start,N):
                st.session_state.start =i 
                step_df = df.iloc[0:size]
                lines = plot_animation(step_df)
                line_plot = line_plot.altair_chart(lines)
                st.session_state.size1 = size
                size = i + burst
                time.sleep(.000001)

    elif pause_btn:
            st.session_state.flag =0
            step_df = df.iloc[0:st.session_state.size1]
            lines = plot_animation(step_df)
            line_plot= line_plot.altair_chart(lines)



    if st.session_state.flag == 1:
        for i in range( st.session_state.start,N):
                st.session_state.start =i 
                step_df = df.iloc[0:size]
                lines = plot_animation(step_df)
                line_plot = line_plot.altair_chart(lines)
                st.session_state.size1 = size
                size = i + burst
                time.sleep(.000001)
                                
def get_index(specific_frequency ,sample_rate ,signal):
    return int((specific_frequency/(sample_rate/2))*len(signal))  # (freq(hz)/fmax)*len(signal)  => where is 50 hz in fft

def hanning (arr, range_length):
    result= []
    result= result[:len(arr)]
    for i in range(len(arr)):
        result[i]= np.hanning(range_length)[i]* arr[i]
        
    return result