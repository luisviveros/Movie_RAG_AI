import json
import sys
sys.path.append('..')
from google import genai
from systemMessage import system_message
from db import supabase_client
from constants import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

user_question = "Quiero una película sobre un caballero de la noche"

# Buscar películas relevantes usando embeddings
embedding = client.models.embed_content(
    model="gemini-embedding-001",
    contents=user_question
)

movies_response = supabase_client.rpc('match_movies', {
    "query_embedding": embedding.embeddings[0].values,
    "match_threshold": 0.2,
    "match_count": 3
}).execute()

movies = movies_response.data

# Generar respuesta con Gemini
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        f"{system_message}\n\nPregunta del usuario: {user_question}\n\nContexto: {json.dumps(movies)}"
    ],
    config={
        "temperature": 1,
        "max_output_tokens": 2048,
        "top_p": 1
    }
)

print(response.text)