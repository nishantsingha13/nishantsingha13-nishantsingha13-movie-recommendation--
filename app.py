import pickle
import streamlit as st
import pandas as pd
import requests
import gzip

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load movie data and similarity matrix
movies_dicts = pickle.load(open("movies.to_dict()", "rb"))
movies = pd.DataFrame(movies_dicts)

with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

# Streamlit app interface
st.title("MOVIE RECOMMENDER SYSTEM")
selected_movie_name = st.selectbox("Select a movie", movies["title"].values)

if st.button('SHOW RECOMMENDATION'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

# Add footer
st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Created by Nishant Singhal</p>", unsafe_allow_html=True)
