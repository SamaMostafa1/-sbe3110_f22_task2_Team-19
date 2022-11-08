import plotly.express as px
import streamlit as st
import pandas as pd
from plotly1 import plotly_events

df = pd.DataFrame(dict(
    x_axis = [i for i in range(50)],
    y_axis = [i for i in range(50)]
))

fig = px.line(        
        df, #Data Frame
        x = "x_axis", #Columns from the data frame
        y = "y_axis",
        title = "Line Plot"
)

value = plotly_events(fig)
st.write("Received", value)
    