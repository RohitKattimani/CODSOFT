from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Complete movie database (shared with frontend)
movies_data = [
    {"id": 1, "title": "Inception", "genres": ["Action", "Sci-Fi", "Thriller"], "description": "A thief who steals corporate secrets through dream-sharing technology.", "poster": "https://picsum.photos/id/1015/320/420", "imdbRating": 8.8},
    {"id": 2, "title": "The Matrix", "genres": ["Action", "Sci-Fi"], "description": "A computer hacker discovers the shocking truth about his reality.", "poster": "https://picsum.photos/id/133/320/420", "imdbRating": 8.7},
    {"id": 3, "title": "Interstellar", "genres": ["Adventure", "Drama", "Sci-Fi"], "description": "Explorers travel through a wormhole in search of a new home for humanity.", "poster": "https://picsum.photos/id/160/320/420", "imdbRating": 8.7},
    {"id": 4, "title": "Dune: Part Two", "genres": ["Action", "Adventure", "Drama", "Sci-Fi"], "description": "Paul Atreides unites with Chani and the Fremen people in a war for the universe.", "poster": "https://picsum.photos/id/201/320/420", "imdbRating": 8.8},
    {"id": 5, "title": "Oppenheimer", "genres": ["Biography", "Drama", "History"], "description": "The story of the American scientist who developed the atomic bomb.", "poster": "https://picsum.photos/id/211/320/420", "imdbRating": 8.4},
    {"id": 6, "title": "Parasite", "genres": ["Drama", "Thriller"], "description": "Greed and class discrimination threaten a poor family’s new relationship with the rich.", "poster": "https://picsum.photos/id/29/320/420", "imdbRating": 8.5},
    {"id": 7, "title": "Everything Everywhere All at Once", "genres": ["Action", "Adventure", "Comedy", "Sci-Fi"], "description": "An aging Chinese immigrant is swept into an insane multiverse adventure.", "poster": "https://picsum.photos/id/1009/320/420", "imdbRating": 7.8},
    {"id": 8, "title": "Mad Max: Fury Road", "genres": ["Action", "Adventure", "Sci-Fi"], "description": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler.", "poster": "https://picsum.photos/id/1016/320/420", "imdbRating": 8.1},
    {"id": 9, "title": "La La Land", "genres": ["Comedy", "Drama", "Musical", "Romance"], "description": "A jazz pianist and an aspiring actress fall in love while chasing their dreams.", "poster": "https://picsum.photos/id/870/320/420", "imdbRating": 8.0},
    {"id": 10, "title": "The Grand Budapest Hotel", "genres": ["Adventure", "Comedy", "Drama"], "description": "The adventures of a legendary concierge and a lobby boy at a famous hotel.", "poster": "https://picsum.photos/id/1011/320/420", "imdbRating": 8.1},
    {"id": 11, "title": "Joker", "genres": ["Crime", "Drama", "Thriller"], "description": "A failed comedian descends into madness and becomes the criminal mastermind Joker.", "poster": "https://picsum.photos/id/1020/320/420", "imdbRating": 8.4},
    {"id": 12, "title": "Spider-Man: Across the Spider-Verse", "genres": ["Animation", "Action", "Adventure"], "description": "Miles Morales embarks on an epic journey across the multiverse with other Spider-People.", "poster": "https://picsum.photos/id/1040/320/420", "imdbRating": 8.6}
]

class RecommendRequest(BaseModel):
    liked_ids: List[int]

def get_all_genres():
    genres = set()
    for movie in movies_data:
        for g in movie["genres"]:
            genres.add(g)
    return sorted(list(genres))

all_genres = get_all_genres()

def get_movie_vector(movie: Dict, genres_list: List[str]):
    return [1 if g in movie["genres"] else 0 for g in genres_list]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = (sum(x * x for x in a)) ** 0.5
    mag_b = (sum(x * x for x in b)) ** 0.5
    return dot / (mag_a * mag_b) if mag_a and mag_b else 0.0

def get_recommendations(liked_ids: List[int]) -> List[Dict]:
    if not liked_ids:
        return []
    liked_movies = [m for m in movies_data if m["id"] in liked_ids]
    if not liked_movies:
        return []
    user_vector = [0.0] * len(all_genres)
    for movie in liked_movies:
        vec = get_movie_vector(movie, all_genres)
        user_vector = [u + v for u, v in zip(user_vector, vec)]
    user_vector = [v / len(liked_movies) for v in user_vector]
    scored = []
    for movie in movies_data:
        if movie["id"] in liked_ids:
            continue
        vec = get_movie_vector(movie, all_genres)
        similarity = cosine_similarity(user_vector, vec)
        scored.append({**movie, "similarity": round(similarity, 4)})
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:8]

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/recommend")
async def recommend(req: RecommendRequest):
    recs = get_recommendations(req.liked_ids)
    return {"recommendations": recs}

@app.get("/api/movies")
async def get_movies():
    return {"movies": movies_data}