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
    #st.write('W. Gaspillage')
    st.markdown(
    f'<div style="background-color:#0E2D23; padding: 2px; border-radius: 5px;">'
    '<h1 style="color: white;font-size: 18px;">W. Gaspillage</h1>'
    '</div>',
    unsafe_allow_html=True)
    ECOLE_TYPES = [
        "Maternelles",
        "Elementaires",
    ]
    NOM_ECOLE_MATERNELLE = [
        "BBD / PETITE SIRENE",
        "CENDRILLON",
        "CHAPERON ROUGE",
        "CHAT BOTTE LANGEVIN",
        "JEAN MOULIN",
        "BELIER / CERF (DEDALE)",
        "LANGEVIN",
        "BUFFLE /PEGASE",
        "LICORNE",
        "TILLEULS",
        "MINOTAURE",
        "ANGELA DAVIS",
        "GEORGES CHARPACK",
    ]
    NOM_ECOLE_ELEMENTAIRE = [
        "BUFFLE /AUTRUCHE",
        "BELIER / RENNE (DEDALE)",
        "AIME CESAIRE",
        "DULCIE SEPTEMBER",
        "LUCIE AUBRAC",
        "P LANGEVIN",
        "JEAN MOULIN",
        "GABRIEL PERI",
    ]
    st.markdown(
    f'<h1 style="color: #0E2D23; font-size: 24px;">Formulaire de mise à jour de gaspillage</h1>', 
    unsafe_allow_html=True
    )
   
    with st.form("Gestion Affluence"):
        date_du_jour = st.date_input(label="Date du jour")
        ecole_type = st.selectbox("Type d'Ecole", options=ECOLE_TYPES, key="ecole_type_select")
        

        # Définition des options 
        if ecole_type == "Maternelles":
            options_choix = NOM_ECOLE_MATERNELLE  
        elif ecole_type == "Elementaires":
            options_choix = NOM_ECOLE_ELEMENTAIRE 
        else:
            options_choix = []

        # Création du deuxième selectbox avec les options dynamiques
        ecole_nom = st.selectbox(
            label="Choix de l'école",
            options=options_choix)

        nombre_eleve_cantine = st.text_input(label="Nombre d'élève à la cantine")

        # Mark mandatory fields
        ##st.markdown("**required*")
        

        submit_button = st.form_submit_button(label="Ajout des données")

        if submit_button :
            st.write(date_du_jour)
            st.write(ecole_nom)
            st.write(nombre_eleve_cantine)
            st.success("Vendor details successfully submitted!")
            pass