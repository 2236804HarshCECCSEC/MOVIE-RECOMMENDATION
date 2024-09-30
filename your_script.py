import requests
import streamlit as st
import pickle
import pandas as pd

# Your Google API key and Custom Search Engine ID
API_KEY = 'ENTER YOUR API_KEY'  # Replace with your actual Google API key
CSE_ID = 'ENTER YOUR CSE_ID'  # Replace with your actual Custom Search Engine ID. Just chatgpt how to create then and you are good to go.

# Function to fetch the movie poster using Google Custom Search API
def fetch_poster(movie_title):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={movie_title}+movie+poster&cx={CSE_ID}&searchType=image&key={API_KEY}&num=1"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Check if the request was successful
        
        data = response.json()  # Parse the JSON response
        
        if 'items' in data:
            # Get the first image URL
            poster_url = data['items'][0]['link']
            return poster_url
        else:
            # If no image is found, return a placeholder image
            return "https://via.placeholder.com/500"
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500"  # Return a default image if an error occurs

# Function to recommend movies based on similarity and fetch their posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list[1:6]:  # Recommend 5 movies
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        # Fetch the movie poster using the fetch_poster function
        poster_url = fetch_poster(movie_title)
        recommended_movies_posters.append(poster_url)
    
    return recommended_movies, recommended_movies_posters

# Load the movie data and similarity model
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app UI
st.title('Movie Recommendation App')

# Dropdown to select a movie
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# Recommend button
if st.button('Recommend'):
    # Get recommendations and poster URLs
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    
    # Display recommendations with posters
    for i in range(len(recommended_movie_names)):
        st.text(recommended_movie_names[i])
        st.image(recommended_movie_posters[i])