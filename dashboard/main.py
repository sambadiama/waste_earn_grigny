import sys
print(sys.executable)
import re
import warnings
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
import affluence, gaspillage, commande, asso, homestats
st.set_page_config(layout="wide", page_title="WASTEARN APP")
  # Remplacez ceci par le chemin de votre logo
#st.image("WASTEARN_LOGO-removebg-preview.png", width=(50))  # Changer la largeur selon vos besoins
  

class MultiApp :

    def __init__(self) :
        self.apps = []
    def add_app(self,title,function):
        self.apps.append({"title": title,
                          "function": function})
    def run ():
        logo_path = "WASTEARN_LOGO-removebg-preview.png"  # Remplacez ceci par le chemin de votre logo
        st.image(logo_path, width=100)  # Changer la largeur selon vos besoins

        st.markdown("""
        <style>
            [data-testid=stSidebar] {
                background-color: #FFC300;
            }
        </style>
        """, unsafe_allow_html=True)

        with st.sidebar:
            logo_path = "WASTEARN_LOGO-SF-2.png" 
            logo_path2 = "WASTEARN_LOGO-Titre.png" 
            st.image(logo_path2, width=300)
            app = option_menu(
                menu_title='WASTEARN App',
                options=['Acceuil','W. Affluence','W. Gaspillage','W. Menu','W. Asso/Redistribution'],
                icons=['house-fill','person-circle','trash-fill','card-text','info-circle-fill'],
                menu_icon='WASTEARN_LOGO-SF Blanc.png',
                default_index=0,
                styles={
                    "container": {"padding": "5!important","background-color":'#69C649'},
                   
                     "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#FFC300"},
                     "nav-link-selected": {"background-color": "#0E2D23"},})
            st.image(logo_path, width=270)
              

        if app == "Acceuil":
            homestats.app()
        if app == "W. Affluence":
            affluence.app()    
        if app == "W. Gaspillage":
            gaspillage.app()        
        if app == 'W. Menu':
            commande.app()
        if app == 'W. Asso':
            asso.app()
     
    run()

    ### "icon": {"color": "white", "font-size": "23px"}, 'house-fill','person-circle','trash-fill','card-text','info-circle-fill'

