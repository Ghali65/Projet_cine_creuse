import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_tags import st_tags
from itertools import chain

def menu():
    with st.sidebar:
        val_menu = option_menu(menu_title=None, options=["Menu principal", "Recherche avancée", "Informations"], icons=['house', 'search','info'])
        if st.session_state["film_click"]:
            st.session_state["selection"] = "Menu principal" 
            st.session_state["film_click"] = False
            
        else:
            st.session_state["selection"] = val_menu
        # Retourner la sélection pour afficher le contenu principal
def list_unik(liste):
    return list(set(list(chain.from_iterable(liste))))

@st.cache_data
def create_df_final():
    df_final = pd.read_csv('df_final_title_stem.csv')
    df_search = pd.read_csv('reco_title_stem.csv')
    df_final['Titres_voisins'] = df_final['Titres_voisins'].apply(pd.eval)
    df_final['directors'] = df_final['directors'].apply(pd.eval)
    df_final['production_companies_name'] = df_final['production_companies_name'].apply(pd.eval)
    df_final['genres_x'] = df_final['genres_x'].apply(pd.eval)
    df_final['primaryName'] = df_final['primaryName'].apply(pd.eval)
    df_final = df_final.sort_values(by='averageRating', ascending=False)
    genre_x = list_unik(df_final['genres_x']) #créé une liste unique de tous les genres
    directors = list_unik(df_final['directors']) #créé une liste unique de tous les directors
    actors = list_unik(df_final['primaryName']) #créé une liste unique de tous les acteurs
    return df_final, df_search, genre_x, directors, actors

    # Lire les CSV pour les DataFrames
    
df_final, df_search, genre_x, directors, actors = create_df_final()

# Ajouter une option vide comme première option 
options = [''] + df_search['title_y'].tolist()

if "film_click" not in st.session_state:
    st.session_state["film_click"] = False

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
    st.session_state["film_click"] = True
    st.session_state["film_actuel"] = title
    st.session_state["lookreco"] = True


def logo():
    fond_accueil = "fond_logos.png"
    return st.image(fond_accueil, caption=None, width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=True)


if "film_actuel" not in st.session_state:
    st.session_state["film_actuel"] = None
    st.session_state["lookreco"] = False


menu()
if st.session_state["selection"] == "Menu principal":
    #image d'accueil :
    logo()
    search_query = st.selectbox('Que voulez-vous regarder ?', options=options)
    if search_query and st.session_state["lookreco"] is False: # reco par recherche, ca rentre si look reco false
        print("oOKOKOKOKOKOKO")
        st.session_state["film_actuel"] = search_query
    if st.session_state["film_actuel"] is not None:
        # Barre de recherche

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

elif st.session_state["selection"] == "Recherche avancée":
    #image d'accueil :
    logo()
    # Appliquer les styles CSS pour réduire la taille du label et ajuster la barre de tags
    st.markdown(""" <style> .stTags label { font-size: 10px; /* Taille de la police du label */ } 
                .stTags-content { width: 80px; } </style> """, unsafe_allow_html=True)
    # Créer des colonnes pour selecteur de critères:
    col_genre, col_directors = st.columns(2)
    with col_genre:
        key_genre = st_tags(
        text='tab + Entrée pour plus de critères',
        label='Choississez vos genres de film :',
        suggestions= genre_x,
        maxtags = -1,
        key='1')
    with col_directors:
        key_directors = st_tags(
        text='tab + Entrée pour plus de critères',
        label='Choississez vos réalisateurs :',
        suggestions= directors,
        maxtags = -1,
        key='2')
    key_actors = st_tags(
    text='tab + Entrée pour plus de critères',
    label='Choississez vos acteurs :',
    suggestions= actors,
    maxtags = -1,
    key='3')    
    print(key_genre)
    print(key_directors)

    if key_genre==[] and key_directors==[] and key_actors == [] :
        df_advanced_search=[]
    
    else :
        df_advanced_search = df_final[(df_final['genres_x'].apply(lambda row: set(key_genre).issubset(set(row)))) & 
                                    (df_final['directors'].apply(lambda row: set(key_directors).issubset(set(row)))) &
                                    (df_final['primaryName'].apply(lambda row: set(key_actors).issubset(set(row))))]

    print(df_advanced_search)
     
    list_titles = []
    liste_poster_result = []
    
    for movie in range(len(df_advanced_search)):
        df_result_search = df_advanced_search[df_advanced_search.index == df_advanced_search.index[movie]]
        if not df_advanced_search.empty:
            title = df_result_search['title_y'].iloc[0]
            poster = df_result_search['url_poster_path'].iloc[0]
            list_titles.append(title)
            liste_poster_result.append(poster)        
        else:
            liste_poster_result.append("")
            list_titles.append("")
        

    results_per_page = 20

    total_results = len(list_titles)
    total_pages = (total_results - 1) // results_per_page + 1

    # Sélecteur de page
    if total_results != 0 :
        page_number = st.number_input(f'Selectionner votre page parmis les {total_pages}', min_value=1, max_value=total_pages, step=1)
    
        # Calculer les index de début et de fin pour la page actuelle
        start_index = (page_number - 1) * results_per_page
        end_index = start_index + results_per_page

        # Sélectionner les résultats pour la page actuelle
        current_posters = liste_poster_result[start_index:end_index]
        current_titles = list_titles[start_index:end_index]

        # Créer des colonnes pour l'affichage
        cols_top = st.columns(5)
        cols_sub_top = st.columns(5)
        cols_sub_bottom = st.columns(5)
        cols_bottom = st.columns(5) 

        for i, (poster, title) in enumerate(zip(current_posters, current_titles)):
            if poster:  # Vérifie si l'URL du poster n'est pas vide
                if i < 5:
                        with cols_top[i % 5]:
                            st.image(poster)
                            st.button(title, on_click=click_button, args=[title])
                elif i >= 5 and i < 10 :
                        with cols_sub_top[i % 5]:
                            st.image(poster)
                            st.button(title, on_click=click_button, args=[title])
                elif i>=10 and i < 15 :
                        with cols_sub_bottom[i % 5]:
                            st.image(poster)
                            st.button(title, on_click=click_button, args=[title])
                else:
                    with cols_bottom[i % 5]:
                        st.image(poster)
                        st.button(title, on_click=click_button, args=[title])

 
    
