import streamlit as st
import pandas as pd
from streamlit_image_select import image_select
from streamlit_carousel import carousel



# Lire les CSV pour les DataFrames
df_search = pd.read_csv('reco.csv')
df_final = pd.read_csv('df_final.csv')
df_final['Titres_voisins'] = df_final['Titres_voisins'].apply(pd.eval)
df_final['directors'] = df_final['directors'].apply(pd.eval)
df_final['production_companies_name'] = df_final['production_companies_name'].apply(pd.eval)
df_final['genres_x'] = df_final['genres_x'].apply(pd.eval)

# Titre de l'application
st.title('Bienvenue sur Cinécreusix')

# Ajouter une option vide comme première option 
options = [''] + df_search['title_y'].tolist()

# Barre de recherche
search_query = st.selectbox('Que voulez-vous regarder ?', options=options)

def resultat_recherche(text):
    print("SALUT "+text)
    st.subheader('Résultats de la recherche :')
    film_details = df_final[df_search['title_y'] == text]
    if film_details.empty:
        st.write(f"Aucun résultat trouvé pour : {text}")
    else:
        film_title = film_details['title_y'].iloc[0] 
        film_overview = film_details['résumé'].iloc[0]
        film_poster = film_details['url_poster_path'].iloc[0]
        film_gender = film_details['genres_x'].iloc[0]
        film_gender_str = ', '.join(film_gender)
        film_directors = film_details['directors'].iloc[0]
        film_directors_str = ', '.join(film_directors)
        #print(len_max)
        print(film_gender)
        # Afficher les résultats 
        col1, col2 = st.columns([2, 1]) 
        # Ajouter du contenu dans la première colonne 
        with col1: 
            st.write(f"**Titre du film :** {film_title}") 
            st.write(f"**Résumé :** {film_overview}")
            st.write(f"**Genre :** {film_gender_str}")
            st.write(f"**Réalisateur :** {film_directors_str}")
        # Ajouter du contenu dans la deuxième colonne 
        with col2: 
            st.image(film_poster)

def click_button(title):
    print(title)
    print('TU ES RENTRE')
    st.session_state["film_actuel"] = title
    st.session_state["lookreco"] = True

if "film_actuel" not in st.session_state:
    st.session_state["film_actuel"] = None
    st.session_state["lookreco"] = False

if search_query and st.session_state["lookreco"] is False: # reco par recherche, ca rentre si look reco false
    print("oOKOKOKOKOKOKO")
    st.session_state["film_actuel"] = search_query

if st.session_state["film_actuel"] is not None:
    st.session_state["lookreco"] = False
    print("bbbb"+st.session_state["film_actuel"])
    # Mettre à jour les paramètres de requête avec st.experimental_set_query_params
    #st.experimental_set_query_params(search_query=search_query)
    resultat_recherche(st.session_state["film_actuel"])
    st.subheader('Nos recommandations :')
    film_recommandation = df_final[df_search['title_y'] == st.session_state["film_actuel"]]
    liste_reco = film_recommandation['Titres_voisins'].iloc[0]
    print(liste_reco)
    liste_poster = []

    for movie in range(10):
        film_details = df_final[df_search['title_y'] == liste_reco[movie]]
        if not film_details.empty:
            film_poster = film_details['url_poster_path'].iloc[0]
            liste_poster.append(film_poster)
        else:
            liste_poster.append("")

    # Afficher les résultats dans deux rangées de cinq colonnes 
    cols_top = st.columns(5) 
    cols_bottom = st.columns(5) 
    for i, (poster, title) in enumerate(zip(liste_poster, liste_reco)): 
        if poster:  # Vérifie si l'URL du poster n'est pas vide
            if i < 5:
                with cols_top[i % 5]:
                    st.image(poster)
                    st.button(title, on_click=click_button, args=[title])

            else:
                with cols_bottom[i % 5]:
                    st.image(poster)
                    st.button(title, on_click=click_button, args=[title])


# Gestion de l'URL pour rediriger vers la recherche 
# if 'search_query' in st.query_params: 
#     search_query = st.query_params['search_query'][0] 
#     resultat_recherche(search_query)
