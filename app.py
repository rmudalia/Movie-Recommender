# app.py

import streamlit as st
from recommender import load_data, build_similarity_matrix, recommend
from tmdb import get_poster, get_movie_details

# ─────────────────────────────────────────────
# Page config — must be the first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ─────────────────────────────────────────────
# Load data once and cache it
# @st.cache_data means it only runs once — not on every interaction
# ─────────────────────────────────────────────
@st.cache_data
def load():
    movies = load_data()
    similarity = build_similarity_matrix(movies)
    return movies, similarity

movies, similarity = load()

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.title("🎬 Movie Recommender")
st.markdown("Type a movie you like and get 5 similar recommendations.")
st.markdown("---")

# ─────────────────────────────────────────────
# Search input
# ─────────────────────────────────────────────
col_input, col_btn = st.columns([4, 1])

with col_input:
    movie_input = st.text_input(
        label="Movie title",
        placeholder="e.g. Toy Story, The Matrix, Inception...",
        label_visibility="collapsed"
    )

with col_btn:
    search = st.button("Recommend", use_container_width=True)

# ─────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────
if search or movie_input:
    if not movie_input.strip():
        st.warning("Please enter a movie title.")
    else:
        with st.spinner("Finding recommendations..."):
            results = recommend(movie_input, movies, similarity, n=5)
        
        if not results:
            st.error(f"Could not find '{movie_input}' in the dataset. Try a different title.")
            st.info("Tip: Try searching with just part of the title, e.g. 'toy' instead of 'Toy Story (1995)'")
        else:
            # Show what movie was matched
            st.success(f"Showing recommendations based on: **{results[0]['matched_title']}**")
            st.markdown("---")
            
            # Display 5 results in columns
            cols = st.columns(5)
            
            for i, col in enumerate(cols):
                result = results[i]
                with col:
                    # Fetch poster
                    poster_url = get_poster(result['title'])
                    st.image(poster_url, use_container_width=True)
                    
                    # Movie title
                    st.markdown(f"**{result['title']}**")
                    
                    # Genres as tags
                    st.caption(result['genres'])
                    
                    # Similarity score
                    st.caption(f"Match score: {result['score']}")

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("Built with MovieLens data · Powered by TF-IDF + Cosine Similarity · Posters from TMDB")