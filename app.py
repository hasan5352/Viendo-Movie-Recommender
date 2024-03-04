import streamlit as st
import pickle
import pandas as pd
import model

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)




st.title('Viendo Recommends you movies!')
selected_movie = st.selectbox('Pick a movie', movies['title'].values)

n = 5
if st.button("Recommend"):
    similar_movies, posters = model.recommend(selected_movie, n)
    cols = st.columns(n)
    for i, (movie, poster) in enumerate(zip(similar_movies, posters)):
        with cols[i]:
            st.text(movie)
            st.image(poster)


