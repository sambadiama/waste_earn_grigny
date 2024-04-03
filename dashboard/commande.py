import sys
print(sys.executable)
import re
import warnings
from datetime import date, datetime, timedelta


import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

def app():
    #st.write('W. Menu')
    st.markdown(
    f'<div style="background-color:#0E2D23; padding: 2px; border-radius: 5px;">'
    '<h1 style="color: white;font-size: 18px;">W. Menu</h1>'
    '</div>',
    unsafe_allow_html=True
)

    st.markdown(
    f'<h1 style="color: #0E2D23; font-size: 24px;">Affichage du menu du jour</h1>', 
    unsafe_allow_html=True
    )

    st.markdown(
    f'<h1 style="color: #0E2D23; font-size: 24px;">Remplissage du menu</h1>', 
    unsafe_allow_html=True
    )