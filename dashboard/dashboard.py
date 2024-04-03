import sys
print(sys.executable)
import re
import warnings
from datetime import date, datetime, timedelta


import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


warnings.filterwarnings("ignore", category=DeprecationWarning)

data_dashboard = pd.read_csv("data/data_dashboard.csv")
# Supprimer toutes les valeurs dde gaspillage négatives
data_dashboard = data_dashboard[data_dashboard["gaspillage_predit"] >= 0]


NUM_WEEKS = 16  # Sur combien de semaines on réalise les prédictions
delay_main_dish = 7  # Par défaut, un plat ne peut pas réapparaître en moins de 7 jours
delay_menu = 30  # Par défaut, un menu entier (entrée, plat, dessert) ne peut pas réapparaître en moins de 30 jours

WEEKDAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

def app():
   
    ####st.set_page_config(layout="wide", page_title="Predictive Cantine")
    
  st.write("# Predictive Cantine")
st.write("# Predictive Cantine")
if "Repas semaine" not in st.session_state:
    with st.spinner("Calcul en cours..."):
        st.session_state["Repas semaine"] = data_dashboard.copy()

# ######## Début du Dashboarding

current_week = (
    int(
        st.selectbox(
            "Choix de la semaine", [f"Semaine {i+1}" for i in range(NUM_WEEKS)], index=0
        ).split(" ")[-1]
    )
    - 1
)

# On a toutes les prédictions dans st.session_state["Repas semaine"], maintenant il faut construire les menus de chaque semaine
# en prenant en compte les règles métiers

sorted_results = st.session_state["Repas semaine"].sort_values(
    "gaspillage_predit_pourcentage", ascending=True
)

# Changer les dates de sorted_results pour qu'elles correspondent aux dates futures
length = sorted_results.shape[0]
# généerer une liste de date pour les jours de la semaine (lundi -> vendredi)
dates = pd.date_range(start=date(2024, 1, 1), periods=length, freq="B")
# ajuster la longueur de sorted_results à la longueur de dates
sorted_results = sorted_results.iloc[: dates.shape[0], :]
sorted_results["date"] = dates


def calcul_menus():
    # Cette fonction va calculer tous les menus des prochaines semaines en appliquant les règles métiers
    menus = {}
    for week in range(NUM_WEEKS):
        for i in range(5):
            delta_i = i + week * 5
            current_date = datetime(2024, 1, 1) + timedelta(
                days=delta_i + (2 * np.floor(delta_i / 5))
            )
            str_date = current_date.strftime("%Y-%m-%d")
            menus[str_date] = (
                sorted_results[sorted_results["date"] == current_date]
                .iloc[:50, :]
                .to_dict("records")
            )
    return menus


col1, col2, col3 = st.columns(3)

co2_couts = pd.read_csv("data/co2_couts.csv")
co2_couts["Nom"] = co2_couts["Nom"].str.lower()
co2_couts["Nom"] = co2_couts["Nom"].str.replace(
    r"(^\s+|\s+$)", ""
)  # On supprime les espaces au début et à la fin
co2_couts["Nom"] = co2_couts["Nom"].str.replace(r"s$", "")  # On supprime le pluriel
menus = calcul_menus()
if "skips" not in st.session_state:
    st.session_state["skips"] = {}


def get_current_menu(week_number):
    week_menus = []
    price = 0  # Coût total de la semaine pour un enfant
    co2 = 0  # Empreinte carbonne

    for i in range(5):
        i_week = i + week_number * 5
        current_date = datetime(2024, 1, 1) + timedelta(
            days=i_week + (2 * np.floor(i_week / 5))
        )
        str_date = current_date.strftime("%Y-%m-%d")

        row = menus[str_date][0]
        if str_date in st.session_state["skips"]:
            row = menus[str_date][st.session_state["skips"][str_date]]

        week_menus.append(row)

        # Maintenant, on calcule le coût du menu
        # On supposera un grammage de 100g pour chaque plat
        for dish in ["Entrée", "Plat", "Accompagnement", "Dessert", "Fromage"]:
            composants = [
                re.sub(r"(^\s+|\s+$)", "", re.sub("\s$", "", x))
                for x in str(row[dish]).lower().split()
            ]
            for comp in composants:
                match = co2_couts[co2_couts["Nom"] == comp]
                if match.shape[0] > 0:
                    price += 0.15 * float(
                        match.iloc[0]["Prix Unitaire Kg"].replace("€", "")
                    )
                    co2 += float(match.iloc[0]["Kg CO2 pour 1 kilo ou 1L"])

    return week_menus, price, co2


