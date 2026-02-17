import constants
from supabase import create_client, Client

supabase_client: Client = create_client(constants.SUPABASE_URL, constants.SUPABASE_KEY)

def get_movies():
    response = supabase_client.table("movies").select("*").execute()
    return response.data

def insert_movie(movie_data):
    response = supabase_client.table("movies").insert(movie_data).execute()
    return response.data


