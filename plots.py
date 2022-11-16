import time
import altair as alt
import librosa
import librosa.display
import numpy as np
import pydub
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
@st.cache
def handle_uploaded_audio_file(uploaded_file):
    """_summary_
    Args:
        uploaded_file (_type_):a wav file the user wants to process
    Returns:
        the wav file as array 
    """
    a = pydub.AudioSegment.from_file(
        file=uploaded_file, format=uploaded_file.name.split(".")[-1])
    channel_sounds = a.split_to_mono()
    samples = [s.get_array_of_samples() for s in channel_sounds]
    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples[0].typecode).max
    return fp_arr[:, 0], a.frame_rate

def plot_transformation(file):
    """_summary_
    Args:
        file (_type_):a wav file the user wants to process
    Returns:
        the spectrogram of the file as figure
    """
    D = librosa.stft(file)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(S_db, x_axis='time', y_axis='linear', ax=ax)
    ax.set(title="Spectrogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    return st.pyplot(plt.gcf())

def show_spectrogram(file):
    """
    check whether there is file uploaded or not
    """
    if file is not None:
        y, sr = handle_uploaded_audio_file(file)
    plot_transformation(y)

##################################################animated plots###############################################

def plot_animation(df):
    brush = alt.selection_interval()
    chart1 = alt.Chart(df).mark_line().encode(
        x=alt.X('time', axis=alt.Axis(title='Time')),
        # y=alt.Y('amplitude', axis=alt.Axis(title='Amplitude')),
    ).properties(
        width=300,
        height=200
    ).add_selection(
        brush).interactive()

    figure = chart1.encode(
        y=alt.Y('amplitude', axis=alt.Axis(title='Amplitude'))) | chart1.encode(
        y=alt.Y('amplitude after processing',
                axis=alt.Axis(title='Amplitude after'))).add_selection(brush)

    return figure


def show_dynamic_plot(data, idata, start_btn, pause_btn, resume_btn, sr , application_type):

    if 'start' not in st.session_state:
        st.session_state['start'] = 0
    if 'size1' not in st.session_state:
        st.session_state['size1'] = 0
    if 'flag' not in st.session_state:
        st.session_state['flag'] = 1
    if 'time_start' not in st.session_state:
        st.session_state['time_start']=0

    max_time = len(data)/(sr)
    if max_time > 1:
        max_time = int(max_time)
    time1 = np.linspace(0, max_time, len(data))
    if application_type=='ECG':
        df = pd.DataFrame({'time': time1,
                       'amplitude': data,
                       'amplitude after processing': idata}, columns=[
        'time', 'amplitude', 'amplitude after processing'])
    else:    
        df = pd.DataFrame({'time': time1[::300],
                        'amplitude': data[:: 300],
                        'amplitude after processing': idata[::300]}, columns=[
            'time', 'amplitude', 'amplitude after processing'])
    N = df.shape[0]  # number of elements in the dataframe
    burst = 10      # number of elements (months) to add to the plot
    size = burst

    step_df = df.iloc[0:st.session_state.size1]
    if st.session_state.size1 == 0:
        step_df = df.iloc[0:N]

    lines = plot_animation(step_df)
    line_plot = st.altair_chart(lines)
    line_plot = line_plot.altair_chart(lines)

    # lines = plot_animation(df)
    # line_plot = st.altair_chart(lines)
    N = df.shape[0]  # number of elements in the dataframe
    burst = 10      # number of elements (months) to add to the plot
    size = burst  # size of the current dataset
    if start_btn:
        st.session_state.flag = 1
        for i in range(1, N):
            st.session_state.start = i
            step_df = df.iloc[0:size]
            lines = plot_animation(step_df)
            line_plot = line_plot.altair_chart(lines)
            size = i + burst
            st.session_state.size1 = size
            time.sleep(.000001)

    elif resume_btn:
        st.session_state.flag = 1
        for i in range(st.session_state.start, N):
            st.session_state.start = i
            step_df = df.iloc[0:size]
            lines = plot_animation(step_df)
            line_plot = line_plot.altair_chart(lines)
            st.session_state.size1 = size
            size = i + burst
            time.sleep(.000001)

    elif pause_btn:
        st.session_state.flag = 0
        step_df = df.iloc[0:st.session_state.size1]
        lines = plot_animation(step_df)
        line_plot = line_plot.altair_chart(lines)

    if st.session_state.flag == 1:
        for i in range(st.session_state.start, N):
            st.session_state.start = i
            step_df = df.iloc[0:size]
            lines = plot_animation(step_df)
            line_plot = line_plot.altair_chart(lines)
            st.session_state.size1 = size
            size = i + burst
            time.sleep(.000001)




