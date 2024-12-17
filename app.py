import streamlit as st
import pandas as pd
from streamlit_image_select import image_select

# Lire les CSV pour les DataFrames
df_search = pd.read_csv('reco.csv')
df_final = pd.read_csv('df_final.csv')
df_final['Titres_voisins'] = df_final['Titres_voisins'].apply(pd.eval)
df_final['directors'] = df_final['directors'].apply(pd.eval)
df_final['production_companies_name'] = df_final['production_companies_name'].apply(pd.eval)
df_final['genres_x'] = df_final['genres_x'].apply(pd.eval)
# Titre de l'application
st.title('Barre de Recherche sur Streamlit')

# Ajouter une option vide comme première option 

options = [''] + df_search['title_y'].tolist()

# Barre de recherche
search_query = st.selectbox('Que voulez-vous regarder ?', options=options)

def resultat_recherche(text):
    st.subheader('Résultats de la recherche :')
    film_details = df_final[df_search['title_y'] == text]
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




# Filtrer le DataFrame en fonction de la saisie utilisateur
if search_query:
    resultat_recherche(search_query)
    st.subheader('Nos recommandations :')
    film_recommandation = df_final[df_search['title_y'] == search_query]
    liste_reco =  film_recommandation['Titres_voisins'].iloc[0]
    liste_poster=[]
    for movie in range(10) :
        film_details = df_final[df_search['title_y'] == liste_reco[movie]]
        film_poster = film_details['url_poster_path'].iloc[0]
        liste_poster.append(film_poster)
    carroussel = image_select("Sélectionnez un film", liste_poster, use_container_width=True)
    # Récupérer les détails du film sélectionné 
    selected_film = df_final[df_final['url_poster_path'] == carroussel]['title_y'].values[0] 
    resultat_recherche(selected_film)
