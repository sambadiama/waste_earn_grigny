import sys
print(sys.executable)
import re
import warnings
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

def app():
    #st.write('W. Affluence')
    st.markdown(
    f'<div style="background-color:#0E2D23; padding: 2px; border-radius: 5px;">'
    '<h1 style="color: white;font-size: 18px;">W. Affluence</h1>'
    '</div>',
    unsafe_allow_html=True)
    # List écoles et type
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
    f'<h1 style="color: #0E2D23; font-size: 24px;">Formulaire de mise à jour de l\'affluence réel</h1>', 
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

        # If the submit button is pressed
        ##if submit_button:
            # Check if all mandatory fields are filled
            ##if not company_name or not business_type:
                ##st.warning("Ensure all mandatory fields are filled.")
                ##st.stop()
            ##elif existing_data["CompanyName"].str.contains(company_name).any():
                ##st.warning("A vendor with this company name already exists.")
                ##st.stop()
            ##else:
                # Create a new row of vendor data
                ##vendor_data = pd.DataFrame(
                    ##[
                        ##{
                            ##"CompanyName": company_name,
                            ##"BusinessType": business_type,
                            ##"Products": ", ".join(products),
                            ##"YearsInBusiness": years_in_business,
                            ##"OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                            ##"AdditionalInfo": additional_info,
                        ##}
                    ##]
                ##)

                # Add the new vendor data to the existing data
                ##updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

                # Update Google Sheets with the new vendor data
                ##conn.update(worksheet="Vendors", data=updated_df)

                ##st.success("Vendor details successfully submitted!")
    st.markdown(
    f'<h1 style="color: #0E2D23; font-size: 24px;">Dashbord de visualisation</h1>', 
    unsafe_allow_html=True
    )
    # Chargement des données
    df = pd.read_csv('data/data_dashboard_grigny2.csv')
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')  # Assurez-vous que le format de date correspond

    st.markdown(
    f'<h1 style="color: #F8AB29; font-size: 24px;">Comparaison de performance</h1>', 
    unsafe_allow_html=True
    )

    # Sélection de la date
    selected_date = st.date_input('Choisissez une date', datetime.today())

    # Filtrage des données en fonction de la date sélectionnée
    filtered_data = df[df['date'] == pd.Timestamp(selected_date)]

    if not filtered_data.empty:
        # Création de trois colonnes
        col1, col2, col3 = st.columns(3)

         # Utilisation de HTML pour ajouter des styles avec fond de couleur
        def display_with_border_and_color(text, color):
            return f"<div style='border:2px solid black; padding:10px; margin: 5px; background-color:{color};'>{text}</div>"

        with col1:
            st.markdown(display_with_border_and_color(f"Commande prévu : {filtered_data['prevision'].iloc[0]}", "#69C649"), unsafe_allow_html=True)
    
        with col2:
             st.markdown(display_with_border_and_color(f"Affluence Réel pour : {filtered_data['reel'].iloc[0]}", "#69C649"), unsafe_allow_html=True)
    
        with col3:
            st.markdown(display_with_border_and_color(f"Affluence prédite par l'IA : {filtered_data['affluence_reelle_predite'].iloc[0]}", "#69C649"), unsafe_allow_html=True)
        # Calcul et affichage des écarts
        ecart_prevision = filtered_data['reel'].iloc[0] - filtered_data['prevision'].iloc[0]
        ecart_affluence_predite = filtered_data['reel'].iloc[0] - filtered_data['affluence_reelle_predite'].iloc[0]

        col4, col5 = st.columns(2)
        with col4:
            st.markdown(display_with_border_and_color(f"Écart entre les commandes réalisé et le nombre d'éleves à la cantine: {ecart_prevision}", "#FFC300"), unsafe_allow_html=True)
        with col5:
            st.markdown(display_with_border_and_color(f"Écart entre les prediction de l'IA et le nombre d'éleves à la cantine: {ecart_affluence_predite}", "#FFC300"), unsafe_allow_html=True)
        # Préparation des données pour Seaborn
        data_to_plot = {
        "Types d'écarts": ["Écart Réel - Prévision", "Écart Réel - Affluence Prédite"],
        "Valeurs": [ecart_prevision, ecart_affluence_predite]
        }
      
        # Création du graphique avec Seaborn
        plt.figure(figsize=(4, 2))
        sns.barplot(x="Types d'écarts", y="Valeurs", data=data_to_plot)
        plt.title('Comparaison des écarts')

        # Affichage du graphique dans Streamlit
        st.pyplot(plt)
    else:
        st.write("Aucune donnée disponible pour cette date.")

    st.title("Dashboard des données d'affluence")
    data = pd.read_csv('data/data_dashboard_grigny.csv')

    # Conversion de la colonne 'date' en type datetime
    data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')

    # Sélection des données à visualiser
    plot_data = data[['date', 'affluence_reelle_predite', 'reel', 'prevision']]

    # Création du graphique
    plt.figure(figsize=(15, 8))
    sns.lineplot(x='date', y='affluence_reelle_predite', data=plot_data, label='Affluence Réelle Prédite')
    sns.lineplot(x='date', y='reel', data=plot_data, label='Réel')
    sns.lineplot(x='date', y='prevision', data=plot_data, label='Prévision')
    plt.title('Évolution des catégories Affluence Réelle Prédite, Réel et Prévision')
    plt.xlabel('Date')
    plt.ylabel('Valeurs')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Affichage du graphique dans Streamlit
    st.pyplot(plt)