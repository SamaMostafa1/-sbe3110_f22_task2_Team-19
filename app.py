import io
import librosa
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
import librosa.display
from scipy.io import wavfile
import pydub

@st.cache
def handle_uploaded_audio_file(uploaded_file):
    a = pydub.AudioSegment.from_file(file=uploaded_file, format=uploaded_file.name.split(".")[-1])
    channel_sounds = a.split_to_mono()
    samples = [s.get_array_of_samples() for s in channel_sounds]
    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples[0].typecode).max
    return fp_arr[:, 0], a.frame_rate

def plot_wave(y, sr):
    fig, ax = plt.subplots()
    ax.set(title="Waveform")
    img = librosa.display.waveshow(y, sr=sr, ax=ax)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    return plt.gcf()

def plot_transformation(y, transformation_name):
    D = librosa.stft(y)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(S_db, x_axis='time', y_axis='linear', ax=ax)
    ax.set(title="Spectrogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    return plt.gcf()

def spacing():
    st.markdown("<br></br>", unsafe_allow_html=True)

def plot_audio_transformations(y, sr, music):
    cols = [1,1,1]
    col1,col2,col3 = st.columns(cols)
    with col1:
        st.pyplot(plot_transformation(y, "Original"))
    with col2:
        st.pyplot(plot_wave(y, sr))
    with col3:
        song, sr = librosa.load(music)
        fequency_domain(song,sr)
    y = y
    sr = sr

def action(file):
    if file is not None:
        y, sr = handle_uploaded_audio_file(file)
    plot_audio_transformations(y, sr, music)

def main1():
    if music is not None:
        st.markdown(f"<h1 style='text-align: center';>Input Signal</h1>",unsafe_allow_html=True)
        action(music)
        st.sidebar.audio(music)
        st.markdown(f"<h1 style='text-align: center';>Output Signal</h1>",unsafe_allow_html=True)

def fequency_domain(signal,sr):
        freq=np.fft.fft(signal)
        freq_mag = np.absolute(freq)
        f = np.linspace(0, sr, len(freq_mag )) 
        fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
        ax.set(title="Signal Spectrum")
        ax.plot(f, freq_mag)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        st.pyplot(fig)

if __name__ == "__main__":
    type = st.sidebar.radio("Mode :",('Uniform Range','Vowel','Musical Instrument','Biological Signal Abnormality'))
    if (type == 'Uniform Range' or type == 'Vowel' or type == 'Musical Instrument' ):
        music = st.sidebar.file_uploader(label="Select a file", type=".wav")
        if type == 'Uniform Range': main1()
        # elif type == 'Vowel': main2()
        # elif type == 'Musical Instrument': main3()
    else:
        medical_file = st.sidebar.file_uploader(label="", type=".csv")

hide_st_style =""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} </style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)