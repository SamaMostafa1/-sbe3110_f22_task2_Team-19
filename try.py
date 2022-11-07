# import numpy as np
# import librosa
# import librosa.display
# import streamlit as st
# from matplotlib import pyplot as plt
# import wavio
# from time import sleep
# from scipy.fft import rfft,irfft, rfftfreq
# import cmath
# signal_temporary_amplitude=[]
# st.session_state.iter = 0 if 'iter' not in st.session_state else st.session_state.iter
# st.session_state.data = [] if 'data' not in st.session_state else st.session_state.data
# file_uploaded = st.file_uploader(label="upload",  type=[ 'wav']) 
# if file_uploaded :  
#         file_details = {"FileName": file_uploaded.name,
#                         "FileType": file_uploaded.type,
#                         "FileSize": file_uploaded.size}
#         if file_details['FileType'] == 'audio/wav':         
#                 with open('Input/FileName', 'wb') as f:
#                     f.write(file_uploaded.getbuffer())
#                     st.subheader("Input audio:")
#                     audio_file = open('Input/FileName', 'rb')
#                     audio_bytes = audio_file.read()
#                     st.audio(audio_bytes, format='audio/wav')
#                     sound_amplitude, sampling_rate = librosa.load('Input/FileName') 
#                     fig, ax = plt.subplots()
#                     librosa.display.waveshow(sound_amplitude, sr=sampling_rate, x_axis="time",ax=ax)
#                     st.pyplot(fig)
#                     #fig, ax = plt.subplots()
#                     #fig=librosa.display.waveshow(sound_amplitude, sr=sampling_rate, x_axis="time")
#                     # chart=st.line_chart()
#                     # st.session_state.data.append(sound_amplitude)
#                     # for data in st.session_state.data:
#                     #     chart.add_rows(sound_amplitude)
#                     # stop = st.checkbox("Stop Update")
#                     # while  st.session_state.iter < 100:
#                     #     if stop:
#                     #         break
#                     #     # update the simulated chart
#                     #     chart.add_rows(sound_amplitude)
#                     #     st.session_state.data.append(sound_amplitude)
#                     #     sleep(1)
#                     #     st.session_state.iter += 1
#                     signal_temporary_amplitude=sound_amplitude
#                     frequency=rfftfreq(len( sound_amplitude),1/ sampling_rate)
#                     fft_parameters= rfft(sound_amplitude)
#                     frequency_phase = np.angle(fft_parameters)
#                     frequency_magnitude = np.abs(fft_parameters)
#                     temporary_frequency_magnitude = np.abs(fft_parameters)
#                     fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
#                     fig.set_figheight(4)
#                     fig.set_figwidth(16)
#                     ax.set(title='Input audio')
#                     line, = ax.plot(frequency, frequency_magnitude)
#                     #the_plot = st.pyplot(plt)
#                     st.pyplot(fig)
#                     points_per_freq = len(frequency) / (sampling_rate / 2)
#                     for i in range(len(frequency)):
#                         f_idx = int(points_per_freq * i)
#                         temporary_frequency_magnitude[f_idx] =frequency_magnitude[f_idx]*100
#                         if 500<i<2000 :
#                             f_idx = int(points_per_freq * i)
#                             temporary_frequency_magnitude[f_idx] =temporary_frequency_magnitude[f_idx]/30
#                             frequency_phase[f_idx]=frequency_phase[f_idx]/30
#                     fig2, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
#                     fig2.set_figheight(4)
#                     fig2.set_figwidth(16)
#                     ax.set(title='Input audio')
#                     line, = ax.plot(frequency,  temporary_frequency_magnitude)
#                     st.pyplot(fig2)
#                    # constructing fft coefficients again (from amplitudes and phases) after processing the amplitudes
#                     new_rfft_coeff = np.zeros((len(frequency),), dtype=complex)
#                     for f in frequency:
#                         try:
#                             f_idx = int(points_per_freq * f)
#                             new_rfft_coeff[f_idx]= temporary_frequency_magnitude[f_idx]*cmath.exp(1j * frequency_phase[f_idx])
#                         except:
#                             pass

