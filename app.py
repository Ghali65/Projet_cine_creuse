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
st.title('Barre de Recherche sur Streamlit')

# Ajouter une option vide comme première option 
options = [''] + df_search['title_y'].tolist()

# Barre de recherche
search_query = st.selectbox('Que voulez-vous regarder ?', options=options)

def resultat_recherche(text):
    st.subheader('Résultats de la recherche :')
    film_details = df_final[df_search['title_y'] == text]
    if film_details.empty:
        st.write(f"Aucun résultat trouvé pour : {text}")
    else:
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

# Gestion de l'URL pour rediriger vers la recherche 


if search_query:
    resultat_recherche(search_query)
    st.subheader('Nos recommandations :')
    film_recommandation = df_final[df_search['title_y'] == search_query]
    liste_reco = film_recommandation['Titres_voisins'].iloc[0]
    liste_poster = []

    for movie in range(10):
        film_details = df_final[df_search['title_y'] == liste_reco[movie]]
        if not film_details.empty:
            film_poster = film_details['url_poster_path'].iloc[0]
            liste_poster.append(film_poster)
        else:
            liste_poster.append("")

    # CSS pour aligner les images et les titres 
    st.markdown(""" 
        <style> 
        .poster-container { 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            text-align: center; 
            padding: 10px; 
        } 
        .poster-container img { 
            width: 100%; 
            height: auto; 
        } 
        </style> 
        """, unsafe_allow_html=True) 

    # Afficher les résultats dans deux rangées de cinq colonnes 
    cols_top = st.columns(5) 
    cols_bottom = st.columns(5) 
    for i, (poster, title) in enumerate(zip(liste_poster, liste_reco)): 
        if poster:  
            markdown_content = f""" 
                <div class="poster-container"> 
                        <img src="{poster}" alt="{title}"> 
                        <div>{title}</div> 
                    </a>
                </div> 
            """ 
            if i < 5: 
                with cols_top[i % 5]: 
                    st.markdown(markdown_content, unsafe_allow_html=True) 
            else: 
                with cols_bottom[i % 5]: 
                    st.markdown(markdown_content, unsafe_allow_html=True)

# Gestion de l'URL pour rediriger vers la recherche 


                

# test_items = [
#     dict(
#         title="Slide 1",
#         text="A tree in the savannah",
#         img="https://img.freepik.com/free-photo/wide-angle-shot-single-tree-growing-clouded-sky-during-sunset-surrounded-by-grass_181624-22807.jpg?w=1380&t=st=1688825493~exp=1688826093~hmac=cb486d2646b48acbd5a49a32b02bda8330ad7f8a0d53880ce2da471a45ad08a4",    
#         link="https://discuss.streamlit.io/t/new-component-react-bootstrap-carousel/46819",
#     ),
#     dict(
#         title="Slide 2",
#         text="A wooden bridge in a forest in Autumn",
#         img="https://img.freepik.com/free-photo/beautiful-wooden-pathway-going-breathtaking-colorful-trees-forest_181624-5840.jpg?w=1380&t=st=1688825780~exp=1688826380~hmac=dbaa75d8743e501f20f0e820fa77f9e377ec5d558d06635bd3f1f08443bdb2c1",
#         link="https://github.com/thomasbs17/streamlit-contributions/tree/master/bootstrap_carousel",
#     ),
#     dict(
#         title="Slide 3",
#         text="A distant mountain chain preceded by a sea",
#         img="https://img.freepik.com/free-photo/aerial-beautiful-shot-seashore-with-hills-background-sunset_181624-24143.jpg?w=1380&t=st=1688825798~exp=1688826398~hmac=f623f88d5ece83600dac7e6af29a0230d06619f7305745db387481a4bb5874a0",
#         link="https://github.com/thomasbs17/streamlit-contributions/tree/master",
#     ),
#     dict(
#         title="Slide 4",
#         text="PANDAS",
#         img="pandas.webp",
#     ),
#     dict(
#         title="Slide 4",
#         text="CAT",
#         img="cat.jpg",
#     ),
# ]

# carousel(items=test_items)

