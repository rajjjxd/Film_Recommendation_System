import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7ed0b2b4d0eadfa99a691bdc5551fc49&language=en-US')
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return ""

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

moviedict_list = pickle.load(open('moviedict_list.pkl', 'rb'))
movies = pd.DataFrame(moviedict_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))



# Input Section
st.sidebar.title('Enter the name of the Movie')
selected_movie_name = st.sidebar.selectbox('Select Movie', movies['title'].values)

# Recommendation Section
if st.sidebar.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.title('Recommended Movies')
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
