import streamlit as st
import pandas as pd


df_search = pd.read_csv('reco.csv')
filtered_df = pd.read_csv('df_final.csv')

def result(movie):
    col1, col2 = st.columns(2)
    pd.set_option('display.max_colwidth', None)
    with col1:
        df_search = pd.read_csv('reco.csv')
        filtered_df = pd.read_csv('df_final.csv')
        filtered_df = filtered_df[df_search['title_y'].str.contains(movie, case=False, na=False)]
        st.title(filtered_df)

    with col2:
        st.header("A dog")
        
    return col1, col2



# Titre de l'application
st.title('Barre de Recherche sur Streamlit')

# Barre de recherche
search_query = st.text_input('Entrez votre recherche ici')



# Filtrer le DataFrame en fonction de la saisie utilisateur
if search_query:
    col1, col2 = st.columns(2)
    pd.set_option('display.max_colwidth', None)
    with col1:
        filtered_df = filtered_df.apply([df_search['title_y'].str.contains(search_query, case=False, na=False)])
        st.title(filtered_df)    
    with col2:
        st.header("A dog")
else :
    st.header('')

# Afficher le DataFrame filtré
st.write('Résultats de la recherche :')


