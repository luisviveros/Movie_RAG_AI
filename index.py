import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'movie-rag'))
from google import genai
from constants import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="Hola soy el primer embedding del curso de Rag en EDTEAM"
)

print(result.embeddings)
