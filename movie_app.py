import streamlit as st
import requests

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Movie Recommendation App",
    page_icon="🎬",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown(
    "<h1 style='text-align: center; color: #FF5733;'>🎬 Movie Recommendation App</h1>",
    unsafe_allow_html=True
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Recommendations", "About"])

# ---------- TMDB API ----------
API_KEY = "YOUR_TMDB_API_KEY"  # Replace with your key
BASE_URL = "https://api.themoviedb.org/3"

def search_movie(movie_name):
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []

def get_recommendations(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []

# ---------- PAGE LOGIC ----------
if page == "Home":
    st.subheader("Welcome!")
    st.write("This app recommends movies based on your search using TMDB API.")
    st.image("https://i.imgur.com/4M7IWwP.png", use_container_width=True)
    st.markdown("**Built with ❤️ by Nanda Viji**")

elif page == "Recommendations":
    movie_name = st.text_input("Enter a movie name (e.g., Inception, Titanic)")
    if st.button("Get Recommendations"):
        with st.spinner("Fetching recommendations..."):
            results = search_movie(movie_name)
            if results:
                first_movie = results[0]
                movie_id = first_movie["id"]
                recommendations = get_recommendations(movie_id)
                st.subheader(f"Top Recommendations for {first_movie['title']}:")
                
                # Show movies in grid
                cols = st.columns(3)
                for i, movie in enumerate(recommendations[:9]):
                    with cols[i % 3]:
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else "https://via.placeholder.com/200x300"
                        st.image(poster_url, width=200)
                        st.caption(f"{movie['title']} ({movie['release_date'][:4] if movie.get('release_date') else 'N/A'})")
                st.balloons()
            else:
                st.warning("No movies found. Try another name!")

elif page == "About":
    with st.expander("About This App"):
        st.write("""
        This is a personalized Movie Recommendation app built with:
        - Streamlit (Web Framework)
        - TMDB API (Movie Database)
        - Python (Requests, JSON)
        """)
    st.success("Thanks for visiting!")

