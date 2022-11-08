"""
for each application
"""
import streamlit as st
import helpers
from Equalizer import Equalizer
import data
import numpy as np
import pandas as pd

def app(application_type ):
    """for the app chosed by the radio button in main.py"""
    with open("style.css")as css:
        st.markdown(f"<style>{css.read() }</style>", unsafe_allow_html=True)
    st.write(application_type)
    file_uploaded = st.file_uploader(
        label="upload", type=['wav'], label_visibility='collapsed')
    # names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    # value=np.zeros(10)
    if file_uploaded:
        # value = helpers.create_sliders_dicts(names, 10)
        data_range = data.INSTRUMENT_FREQRANGE_DICTIONARY
        value = helpers.create_sliders_dicts(data_range)
        sound_amplitude, sampling_rate = helpers.upload_file(file_uploaded)
        helpers.plot_signal(sound_amplitude, sampling_rate)
        current_equalizer = Equalizer(sound_amplitude, sampling_rate)
        current_equalizer.to_frequency_domain()
        current_equalizer.equalize_frequency_range(data_range, value)
    
        # current_equalizer.equalize_frequency_range(data.INSTRUMENT_FREQRANGE_DICTIONARY, value[0])
        current_equalizer.inverse_frequency_domain()
        new_signal = current_equalizer.signal_temporary_amplitude
        helpers.plot_signal(new_signal, sampling_rate)
        helpers.changed_audio(new_signal, sampling_rate)
        
        time1 = np.linspace(0,1,len(new_signal))
        
        sound_plot = sound_amplitude[:len(new_signal)]
        df = pd.DataFrame({'time': time1[::30], 'amplitude': sound_plot[:: 30], 'amplitude after processing': new_signal[::30]}, columns=[
        'time', 'amplitude','amplitude after processing'])
 
        lines = helpers.plot_animation(df)
        line_plot = st.altair_chart(lines)
        col1,col2 = st.columns(2)
        start_btn = col1.button('Start')
        pause_btn = col2.button('Pause')
        N=0
        if start_btn:
            N = df.shape[0]  # number of elements in the dataframe
            burst = 1      # number of elements (months) to add to the plot
            size = burst    # size of the current dataset
    
        for i in range(1, N):
            step_df = df.iloc[0:size]
            lines = helpers.plot_animation(step_df)
            line_plot = line_plot.altair_chart(lines)
            size = i + burst
            if size >= N:
                size = N - 1
                if pause_btn:
                    size = 0
        
        