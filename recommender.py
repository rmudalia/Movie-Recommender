# recommender.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data():
    """Load and prepare the MovieLens dataset."""
    movies = pd.read_csv('data/movies.csv')
    
    # Clean genres — replace pipe separator with space
    movies['genres_clean'] = movies['genres'].str.replace('|', ' ', regex=False)
    
    # Drop movies with no genres listed
    movies = movies[movies['genres'] != '(no genres listed)'].reset_index(drop=True)
    
    return movies


def build_similarity_matrix(movies):
    """Build TF-IDF matrix and cosine similarity matrix from genres."""
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['genres_clean'])
    similarity = cosine_similarity(tfidf_matrix)
    return similarity


def recommend(title, movies, similarity, n=5):
    """
    Given a movie title, return n most similar movies.
    
    Args:
        title: movie title string (e.g. "Toy Story (1995)")
        movies: the movies dataframe
        similarity: the precomputed cosine similarity matrix
        n: number of recommendations to return
    
    Returns:
        list of dicts with title and genres, or empty list if not found
    """
    # Search for the movie — case insensitive partial match
    matches = movies[movies['title'].str.lower().str.contains(title.lower())]
    
    if matches.empty:
        return []
    
    # Use the first match
    idx = matches.index[0]
    matched_title = movies.iloc[idx]['title']
    
    # Get similarity scores
    scores = list(enumerate(similarity[idx]))
    
    # Sort by score, exclude the movie itself
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = [s for s in scores if s[0] != idx][:n]
    
    # Build result list
    results = []
    for i, score in scores:
        results.append({
            'title': movies.iloc[i]['title'],
            'genres': movies.iloc[i]['genres'].replace('|', ' · '),
            'score': round(score, 3),
            'matched_title': matched_title
        })
    
    return results


# Quick test — run this file directly to verify it works
if __name__ == '__main__':
    print("Loading data...")
    movies = load_data()
    print(f"Loaded {len(movies)} movies")
    
    print("\nBuilding similarity matrix...")
    similarity = build_similarity_matrix(movies)
    print("Done")
    
    print("\nTest recommendations for 'Toy Story':")
    results = recommend("Toy Story", movies, similarity)
    for r in results:
        print(f"  {r['title']} ({r['genres']}) — score: {r['score']}")