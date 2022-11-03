"""
this file contains the ui & it is where the the app starts the run ..
"""
import streamlit as st  # 🎈 data web app development
from application import app
# import plotly.graph_objects as plot


# general styling and tab name
st.set_page_config(
    page_title="Equalizer Studio",
    page_icon="✅",
    layout="wide",
)

APP_1 = 'first app'
APP_2= 'second app'
APP_3 = 'third app'
APP_4 = 'forth app'
applications = st.radio('applications' ,(APP_1, APP_2 , APP_3  , APP_4  ),
                        index=0, horizontal=True, label_visibility='collapsed' )


if applications == APP_1:
    app(APP_1)
if applications == APP_2:
    app(APP_2)
if applications == APP_3:
    app(APP_3)
if applications == APP_4:
    app(APP_4)
