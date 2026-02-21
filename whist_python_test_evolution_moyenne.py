# import pandas as pd
# import streamlit as st

# EXCEL_FILE = "classement_whist_2023_2025.xlsx"
# SHEET_NAME = "Classement"

# # -----------------------------
# # ÉVOLUTION DE LA MOYENNE : ACHILLE
# # -----------------------------
# st.write("---")
# st.subheader("📈 Évolution de la moyenne : Achille")

# # 1. Charger la feuille contenant l'historique des parties
# # Remplacez "All_stat" par le nom exact de l'onglet concerné
# df_historique = pd.read_excel(EXCEL_FILE, sheet_name="All stat")


# # 2. Isoler les colonnes pour Achille :
# # Index 1 (Col B) = Numéro de soirée
# # Index 2 (Col C) = Points obtenus par Achille lors de la soirée
# # Index 3 (Col D) = Nombre de parties jouées par Achille lors de la soirée
# df_achille = df_historique.iloc[:, [1, 2, 3]].copy()
# df_achille.columns = ["Num_Soiree", "Score_Soiree", "Parties_Soiree"]

# # 3. Forcer la conversion en nombres (les textes et en-têtes deviendront "NaN")
# df_achille["Num_Soiree"] = pd.to_numeric(df_achille["Num_Soiree"], errors='coerce')
# df_achille["Score_Soiree"] = pd.to_numeric(df_achille["Score_Soiree"], errors='coerce')
# df_achille["Parties_Soiree"] = pd.to_numeric(df_achille["Parties_Soiree"], errors='coerce')

# # 4. Supprimer les lignes vides ou non valides (ex: soirées où Achille n'a pas joué)
# df_achille = df_achille.dropna(subset=["Num_Soiree", "Score_Soiree", "Parties_Soiree"]).copy()

# # 5. Trier chronologiquement (Soirée 1 en haut)
# df_achille = df_achille.sort_values(by="Num_Soiree", ascending=True)

# # 6. Calculer les totaux cumulés au fil des soirées
# df_achille["Score_Cumule"] = df_achille["Score_Soiree"].cumsum()
# df_achille["Parties_Cumulees"] = df_achille["Parties_Soiree"].cumsum()

# # 7. Calculer la moyenne évolutive (Score total / Parties totales)
# df_achille["Moyenne_Evolutive"] = df_achille["Score_Cumule"] / df_achille["Parties_Cumulees"]

# # 8. Préparer et afficher le graphique
# df_graphique = df_achille.set_index("Num_Soiree")[["Moyenne_Evolutive"]]
# df_graphique.rename(columns={"Moyenne_Evolutive": "Moyenne Achille"}, inplace=True)

# st.line_chart(df_graphique)






import pandas as pd
import streamlit as st

# ... (le reste de votre code en haut) ...
EXCEL_FILE = "classement_whist_2023_2025.xlsx"
SHEET_NAME = "Classement"
# -----------------------------
# ÉVOLUTION DE LA MOYENNE : TOUS LES JOUEURS
# -----------------------------
st.write("---")
st.subheader("📈 Évolution des moyennes")

# 1. Charger la feuille d'historique (sans en-tête pour cibler par index)
df_historique = pd.read_excel(EXCEL_FILE, sheet_name="All stat", header=None)

# 2. Initialiser un DataFrame vide qui va rassembler toutes les moyennes
combined_data = pd.DataFrame()

# La ligne contenant les prénoms est la 9ème ligne (index 8)
# Le premier joueur (Achille) est à la colonne C (index 2)
# Les données avancent par blocs de 2 colonnes (Score puis Parties)
col_idx = 2

while col_idx < len(df_historique.columns):
    # Récupérer le nom du joueur
    player_name = str(df_historique.iloc[8, col_idx]).strip()
    
    # Si la cellule est vide ou "nan", on a atteint la fin des joueurs
    if pd.isna(df_historique.iloc[8, col_idx]) or player_name.lower() == "nan" or player_name == "":
        break

    # Isoler les colonnes : Soirée (1), Score du joueur (col_idx), Parties du joueur (col_idx + 1)
    df_player = df_historique.iloc[:, [1, col_idx, col_idx + 1]].copy()
    df_player.columns = ["Num_Soiree", "Score_Soiree", "Parties_Soiree"]

    # Convertir en valeurs numériques
    df_player["Num_Soiree"] = pd.to_numeric(df_player["Num_Soiree"], errors='coerce')
    df_player["Score_Soiree"] = pd.to_numeric(df_player["Score_Soiree"], errors='coerce')
    df_player["Parties_Soiree"] = pd.to_numeric(df_player["Parties_Soiree"], errors='coerce')

    # Ne garder que les soirées où le joueur a effectivement joué
    df_player = df_player.dropna(subset=["Num_Soiree", "Score_Soiree", "Parties_Soiree"]).copy()

    if not df_player.empty:
        # Trier chronologiquement (Soirée 1 en haut)
        df_player = df_player.sort_values(by="Num_Soiree", ascending=True)

        # Calculer les totaux cumulés
        df_player["Score_Cumule"] = df_player["Score_Soiree"].cumsum()
        df_player["Parties_Cumulees"] = df_player["Parties_Soiree"].cumsum()

        # Calculer la moyenne évolutive
        df_player["Moyenne_Evolutive"] = df_player["Score_Cumule"] / df_player["Parties_Cumulees"]

        # Préparer le tableau avec le numéro de soirée en index et le nom du joueur en colonne
        df_player = df_player.set_index("Num_Soiree")[["Moyenne_Evolutive"]]
        df_player.rename(columns={"Moyenne_Evolutive": player_name}, inplace=True)

        # Ajouter au DataFrame global
        if combined_data.empty:
            combined_data = df_player
        else:
            combined_data = combined_data.merge(df_player, left_index=True, right_index=True, how='outer')

    # Passer au joueur suivant (+2 colonnes)
    col_idx += 2

# 3. Trier l'axe des soirées de la première à la dernière
combined_data = combined_data.sort_index()

# 4. Remplir les valeurs manquantes (forward fill)
# Si un joueur ne joue pas la soirée 10, sa moyenne à la soirée 10 reste celle de la soirée 9
combined_data = combined_data.ffill()

# 5. Interface Streamlit : Sélecteur de joueurs
st.write("Sélectionnez les joueurs pour comparer leur évolution :")

# On affiche par défaut le top 3 (ou tous les joueurs si moins de 3)
default_players = combined_data.columns[:3].tolist() 

joueurs_selectionnes = st.multiselect(
    "Joueurs",
    options=combined_data.columns,
    default=default_players
)

# 6. Afficher le graphique avec les joueurs sélectionnés
if joueurs_selectionnes:
    st.line_chart(combined_data[joueurs_selectionnes])
else:
    st.warning("Veuillez sélectionner au moins un joueur.")