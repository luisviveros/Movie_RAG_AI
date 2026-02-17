from data import movies
from google import genai
from db import insert_movie
from constants import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

data = [
    {
        "id": movie["id"],
        "title": movie["title"],
        "overview": movie["overview"],
        "release_date": movie["release_date"]
    }
    for movie in movies["results"]
]

for movie in data:
    embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents=f"Title: {movie['title']} Overview: {movie['overview']}"
    )

    movie_data = {
        "id": movie["id"],
        "vector": embedding.embeddings[0].values,
        "content": f"Title: {movie['title']} Overview: {movie['overview']}",
        "metadata": {
            "id": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"]
        }
    }

    insert_movie(movie_data)
    print(f"Inserted: {movie['title']}")