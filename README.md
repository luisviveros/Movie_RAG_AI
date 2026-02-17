# Movie RAG - Sistema de Recomendacion de Peliculas con IA

Sistema de recomendaciones de peliculas basado en **Retrieval-Augmented Generation (RAG)** con interfaz web interactiva. Utiliza embeddings vectoriales para busqueda semantica y un LLM para generar recomendaciones personalizadas en lenguaje natural.

## Caracteristicas

- Busqueda semantica de peliculas usando embeddings vectoriales
- Generacion de recomendaciones en lenguaje natural con Google Gemini
- Interfaz web tipo chat interactiva
- Soporte multilenguaje (responde en el idioma del usuario)
- API REST con FastAPI

## Demo

La interfaz web permite hacer preguntas en lenguaje natural y recibir recomendaciones personalizadas:

```
Usuario: "Quiero ver algo de ciencia ficcion"
Bot:     Basandome en las peliculas disponibles, te recomiendo Interstellar...
```

## Arquitectura

```
┌─────────────────────────────────────────────────┐
│                 Interfaz Web                     │
│              (HTML + CSS + JS)                   │
└──────────────────┬──────────────────────────────┘
                   │ POST /api/chat
                   v
┌─────────────────────────────────────────────────┐
│              FastAPI Backend                     │
│                 (app.py)                         │
│                                                  │
│  1. Recibe pregunta del usuario                  │
│  2. Genera embedding (gemini-embedding-001)      │
│  3. Busqueda vectorial en Supabase (cosine)      │
│  4. Recupera top 3 peliculas similares           │
│  5. Genera respuesta con Gemini 2.0 Flash        │
│  6. Retorna recomendacion al frontend            │
└────────┬────────────────────┬───────────────────┘
         │                    │
         v                    v
┌────────────────┐  ┌─────────────────────┐
│  Google Gemini │  │  Supabase (pgvector) │
│  - Embeddings  │  │  - Vector store      │
│  - LLM (Flash) │  │  - match_movies RPC  │
└────────────────┘  └─────────────────────┘
```

## Estructura del proyecto

```
RAG_Course/
├── movie-rag/
│   ├── app.py                  # Servidor FastAPI (punto de entrada web)
│   ├── static/
│   │   └── index.html          # Interfaz de chat
│   ├── chat/
│   │   ├── chat.py             # Pipeline RAG (CLI)
│   │   ├── gemini.py           # Cliente de Google Gemini
│   │   └── systemMessage.py    # System prompt del RAG
│   ├── chunks.py               # Chunking de texto con tokens
│   ├── constants.py            # Variables de entorno
│   ├── data.py                 # Dataset de 20 peliculas (TMDB)
│   ├── db.py                   # Operaciones con Supabase
│   ├── index.py                # Indexacion de peliculas
│   ├── search.py               # Busqueda semantica
│   └── text.py                 # Peliculas formateadas como texto
├── index.py                    # Test basico de embeddings
├── .env                        # Variables de entorno (no se sube a git)
├── .env.example                # Plantilla de variables de entorno
├── requirements.txt
├── .gitignore
└── README.md
```

## Stack tecnologico

| Componente | Tecnologia |
|---|---|
| Backend | Python 3.10+ / FastAPI |
| Frontend | HTML5 + CSS3 + JavaScript (vanilla) |
| LLM | Google Gemini 2.0 Flash |
| Embeddings | Google Gemini (`gemini-embedding-001`) |
| Base de datos vectorial | Supabase (PostgreSQL + pgvector) |
| Chunking | LangChain (`RecursiveCharacterTextSplitter`) |
| Tokenizacion | Tiktoken |

## Requisitos previos

- Python 3.10+
- Una API key de [Google AI Studio](https://aistudio.google.com/)
- Un proyecto en [Supabase](https://supabase.com/) con la extension `vector` habilitada

## Instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/movie-rag.git
cd movie-rag
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raiz del proyecto basado en `.env.example`:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
GEMINI_API_KEY=tu_api_key_de_gemini
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_key_de_supabase
```

### 5. Configurar Supabase

1. Habilitar la extension `vector` en tu proyecto de Supabase
2. Crear la tabla `movies` con columnas para almacenar embeddings vectoriales
3. Crear la funcion RPC `match_movies` para busqueda por similitud coseno

### 6. Indexar peliculas

```bash
cd movie-rag
python index.py
```

Esto genera embeddings para las 20 peliculas del dataset y los almacena en Supabase. Solo es necesario ejecutarlo una vez.

## Como ejecutar

### Interfaz web (recomendado)

```bash
cd movie-rag
uvicorn app:app --reload
```

Abrir en el navegador: **[http://localhost:8000](http://localhost:8000)**

### CLI (linea de comandos)

```bash
cd movie-rag/chat
python chat.py
```

### Scripts auxiliares

```bash
# Test basico de embeddings
python index.py

# Busqueda semantica directa
cd movie-rag
python search.py
```

## API

### POST /api/chat

Envia una pregunta y recibe una recomendacion de pelicula.

**Request:**

```json
{
  "question": "Quiero una pelicula sobre un caballero de la noche"
}
```

**Response:**

```json
{
  "answer": "Te recomiendo The Dark Knight...",
  "movies": [
    {
      "content": "Title: The Dark Knight Overview: ...",
      "metadata": { "title": "The Dark Knight", "release_date": "2008-07-16" }
    }
  ]
}
```

## Dataset

El proyecto utiliza las 20 peliculas mejor valoradas de [TMDB](https://www.themoviedb.org/):

The Shawshank Redemption, The Godfather, The Dark Knight, Interstellar, Forrest Gump, Parasite, Spirited Away, Schindler's List, Pulp Fiction, The Green Mile, The Lord of the Rings: The Return of the King, entre otras.

## Como funciona el RAG

1. **Indexacion**: Cada pelicula se convierte en un embedding vectorial usando `gemini-embedding-001` y se almacena en Supabase con pgvector
2. **Busqueda**: Cuando el usuario hace una pregunta, se genera un embedding de la consulta y se buscan las 3 peliculas mas similares por distancia coseno
3. **Generacion**: Las peliculas encontradas se pasan como contexto a Gemini 2.0 Flash junto con un system prompt que lo restringe a recomendar solo del contexto proporcionado
