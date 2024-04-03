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
import plotly.express as px

def app():
    #st.write('W. Acceuil')
    st.markdown(
    f'<div style="background-color:#0E2D23; padding: 2px; border-radius: 5px;">'
    '<h1 style="color: white;font-size: 18px;">W. Acceuil</h1>'
    '</div>',
    unsafe_allow_html=True)
    import folium 
    from streamlit_folium import folium_static
    from folium.plugins import MarkerCluster

    # Chargement des données
    data = pd.read_csv('data/StatsGrigny.csv', sep=';')
    """
    def create_map(data, pop):
        # Filtrer les données pour supprimer les lignes où la latitude ou la longitude est NaN
        data = data.dropna(subset=['latitude', 'longitude'])

        # Création de la carte
        m = folium.Map(location=[48.653396,2.384062], zoom_start=15)
        # Ajout des marqueurs
        for idx, row in data.iterrows():
            print(row.keys())  # Ajouter cette ligne pour le débogage
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=pop.format(row=row),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
        return m
    col1, col2, col3 = st.columns(3)
    with col1:
        optionAnnee = st.selectbox(
            label="Choix de l'année en cours",
            options=("2023", "2024", "2025")
        )
    with col2:
        optionMois = st.selectbox(
            label="Choix du mois en cours",
            options=("Janvier", "Fevrier")
        )
    with col3:
        boutonChoixCarte1 = st.button("Mise à jour de la carte")

    # Définition du popupInfo initial
    popupInfo = "{row['etablisement']}: {row['ElevePresentJanvierPourcentageMaxiJour']}"

    # Affichage de la carte initial
    carte = create_map(data, popupInfo)
    st.write(carte)

    # Mise à jour de la carte lorsqu'on clique sur le bouton
    if boutonChoixCarte1:
        # Mise à jour du popupInfo en fonction des options sélectionnées
        if optionAnnee == '2024' and optionMois == 'Janvier':
            popupInfo = "{row['etablisement']}: {row['ElevePresentJanvierPourcentageMaxiJour']}"
        elif optionAnnee == '2024' and optionMois == 'Fevrier':
           popupInfo = "{row['etablisement']}: {row['ElevePresentFevrierPourcentageMaxiJour']}"
        elif optionAnnee == '2023' and optionMois == 'Decembre':
            popupInfo = "{row['etablisement']}: {row['ElevePresentDecembrePourcentageMaxiJour']}"
        elif optionAnnee == '2023' and optionMois == 'Novembre':
            popupInfo = "{row['etablisement']}: {row['ElevePresentNovembrePourcentageMaxiJour']}"
        elif optionAnnee == '2023' and optionMois == 'Octobre':
            popupInfo = "{row['etablisement']}: {row['ElevePresentOctobrePourcentageMaxiJour']}"
        elif optionAnnee == '2023' and optionMois == 'Septembre':
            popupInfo = "{row['etablisement']}: {row['ElevePresentSeptembrePourcentageMaxiJour']}"

        # Mise à jour de la carte avec le nouveau popupInfo
        carte = create_map(data, popupInfo)
        st.write(carte)

    col11, col21 = st.columns([2, 1]) 
    with col11 :
        # Affichage de la carte dans Streamlit
        st.title('Carte des Établissements')
        st_map = create_map(data)
        folium_static(st_map, width=600)
    with col21:
        # Conteneur pour les informations sur les écoles maternelles
        with st.container() :
            st.title("Nombre d'école maternelle")
            st.write('Nombre école MATERNELLE')

        # Conteneur pour les informations sur les écoles élémentaires
        with st.container() :
            st.title("Nombre d'école élémentaire")
            st.write('Nombre école ELEMENTAIRE')

        # Conteneur pour les informations sur les écoles élémentaires
        with st.container() :
           # st.markdown("<style>div[data-testid='stContainer'] div { background-color: #FFC300; padding: 10px; border-radius: 30px; }</style>", unsafe_allow_html=True)
            st.markdown("<h2 style='font-size: 20px; background-color: #69C649; border-radius: 30px ; '>Pourcentage de presence sur le mois au niveau de la ville</h2>", unsafe_allow_html=True)
            st.write('POURCENTAGE VILLE')
    """
    dataO = data.dropna(subset=['ElevePresentJanvierSommeTotal'])
    data = pd.read_csv('data/StatsGrigny.csv', sep=';')
    # Filtrer les données pour la ville
    data_ville = data[data['etablisement'] == "Total Villes"]
    data_elementaire = data[data['etablisement'] == "Total Elementaires"]
    data_maternelle = data[data['etablisement'] == "Total Maternelles"]

    
    st.title('Dashboard interactif général')
    col1, col2, col3 = st.columns(3)
    with col1:
        optionAnnee = st.selectbox(
            label="Choix de l'année en cours",
            options=("2023", "2024")
        )
    with col2:
        optionMois = st.selectbox(
            label="Choix du mois en cours",
            options=("Janvier", "Fevrier","Mars","Avril","Mai","Juin","Juillet","Septembre","Octobre","Novembre","Decembre")
        )
    with col3:
        boutonChoixCarte1 = st.button("Mise à jour des données")
    
    # Initialisation des conteneurs vides
    #conteneur1 = st.metric(label="Pourcentage d'élève à la cantine dans la ville",value=data_ville['ElevePresentFevrierPourcentageMaxiJour'].iloc[0])
    #conteneur2 = st.metric(label="Pourcentage d'élève à la cantine en élémentaire",value=data_elementaire['ElevePresentFevrierPourcentageMaxiJour'].iloc[0])
    #conteneur3 = st.metric(label="Pourcentage d'élève à la cantine en maternellr",value=data_maternelle['ElevePresentFevrierPourcentageMaxiJour'].iloc[0])
    
    
    def valeur_par_annee_et_mois(dataframe, annee, mois):
        # Cette fonction doit être implémentée pour retourner la valeur correspondante
        # en fonction de l'année et du mois. Par exemple:
        colonne = f"ElevePresent{mois}PourcentageMaxiJour"
        if annee == "2023" and optionMois == "Septembre" :
            return dataframe[colonne].iloc[0]
        elif annee == "2023" and optionMois == "Octobre" :
            # Modifier selon la logique souhaitée pour 2024
            return dataframe[colonne].iloc[0]
        elif annee == "2023" and optionMois == "Novembre" :
            # Modifier selon la logique souhaitée pour 2024
            return dataframe[colonne].iloc[0]
        elif annee == "2023" and optionMois == "Decembre" :
            # Modifier selon la logique souhaitée pour 2024
            return dataframe[colonne].iloc[0]
        elif annee == "2024" and optionMois == "Janvier" :
            # Modifier selon la logique souhaitée pour 2024
            return dataframe[colonne].iloc[0]
        elif annee == "2024" and optionMois == "Fevrier" :
            # Modifier selon la logique souhaitée pour 2024
            return dataframe[colonne].iloc[0]
        else:
            return "Données indisponible"

    # Initialisation de la variable valeur
    #valeur = None
    #valeur1 = None
    #valeur2 = None
    
        
    def graphique_par_annee_et_mois_elementaire(dataframe, annee, mois):
        # Définition de la fonction pour créer le graphique
        # Filtrer pour les établissements de type "élémentaire"
        dataframe_filtre = dataframe[dataframe['type'] == "Elementaires"]
        # Sélectionner la colonne appropriée
        colonne = f"ElevePresent{mois}PourcentageMaxiJour"
        
        # Filtrer pour l'année sélectionnée
        # dataframe_filtre = dataframe_filtre[dataframe_filtre['annee'] == annee]
    
        if annee == "2023" and mois in ["Septembre", "Octobre", "Novembre", "Decembre"]:
            # Trier les données par pourcentage de présence des élèves
            dataframe_filtre = dataframe_filtre.sort_values(by=colonne)
            dataframe_filtre[colonne] = dataframe_filtre[colonne].str.replace(',', '.').astype(float)
            # Création du graphique en barres
           # plt.figure(figsize=(10, 6))
            f=px.bar(dataframe_filtre, x="etablisement", y=colonne, color="etablisement")
            f.update_layout(yaxis=dict(
        tickformat=',2%',  # Format avec deux décimales
        title="Pourcentage d'éleves à la cantine d'urant la période selectionné"  # Titre de l'axe y
    ),xaxis=dict(
        title="Ecole élémentaire de Grigny"  # Titre de l'axe x
    ))
            f.update_layout(
    width=500,  # Largeur en pixels
    height=350,  # Hauteur en pixels
    xaxis_title_font_size=9,  # Taille de la police pour le titre de l'axe X
    yaxis_title_font_size=9   # Taille de la police pour le titre de l'axe Y
)
            f.update_layout(
    xaxis_tickfont_size=6  # Ajuster la taille de la police ici
)
            return f
    
        elif annee == "2024" and mois in ["Janvier", "Fevrier"]:
            # Trier les données par pourcentage de présence des élèves
            dataframe_filtre = dataframe_filtre.sort_values(by=colonne)
            dataframe_filtre[colonne] = dataframe_filtre[colonne].str.replace(',', '.').astype(float)
        
            # Création du graphique en barres
            
            f=px.bar(dataframe_filtre, x="etablisement", y=colonne, color="etablisement")
            f.update_layout(yaxis=dict(
        tickformat=',2%', # Format avec deux décimales
        title="Pourcentage d'éleves à la cantine d'urant la période selectionné"  # Titre de l'axe y
    ),xaxis=dict(
        title="Ecole élémentaire de Grigny"  # Titre de l'axe x
    ))
            f.update_layout(
    width=500,  # Largeur en pixels
    height=350,  # Hauteur en pixels
    xaxis_title_font_size=9,  # Taille de la police pour le titre de l'axe X
    yaxis_title_font_size=9   # Taille de la police pour le titre de l'axe Y
)
            f.update_layout(
    xaxis_tickfont_size=6  # Ajuster la taille de la police ici
)
            return f
        else:
            # Retourner un message d'erreur
            return "Données indisponible ou mois non reconnu"
            
        

    col111, col222, col333 = st.columns(3)
    with col111:
        # Initialisation des métriques avec des valeurs par défaut
        conteneur1 = st.metric(label="Pourcentage d'élève à la cantine dans la ville", value=f"{data_ville['ElevePresentFevrierPourcentageMaxiJour'].iloc[0]}%")
        conteneur2 = st.metric(label="Pourcentage d'élève à la cantine en élémentaire", value=f"{data_elementaire['ElevePresentFevrierPourcentageMaxiJour'].iloc[0]}%")
        conteneur3 = st.metric(label="Pourcentage d'élève à la cantine en maternelle", value=f"{data_maternelle['ElevePresentFevrierPourcentageMaxiJour'].iloc[0]}%")

        # Mise à jour des métriques en fonction des sélections
        if boutonChoixCarte1:
            try:
                # Récupération des nouvelles valeurs en fonction des sélections
                nouvelle_valeur = valeur_par_annee_et_mois(data_ville, optionAnnee, optionMois)
                nouvelle_valeur1 = valeur_par_annee_et_mois(data_elementaire, optionAnnee, optionMois)
                nouvelle_valeur2 = valeur_par_annee_et_mois(data_maternelle, optionAnnee, optionMois)

                # Mise à jour des métriques
                conteneur1.metric(label="Pourcentage d'élève à la cantine dans la ville", value=f"{nouvelle_valeur}%")
                conteneur2.metric(label="Pourcentage d'élève à la cantine en élémentaire", value=f"{nouvelle_valeur1}%")
                conteneur3.metric(label="Pourcentage d'élève à la cantine en maternelle", value=f"{nouvelle_valeur2}%")

            except IndexError:
                # Affichage d'un message d'erreur en cas de problème
                conteneur1.metric(label="Pourcentage d'élève à la cantine dans la ville", value="Données indisponible")
                conteneur2.metric(label="Pourcentage d'élève à la cantine en élémentaire", value="Données indisponible")
                conteneur3.metric(label="Pourcentage d'élève à la cantine en maternelle", value="Données indisponible")
        
        with col222:
            #plt_initial = graphique_par_annee_et_mois_elementaire(data, "2024", "Fevrier")
            #st.pyplot(plt_initial)
            if boutonChoixCarte1:
                #graph = graphique_par_annee_et_mois_elementaire(data, optionAnnee, optionMois)
                #st.pyplot(graph)
                
                graph = graphique_par_annee_et_mois_elementaire(data, optionAnnee, optionMois)
                if isinstance(graph, str):
                    # Si le graphique est un message d'erreur, afficher le message
                    st.write(graph)
                else:
                    # Si le graphique est un objet Plotly, l'afficher avec st.plotly_chart()
                    st.plotly_chart(graph)
        

    # Application Streamlit
    st.title('Graphique dynamique des repas consommés sur le mois dans les établissements')

    # Widget Multiselect pour sélectionner les établissements
    selected_etablissements = st.multiselect('Choisissez les établissements', data['etablisement'].unique().tolist())

    # Filtrer les données en fonction des établissements sélectionnés
    filtered_data = dataO[dataO['etablisement'].isin(selected_etablissements)]
    # S'assurer que les établissements sont sélectionnés avant de créer le graphique
    col12, col22 = st.columns([2, 1])
    if selected_etablissements:
        with col12 :
            figure = px.bar(filtered_data, x="etablisement", y="ElevePresentJanvierSommeTotal", color="etablisement")
            figure.update_layout(width=800)
            st.plotly_chart(figure)

    optionSemaine = st.selectbox(
            label = "Choix de semaine par rapport à l'année selectioné plus haut." ,
            options = ("Semaine 1","Semaine 2","Semaine 3","Semaine 4","Semaine 5","Semaine 6",
                       "Semaine 7","Semaine 8","Semaine 9","Semaine 10","Semaine 11","Semaine 12",
                       "Semaine 13","Semaine 14","Semaine 15","Semaine 16","Semaine 17","Semaine 18",
                       "Semaine 19","Semaine 20","Semaine 21","Semaine 22","Semaine 23","Semaine 24",
                       "Semaine 25","Semaine 26","Semaine 27","Semaine 28","Semaine 29","Semaine 30",
                       "Semaine 31","Semaine 32","Semaine 33","Semaine 34","Semaine 35","Semaine 36",
                       "Semaine 37","Semaine 38","Semaine 39","Semaine 40","Semaine 41","Semaine 42",
                       "Semaine 43","Semaine 44","Semaine 45","Semaine 46","Semaine 47","Semaine 48",
                       "Semaine 49","Semaine 50","Semaine 51","Semaine 52"
                        )
        )
    def create_map2(data):
        # Filtrer les données pour supprimer les lignes où la latitude ou la longitude est NaN
        data = data.dropna(subset=['latitude', 'longitude'])
        # Création de la carte
        m = folium.Map(location=[48.653396,2.384062], zoom_start=15)
        # Ajout des marqueurs
        for idx, row in data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['etablisement']}: {row['ElevePresentJanvierPourcentageMaxiJour']}%"
            ).add_to(m)
        return m
    
    col13, col23 = st.columns([2, 1]) 
    with col13 :
        # Affichage de la carte dans Streamlit
        st.title('Localisation des écoles et taux de présence sur le dernier mois')
        st_map2 = create_map2(data)
        folium_static(st_map2, width=600)
    
    
    col14, col24, col34 = st.columns(3)
    with col14:
        optionAnnee = st.selectbox(
            label = "Choix du type d'école" ,
            options = ("Elementaires","Maternelles")
        )
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
    with col24:
        # Définition des options pour le deuxième selectbox en fonction du premier choix
        if optionAnnee == "Elementaires":
            options_choix2 = NOM_ECOLE_MATERNELLE  
        elif optionAnnee == "Maternelles":
            options_choix2 = NOM_ECOLE_ELEMENTAIRE

        # Création du deuxième selectbox avec les options dynamiques
        optionEcole = st.selectbox(
            label="Choix de l'école",
            options=options_choix2
        )
        
    with col34:
        boutonChoixInfoEcole = st.button("Mise à jour des infos")
    
    col15, col25, col35, col45 = st.columns(4)
   # with col15:
        #boutonChoixInfoEcole = st.button("Mise à jour des infos")
    #with col25:
        #boutonChoixInfoEcole = st.button("Mise à jour des infos")
    #with col35:
        #boutonChoixInfoEcole = st.button("Mise à jour des infos")
    #with col45:
        #boutonChoixInfoEcole = st.button("Mise à jour des infos")

           