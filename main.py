"""
this file contains the ui & it is where the the app starts the run ..
"""
import streamlit as st  # 🎈 data web app development
from application import app
# import plotly.graph_objects as plot


# general styling and tab name
st.set_page_config(page_title="Equalizer Studio",page_icon="🎚️",layout="wide")

APP_1 = "General Signal"
APP_2 = 'Vowels'
APP_3 = 'Music Instruments'
APP_4 = 'forth app'
applications = st.sidebar.radio("Modes :" ,(APP_1, APP_2 , APP_3  , APP_4),index=0, horizontal=True)
if applications == APP_1:
    app(APP_1)
if applications == APP_2:
    app(APP_2)
if applications == APP_3:
    app(APP_3)
if applications == APP_4:
    app(APP_4)

# hide_st_style =""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} </style>"""
# st.markdown(hide_st_style, unsafe_allow_html=True)
