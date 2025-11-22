


import streamlit as st
import pandas as pd

# -----------------------------
# PARAMÈTRES
# -----------------------------
EXCEL_FILE = "classement_whist_2023_2025.xlsx"
SHEET_NAME = "Classement"

df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

# Nettoyer les noms de colonnes
df.columns = df.columns.str.strip().str.lower()

# Garder uniquement les 4 premières colonnes
df = df.iloc[:, :4]

# Retirer l’index
df = df.reset_index(drop=True)

# -----------------------------
# CSS POUR CENTRER TOUTES LES CELLULES DU TABLEAU STREAMLIT
# -----------------------------
st.markdown("""
<style>
/* Centrer tout le texte du tableau */
[data-testid="stDataFrame"] td {
    text-align: center !important;
}
[data-testid="stDataFrame"] th {
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# FONCTION COULEURS
# -----------------------------
def color_party_count(val):
    if val < 10:
        return "background-color: #A0A0A0"
    elif val < 20:
        return "background-color: #C0C0C0"
    elif val < 50:
        return "background-color: #FF4C4C"
    elif val < 100:
        return "background-color: #FFD44C"
    elif val < 250:
        return "background-color: #C6FF4C"
    elif val < 500:
        return "background-color: #80FF4C"
    elif val < 1000:
        return "background-color: #00CC00"
    else:
        return "background-color: #009900"

# -----------------------------
# TITRE + PODIUM
# -----------------------------
st.title("🏆 Classement Whist")

top3 = df.head(3)

st.markdown(
    f"""
    <div style="display:flex; justify-content:center; gap:25px; margin-bottom:25px;">
        <div style="text-align:center;">
            <h2>🥈 {top3.iloc[1]['noms']}</h2>
            <p style="font-size:20px;">{top3.iloc[1]['moyennes']:.3f}</p>
        </div>
        <div style="text-align:center;">
            <h1>🥇 {top3.iloc[0]['noms']}</h1>
            <p style="font-size:24px; font-weight:bold;">{top3.iloc[0]['moyennes']:.3f}</p>
        </div>
        <div style="text-align:center;">
            <h2>🥉 {top3.iloc[2]['noms']}</h2>
            <p style="font-size:20px;">{top3.iloc[2]['moyennes']:.3f}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)




# ----------# -----------------------------
# PODIUM DES DERNIERS (LOOSERS)
# -----------------------------
st.write("---")
st.subheader("🐐 Podium du bas (Looser)")

bottom3 = df.tail(3)  # les 3 derniers joueurs

st.markdown(
    f"""
    <div style="display:flex; justify-content:center; gap:25px; margin-bottom:25px;">
        <div style="text-align:center;">
            <h2>💀 {bottom3.iloc[1]['noms']}</h2>
            <p style="font-size:20px;">{bottom3.iloc[1]['moyennes']:.3f}</p>
        </div>
        <div style="text-align:center;">
            <h1>🪦 {bottom3.iloc[2]['noms']}</h1>
            <p style="font-size:24px; font-weight:bold;">{bottom3.iloc[2]['moyennes']:.3f}</p>
        </div>
        <div style="text-align:center;">
            <h2>⬇️ {bottom3.iloc[0]['noms']}</h2>
            <p style="font-size:20px;">{bottom3.iloc[0]['moyennes']:.3f}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.write("---")




# -----------------------------
# TABLEAU COULEUR DYNAMIQUE
# -----------------------------
styled_df = (
    df.style
      .apply(lambda row: [color_party_count(row["nombre de parties"])] * len(row), axis=1)
      .format({"moyennes": "{:.3f}"})
)

# -----------------------------
# TABLEAU + LÉGENDE CÔTE À CÔTÉ
# -----------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📊 Tableau complet du classement")
    # st.dataframe(styled_df, hide_index=True, use_container_width=True, height=700)

    # -----------------------------
    # TABLEAU COULEUR + CENTRAGE TOTAL (HTML)
    # -----------------------------
    styled_df = (
        df.style
        .apply(lambda row: [color_party_count(row["nombre de parties"])] * len(row), axis=1)
        .format({"moyennes": "{:.3f}"})
        .set_properties(**{'text-align': 'center'})
    )

    # Conversion HTML (sans index)
    html_table = styled_df.hide(axis="index").to_html()

    # # Centrer aussi la table elle-même
    # html_table = f"""
    # <div style="display:flex; justify-content:center;">
    #     {html_table}
    # """

    # Affichage dans Streamlit
    st.markdown(html_table, unsafe_allow_html=True)


with col2:
    st.subheader("🟩 Légende fiabilité")

    legend_data = {
        "Nbr parties": [
            "1 à 10", "10 à 20", "20 à 50", "50 à 100",
            "100 à 250", "250 à 500", "500 à 1000", "1000+"
        ],
        "Interprétation": [
            "anecdotique", "inexploitable", "pas fiable", "exploratoire",
            "solide", "fiable", "très fiable", "indiscutable"
        ],
        "Crédibilité": [
            "négligeable", "inutile", "fragile", "à confirmer",
            "fondé", "crédible", "très robuste", "irréfutable"
        ],
        "Couleur": [
            "#A0A0A0", "#C0C0C0", "#FF4C4C", "#FFD44C",
            "#C6FF4C", "#80FF4C", "#00CC00", "#009900"
        ]
    }

    legend_df = pd.DataFrame(legend_data)

    def color_square_hex(hex_color):
        return f'<div style="width:25px;height:25px;background:{hex_color};border-radius:4px;"></div>'

    legend_df[""] = legend_df["Couleur"].apply(color_square_hex)

    st.markdown(
        legend_df[["", "Nbr parties", "Interprétation", "Crédibilité"]]
        .to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
    #éviter le passage ) la ligne dans la légende
    # st.markdown("""
    # <style>
    # .dataframe td, .dataframe th {
    #     white-space: nowrap;
    #     min-width: 100px;
    # }
    # </style>
    # """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Empêcher le texte de passer à la ligne */
    .dataframe td, .dataframe th {
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

