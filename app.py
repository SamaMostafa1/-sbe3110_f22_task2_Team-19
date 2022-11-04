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
    img = librosa.display.waveshow(y, sr=sr, x_axis="time", ax=ax)
    return plt.gcf()

# def plot_transformation(y, sr, transformation_name):
#     D = librosa.stft(y)  # STFT of y
#     S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
#     fig, ax = plt.subplots()
#     img = librosa.display.specshow(S_db, x_axis='time', y_axis='linear', ax=ax)
#     ax.set(title=transformation_name)
#     fig.colorbar(img, ax=ax, format="%+2.f dB")
#     return plt.gcf()

def spacing():
    st.markdown("<br></br>", unsafe_allow_html=True)

def plot_audio_transformations(y, sr):
    # st.markdown(f"<h4 style='text-align: center;'>Original</h5>",unsafe_allow_html=True)
    # st.pyplot(plot_transformation(y, sr, "Original"))
    st.markdown(f"<h4 style='text-align: center;'>Wave Plot </h5>",unsafe_allow_html=True)
    st.pyplot(plot_wave(y, sr))
    y = y
    sr = sr

def action(file):
    if file is not None:
        y, sr = handle_uploaded_audio_file(file)
    plot_audio_transformations(y, sr)

def main():
    music = st.sidebar.file_uploader(label="Select a file", type=[".wav"])
    if music is not None:
        action(music)
        st.sidebar.audio(music)
        song, sr = librosa.load(music)
        fequency_domain(song,sr,'freq',0.1)

def fequency_domain(signal,sr,title,f_ratio=1):
        freq=np.fft.fft(signal)
        freq_mag = np.absolute(freq)
        f = np.linspace(0, sr, len(freq_mag )) 
        fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
        fig.set_figheight(4)
        fig.set_figwidth(16)
        ax.set(title='Input audio')
        line = ax.plot(f, freq_mag)
        st.markdown(f"<h4 style='text-align: center;'>Frequency Plot </h5>",unsafe_allow_html=True)
        st.pyplot(fig)

if __name__ == "__main__":
    main()

hide_st_style =""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
                    </style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)