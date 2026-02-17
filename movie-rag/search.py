from google import genai
from db import supabase_client
from constants import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

content = "A man with of a man with a low IQ"

embedding = client.models.embed_content(
    model="gemini-embedding-001",
    contents=content
)

response = supabase_client.rpc('match_movies', {
    "query_embedding": embedding.embeddings[0].values,
    "match_threshold": 0.2,
    "match_count": 3
}).execute()

movies = response.data
print(movies)
