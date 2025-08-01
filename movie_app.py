import streamlit as st
import requests

# TMDB API key
API_KEY = "aafab8350973c56c9df7f28edb184e26"
BASE_URL = "https://api.themoviedb.org/3"

st.title("🎬 Movie Recommendation App")
st.write("Search for a movie and get recommendations instantly!")

def search_movie(name):
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={name}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json().get('results', [])

def get_recommendations(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations?api_key={API_KEY}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json().get('results', [])

movie_name = st.text_input("Enter Movie Name")

if st.button("Get Recommendations"):
    if not movie_name.strip():
        st.warning("Please enter a movie name.")
    else:
        try:
            results = search_movie(movie_name)
            if results:
                movie_id = results[0]['id']
                st.subheader(f"Recommendations based on {results[0]['title']}")
                recommendations = get_recommendations(movie_id)
                if recommendations:
                    for movie in recommendations[:5]:
                        st.markdown(f"### {movie['title']} ({movie.get('release_date', 'N/A')})")
                        poster_path = movie.get('poster_path')
                        if poster_path:
                            st.image(f"https://image.tmdb.org/t/p/w200{poster_path}")
                        st.write(movie.get('overview', 'No overview available.'))
                        st.write("---")
                else:
                    st.info("No recommendations found.")
            else:
                st.warning("No movie found. Try another name.")
        except Exception as e:
            st.error(f"Error: {e}")
