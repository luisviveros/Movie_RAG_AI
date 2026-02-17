import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from google import genai
from db import supabase_client
from constants import GEMINI_API_KEY
from chat.systemMessage import system_message

app = FastAPI()

client = genai.Client(api_key=GEMINI_API_KEY)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    question = body.get("question", "")

    if not question.strip():
        return {"error": "La pregunta no puede estar vacía"}

    # Generar embedding de la pregunta
    embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    # Buscar películas similares en Supabase
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
            f"{system_message}\n\nPregunta del usuario: {question}\n\nContexto: {json.dumps(movies)}"
        ],
        config={
            "temperature": 1,
            "max_output_tokens": 2048,
            "top_p": 1
        }
    )

    return {"answer": response.text, "movies": movies}
