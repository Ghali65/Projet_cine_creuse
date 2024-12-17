import streamlit as st
import pandas as pd

# Lire les CSV pour les DataFrames
df_search = pd.read_csv('reco.csv')
df_final = pd.read_csv('df_final.csv')
# Titre de l'application
st.title('Barre de Recherche sur Streamlit')

# Barre de recherche
search_query = st.selectbox('Que voulez-vous regarder ?', options=df_search['title_y'])

# Filtrer le DataFrame en fonction de la saisie utilisateur
if search_query:
    st.write('Résultats de la recherche :')
    film_details = df_final[df_search['title_y'] == search_query]
    film_title = film_details['title_y'].iloc[0] 
    film_overview = film_details['résumé'].iloc[0]
    film_poster = film_details['url_poster_path'].iloc[0]
     # Afficher les résultats 
    col1, col2 = st.columns([2, 1]) 
    # Ajouter du contenu dans la première colonne 
    with col1: 
        st.write(f"**Titre du film :** {film_title}") 
        st.write(f"**Résumé :** {film_overview}")
    # Ajouter du contenu dans la deuxième colonne 
    with col2: 
        st.image(film_poster)
# Afficher le DataFrame filtré

