#creating the backend using streamlit
import streamlit as st 
import pickle
import requests 
import pandas as pd 

st.markdown(
    '''
    <style>
    .reportview-container {
        background: url("space.jpeg")
    }
    </style>
    ''',
    unsafe_allow_html=True)

movie_dict = pickle.load(open("movies.pkl","rb"))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open("similar.pkl","rb"))

#movie.pkl will contain the dataframe "movie_final"

st.title("Movie Recommendation System")

#taking user input
#show the movie list
selected_movie_name = st.selectbox("Select a Movie",movies['title'].values)

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=74d5023529083f68715a60e7caafd6db&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data["poster_path"]

def recommend(movie):
        movie_index = movies[movies["title"] == movie].index[0]
        distance = similarity[movie_index]
        movie_list = sorted(list(enumerate(distance)),reverse = True, key = lambda x : x[1])[1:6]
        
        recommended_movies = []
        recommended_posters = []
        for i in movie_list:
            movie_id = movies.iloc[i[0]].id
            #now fetch poster
            recommended_movies.append(movies.iloc[i[0]].title)
            poster = fetch_poster(movie_id)
            recommended_posters.append(poster)
        return recommended_movies,recommended_posters

if st.button("recommend"):
    st.write('Try these:') 
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
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


#now lets show the poster of recommended movies 
#we will fetch the poster by its id 
#updates made in recommender function 


