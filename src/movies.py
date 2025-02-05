import streamlit as st
import pandas as pd
import ast  # Para convertir strings en listas de Python

# Cargar el dataset
df = pd.read_csv("tmdb_5000_movies.csv")

# Función para extraer los nombres de los géneros
def extract_genre_names(genre_str):
    try:
        genres = ast.literal_eval(genre_str)  # Convierte el string en lista de diccionarios
        return [genre['name'] for genre in genres]  # Extrae los nombres
    except (ValueError, SyntaxError):
        return []  # En caso de error, devuelve una lista vacía

# Extraer y limpiar nombres de géneros eliminando NaN
all_genres = df['genres'].dropna().apply(extract_genre_names).explode().dropna().unique()

# Convertir a lista y eliminar posibles valores no string
all_genres = [genre for genre in all_genres if isinstance(genre, str)]

# Agregar una opción vacía al inicio
all_genres.insert(0, "Selecciona un género")

# Encabezado estilo marquesina de cine
st.markdown("<h1 style='text-align: center; color: red;'>🎬 Movie Recommendations 🎬</h1>", unsafe_allow_html=True)

# Seleccionar género con la opción vacía
genre = st.selectbox("🍿", all_genres, index=0)

# Función para obtener películas por género
def get_movies_by_genre(genre):
    filtered_movies = df[df['genres'].apply(lambda x: genre in extract_genre_names(x))]
    return filtered_movies[['title']]

# Mostrar películas solo si se ha seleccionado un género válido
if genre != "Selecciona un género":
    movies = get_movies_by_genre(genre)
    st.write(f"### Películas de {genre}")
    movie_titles = movies['title'].tolist()
    if movie_titles:
        for title in movie_titles:
            st.write(f"- {title}")
    else:
        st.write("No hay películas disponibles para este género.")
