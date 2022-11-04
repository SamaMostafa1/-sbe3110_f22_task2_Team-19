import numpy as np
import librosa
import librosa.display
import streamlit as st
from matplotlib import pyplot as plt
import wavio
from scipy.io.wavfile import write
import soundfile as sf

signal_temporary_amplitude=[]
file_uploaded = st.file_uploader(label="",  type=[ 'wav']) 
if file_uploaded :  
        file_details = {"FileName": file_uploaded.name,
                        "FileType": file_uploaded.type,
                        "FileSize": file_uploaded.size}
        if file_details['FileType'] == 'audio/wav':         
                with open('Input/FileName', 'wb') as f:
                    f.write(file_uploaded.getbuffer())
                    st.subheader("Input audio:")
                    audio_file = open('Input/FileName', 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/wav')
                    sound_amplitude, sampling_rate = librosa.load('Input/FileName') 
                    fig, ax = plt.subplots()
                    librosa.display.waveshow(sound_amplitude, sr=sampling_rate, x_axis="time",ax=ax)
                    st.pyplot(fig)
                    signal_temporary_amplitude=sound_amplitude
                    frequency=np.fft.rfftfreq(len( sound_amplitude),1/ sampling_rate)[:len(sound_amplitude)//2]
                    fft_parameters= np.fft.fft(sound_amplitude)[:len(sound_amplitude)//2]
                    frequency_phase = np.angle(fft_parameters)
                    frequency_magnitude = np.abs(fft_parameters)[:len(sound_amplitude)//2]
                    temporary_frequency_magnitude = np.abs(fft_parameters)
                    fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
                    fig.set_figheight(4)
                    fig.set_figwidth(16)
                    ax.set(title='Input audio')
                    line, = ax.plot(frequency, frequency_magnitude)
                    #the_plot = st.pyplot(plt)
                    st.pyplot(fig)
                    for i in range(len(frequency)):
                        if 0<frequency[i]<4000 :
                            temporary_frequency_magnitude[i] =frequency_magnitude[i]*0
                    fig2, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
                    fig2.set_figheight(4)
                    fig2.set_figwidth(16)
                    ax.set(title='Input audio')
                    line, = ax.plot(frequency, temporary_frequency_magnitude[:len(sound_amplitude)//2])
                    st.pyplot(fig2)
                    complex_parameters = np.multiply(
                    temporary_frequency_magnitude, np.exp(np.multiply(1j, frequency_phase)))
                    signal_temporary_amplitude = np.fft.irfft(complex_parameters)
                    fig, ax = plt.subplots()
                    librosa.display.waveshow(signal_temporary_amplitude, sr=sampling_rate, x_axis="time",ax=ax)
                    st.pyplot(fig)
                    wavio.write("myfileout.wav", signal_temporary_amplitude, sampling_rate, sampwidth=1)
                    audio_file = open('myfileout.wav', 'rb')
                    audio_ = audio_file.read()
                    st.audio(audio_, format='audio/wav')
                      
                    #st.audio(myfileout.wav)
                
    # filtered=[]
    # filtered_out=[]
    # for i in range(len(x_axis_fourier)):
    #     if 600<x_axis_fourier[i]<700 or 1620<x_axis_fourier[i]<1820 or 2310<x_axis_fourier[i]<2510:
    #         filtered.append(0)
    #         filtered_out.append(fft_out[i])
    #     else:
    #         filtered_out.append(0)
    #         filtered.append(fft_out[i])