with col1:
    st.write("### Menu de la semaine")
    week_menus, prix_semaine, _ = get_current_menu(current_week)
    for i, row in enumerate(week_menus):
        btn = col1.button("Changer de menu", key="redo_{}".format(row["date"]))
        if btn:
            str_date = row["date"].strftime("%Y-%m-%d")
            st.session_state["skips"][str_date] = (
                st.session_state["skips"].get(str_date, 0) + 1
            )
            week_menus, prix_semaine, _ = get_current_menu(current_week)
            row = week_menus[i]

        col1.write(
            "#### {} ({})".format(
                WEEKDAYS[row["date"].weekday()], row["date"].strftime("%Y-%m-%d")
            )
        )
        day_cols = col1.columns(3)
        day_cols[0].write("##### Entrée")
        day_cols[0].write(row["Entrée"])
        if row["Entrée_Bio"]:
            day_cols[0].success("Bio")
        day_cols[1].write("##### Plat")
        day_cols[1].write(
            " + ".join(
                [x for x in [row["Plat"], row["Accompagnement"]] if str(x) != "nan"]
            )
        )
        if row["Plat_Bio"] or row["Accompagnement_Bio"]:
            day_cols[1].success("Bio")
        day_cols[2].write("##### Dessert")
        day_cols[2].write(
            " + ".join([x for x in [row["Dessert"], row["Fromage"]] if str(x) != "nan"])
        )
        if row["Dessert_Bio"] or row["Fromage_Bio"]:
            day_cols[2].success("Bio")
        col1.write("---")

with col2:
    participations = []
    week_menus, prix_semaine, _ = get_current_menu(current_week)
    for row in week_menus:
        participations.append(row["reel"])

    col2.write("### Budget")
    cols2_2 = col2.columns(2)
    num_students = cols2_2[0].number_input(
        "Nombre d'élèves inscrits à la cantine :",
        min_value=0,
        max_value=1500,
        value=150,
    )
    show_percent = cols2_2[1].checkbox("Afficher en pourcentages", value=False)

    cols2_1_metrics = col2.columns(3)
    cols2_1_metrics[0].metric(
        "Coût semaine par enfant", "{:2.1f}€".format(prix_semaine)
    )
    cols2_1_metrics[1].metric(
        "Coût total semaine", "{:2.1f}€".format(prix_semaine * num_students)
    )
    total_participation_rate = sum([x["reel"] for x in week_menus])
    cols2_1_metrics[2].metric(
        "Coût total semaine optimisé",
        "{:2.1f}€".format(prix_semaine * num_students * total_participation_rate / 5),
    )

    total_etudiants = sum([x["reel"] for x in week_menus])

    col2.write("### Affluence")
    col2.bar_chart(
        data=pd.DataFrame(
            np.array(
                [
                    [
                        round(x * 10) / 10
                        if show_percent
                        else round(x / 100 * num_students)
                    ]
                    for x in participations
                ]
            ),
            index=[f"{i+1} - {w}" for i, w in enumerate(WEEKDAYS)],
            columns=["reel" if show_percent else "Nombre de participants"],
        ),
        y="reel" if show_percent else "Nombre de participants",
    )
    week_menus, prix_semaine, co2 = get_current_menu(current_week)
    gaspillage_initial = []
    gaspillage_prevu = []
    for row in week_menus:
        gaspillage_initial.append(row["gaspillage_pourcentage"] * 100)
        gaspillage_prevu.append(row["gaspillage_predit_pourcentage"] * 100)

    col2.write("### Gaspillage")
    col2.bar_chart(
        data=pd.DataFrame(
            {
                "Gaspillage initial": gaspillage_initial,
                "Gaspillage prévu": gaspillage_prevu,
            },
            index=[f"{i+1} - {w}" for i, w in enumerate(WEEKDAYS)],
        )
    )

with col3:
    col3.write("### Gaspillage et CO2")
    cols3_1_metrics = col3.columns(3)
    cols3_1_metrics[0].metric(
        "Gaspillage initial", "{:.1f}%".format(sum(gaspillage_initial))
    )
    cols3_1_metrics[1].metric(
        "Gaspillage prévu", "{:.1f}%".format(sum(gaspillage_prevu))
    )
    cols3_1_metrics[2].metric(
        "Économies réalisées",
        "{:2.1f}%".format(
            (
                (
                    (prix_semaine * num_students * total_etudiants / 5)
                    - (prix_semaine * num_students)
                )
                / (prix_semaine * num_students)
            )
            * 100
        ),
    )
    col3.metric("Empreinte CO2 semaine", "{:2.1f} kg CO2".format(co2))

    col3.write("### Produits Bio de la semaine")
    have_bio = False
    for row in week_menus:
        cols_dish = ["Entrée", "Plat", "Accompagnement", "Fromage", "Dessert"]
        for dish in cols_dish:
            if row[dish + "_Bio"]:
                have_bio = True
                col3.write(
                    "{} ({})".format(
                        row[dish],
                        WEEKDAYS[row["date"].weekday()],
                    )
                )
    if not have_bio:
        col3.error("Pas de bio cette semaine !")

    col3.write("### Paramètres")
    delay_main_dish = col3.slider(
        "Délai d'apparition entre deux plats identiques (en jours)",
        min_value=1,
        max_value=30,
        value=7,
        step=1,
    )
    delay_menu = col3.slider(
        "Délai d'apparition entre deux menus identiques (en jours)",
        min_value=1,
        max_value=90,
        value=30,
        step=1,
    )


