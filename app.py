import io
import librosa
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
import librosa.display
from scipy.io import wavfile
import plotly.express as px
def fequency_domain(signal,sr,title,f_ratio=1):
        freq=np.fft.fft(signal)
        freq_mag = np.absolute(freq)
        f = np.linspace(0, sr, len(freq_mag )) 
        fig=px.line(x=f, y=freq_mag) 
        #st.plotly_chart(fig,use_container_width=True)
file_uploader = st.sidebar.file_uploader(label="",  type=[ 'wav'])
if file_uploader is not None:  # File > 0 bytes
        file_details = {"FileName": file_uploader.name,
                        "FileType": file_uploader.type,
                        "FileSize": file_uploader.size}
        st.write(file_details)
        #######################
        # WAV UPLOADED FILE
        #######################
        if file_details['FileType'] == 'audio/wav':         
                with open('Input/FileName', 'wb') as f:
                                f.write(file_uploader.getbuffer())
                                st.subheader("Input audio:")
                                audio_file = open('Input/FileName', 'rb')
                                audio_bytes = audio_file.read()
                                st.audio(audio_bytes, format='audio/wav')
                                song, sr = librosa.load('Input/FileName')
                                fequency_domain(song,sr,'freq',0.1)

        