#                     new_sig = irfft(new_rfft_coeff)
#                     # complex_parameters = np.multiply(
#                     # temporary_frequency_magnitude, np.exp(np.multiply(1j, frequency_phase)))
#                     # signal_ = np.fft.irfft(complex_parameters)
#                     # st.write("signal temp after irfft")
#                     # st.write(signal_temporary_amplitude)
#                     fig, ax = plt.subplots()
#                     librosa.display.waveshow( new_sig , sr=sampling_rate, x_axis="time",ax=ax)
#                     st.pyplot(fig)
#                     wavio.write("myfileout.wav",  new_sig , sampling_rate, sampwidth=1)
#                     audio_file = open('myfileout.wav', 'rb')
#                     audio_ = audio_file.read()
#                     st.audio(audio_, format='audio/wav')
                    # st.write(sound_amplitude)
                    # st.write(signal_temporary_amplitude)
       
                    # st.audio(myfileout.wav)
                
    # filtered=[]
    # filtered_out=[]
    # for i in range(len(x_axis_fourier)):
    #     if 600<x_axis_fourier[i]<700 or 1620<x_axis_fourier[i]<1820 or 2310<x_axis_fourier[i]<2510:
    #         filtered.append(0)
    #         filtered_out.append(fft_out[i])
    #     else:
    #         filtered_out.append(0)
    #         filtered.append(fft_out[i])
import numpy as np
import librosa
import librosa.display
import streamlit as st
from matplotlib import pyplot as plt
import wavio
from scipy.fft import rfft,irfft, rfftfreq
signal_temporary_amplitude=[]
file_uploaded = st.file_uploader(label="upload",  type=[ 'wav']) 
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
                    st.write("signal temp before any")
                    st.write(signal_temporary_amplitude)
                    frequency=rfftfreq(len( sound_amplitude),1/ sampling_rate)
                    fft_parameters= rfft(sound_amplitude)
                    frequency_phase = np.angle(fft_parameters)
                    frequency_magnitude = np.abs(fft_parameters)
                    temporary_frequency_magnitude = np.abs(fft_parameters)
                    fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
                    fig.set_figheight(4)
                    fig.set_figwidth(16)
                    ax.set(title='Input audio')
                    line, = ax.plot(frequency, frequency_magnitude)
                    #the_plot = st.pyplot(plt)
                    st.pyplot(fig)
                    for i in range(len(frequency)):
                        temporary_frequency_magnitude[i] =frequency_magnitude[i]*2
                        if 700<frequency[i]<2800 :
                            temporary_frequency_magnitude[i] =frequency_magnitude[i]/20
                            frequency_phase[i]=frequency_phase[i]/20
                    fig2, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
                    fig2.set_figheight(4)
                    fig2.set_figwidth(16)
                    ax.set(title='Input audio')
                    line, = ax.plot(frequency, temporary_frequency_magnitude)
                    st.pyplot(fig2)
                    complex_parameters = np.multiply(
                    temporary_frequency_magnitude, np.exp(np.multiply(1j, frequency_phase)))
                    signal_temporary_amplitude = irfft(complex_parameters)
                    st.write("signal temp after irfft")
                    st.write(signal_temporary_amplitude)
                    fig, ax = plt.subplots()
                    librosa.display.waveshow(signal_temporary_amplitude, sr=sampling_rate, x_axis="time",ax=ax)
                    st.pyplot(fig)
                    wavio.write("myfileout.wav", signal_temporary_amplitude, sampling_rate, sampwidth=1)
                    audio_file = open('myfileout.wav', 'rb')
                    audio_ = audio_file.read()
                    st.audio(audio_, format='audio/wav')
                    st.write(sound_amplitude)
                    st.write(signal_temporary_amplitude)
       
#                     #st.audio(myfileout.wav)
                