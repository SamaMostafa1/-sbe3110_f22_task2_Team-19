from email.policy import default
from logging import exception
from re import I
from tkinter import HORIZONTAL, Menu
from turtle import width
import streamlit as st
from streamlit_option_menu import option_menu
from scipy.interpolate import CubicSpline
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins
from scipy.io import wavfile
import librosa
import io
import librosa.display
import pylab
import scipy
import random
import streamlit as st
import matplotlib.pylab as plt 
import numpy as np
from numpy import fft
from scipy.io import loadmat
import plotly.express as px
from test import inverse



def inverse (amp , phase) :
       complex_parameters = np.multiply( amp, np.exp(np.multiply(1j, phase)))
       signal_temporary_amplitude =fft.irfft(complex_parameters)
       
       return signal_temporary_amplitude
    
    
       
       
if 'factor' not in st.session_state:  
    factor1 = st.sidebar.slider(label="factor1",min_value=0.0,max_value=5.0,step=0.1,value=1.0)
    factor2 = st.sidebar.slider(label="factor2",min_value=0.0,max_value=5.0,step=0.1,value=1.0)
    factor3 = st.sidebar.slider(label="factor3",min_value=0.0,max_value=5.0,step=0.1,value=1.0)
    factor4 = st.sidebar.slider(label="factor4",min_value=0.0,max_value=5.0,step=0.1,value=1.0)
    factor5 = st.sidebar.slider(label="factor5",min_value=0.0,max_value=5.0,step=0.1,value=1.0)
    
# ####################################

uploaded_file = st.sidebar.file_uploader( label="Upload your  file", type=['csv', 'xlsx'])
    
if uploaded_file is not None:
       global df
       try:
        df = pd.read_csv(uploaded_file)
       except Exception as e:
              df = pd.read_excel(uploaded_file)
       st.session_state.uploaded = df

#      if 'uploaded_file' in st.session_state:
       time = st.session_state.uploaded.iloc[:, 0]
       amplitude = st.session_state.uploaded.iloc[:, 1]
       sample_period = time[1]-time[0]
       n_samples = len(time)
       Fs = n_samples/10
       T = 1 / Fs
       Time=np.linspace(0,n_samples*T,n_samples)

       fig = px.line(x=Time, y=amplitude)
       st.plotly_chart(fig,use_container_width=True)
###fft
   
       fft_frequencies = np.fft.rfftfreq(n_samples, sample_period)
       fft_paramerers = np.fft.rfft(amplitude)
       fft_magnitudes = np.abs(fft_paramerers)
       fft_phase = np.angle(fft_paramerers)
       # fig = px.line(x=fft_frequencies, y=fft_magnitudes)
       # st.plotly_chart(fig,use_container_width=True)

       for i in range(len(fft_frequencies)):
              for j in range(len(fft_magnitudes)):
                     if i == j and fft_frequencies[i]==0:
                            fft_magnitudes[j:j+10] = fft_magnitudes[j]*factor1
                     if i == j and 10>fft_frequencies[i]>0:
                            fft_magnitudes[j:j+10] = fft_magnitudes[j]*factor2   
                     if i == j and 90>fft_frequencies[i]>110:
                            fft_magnitudes[j:j+10] = fft_magnitudes[j]*factor3
                     if i == j and fft_frequencies[i]==-0.000967697097744361:
                            fft_magnitudes[j:j+10] = fft_magnitudes[j]*factor4
                     if i == j and fft_frequencies[i]==-6.265664661654136e-05:
                            fft_magnitudes[j:j+10] = fft_magnitudes[j]*factor5
                     




       ###inverse
       signal_amp= inverse(fft_magnitudes,fft_phase)
       fig_inv=px.line(x=Time,y=signal_amp).update_layout(xaxis_title='time(sec)')
       st.plotly_chart(fig_inv,use_container_width=True)
              
     



    
    
    
   











