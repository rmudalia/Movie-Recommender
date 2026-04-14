# tmdb.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER = "https://via.placeholder.com/500x750?text=No+Poster"


def get_poster(movie_title):
    """
    Fetch movie poster URL from TMDB by title.
    Strips the year from the title before searching (e.g. "Toy Story (1995)" -> "Toy Story")
    Returns a poster URL string, or a placeholder if not found.
    """
    # Strip year from title if present e.g. "Toy Story (1995)" -> "Toy Story"
    import re
    clean_title = re.sub(r'\s*\(\d{4}\)\s*$', '', movie_title).strip()
    
    try:
        url = f"{BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": clean_title,
            "language": "en-US",
            "page": 1
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        results = data.get('results', [])
        if results and results[0].get('poster_path'):
            return IMAGE_BASE_URL + results[0]['poster_path']
        else:
            return PLACEHOLDER
            
    except Exception:
        return PLACEHOLDER


def get_movie_details(movie_title):
    """
    Fetch movie details (overview, rating, year) from TMDB.
    Returns a dict with overview, vote_average, release_date.
    """
    import re
    clean_title = re.sub(r'\s*\(\d{4}\)\s*$', '', movie_title).strip()
    
    try:
        url = f"{BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": clean_title,
            "language": "en-US",
            "page": 1
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        results = data.get('results', [])
        if results:
            movie = results[0]
            return {
                'overview': movie.get('overview', 'No description available.'),
                'rating': movie.get('vote_average', 'N/A'),
                'year': movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A',
                'poster': IMAGE_BASE_URL + movie['poster_path'] if movie.get('poster_path') else PLACEHOLDER
            }
    except Exception:
        pass
    
    return {
        'overview': 'No description available.',
        'rating': 'N/A',
        'year': 'N/A',
        'poster': PLACEHOLDER
    }