import streamlit as st
import pandas as pd
from PIL import Image

# Cargar el dataset (Asegúrate de cargar el DataFrame previamente)
df = pd.read_csv("tmdb_5000_movies.csv")

# Función para obtener películas por género
def get_movies_by_genre(genre):
    filtered_movies = df[df['genres'].apply(lambda x: genre in x)]
    return filtered_movies[['title', 'poster_path']]

# Inicializar watchlist en la sesión
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# Diccionario de fondos por género (Simulado, puedes agregar más estilos dinámicos)
backgrounds = {
    "Action": "background-action.jpg",  # Replace with actual paths
    "Comedy": "background-comedy.jpg",  # Replace with actual paths
    "Drama": "background-drama.jpg",  # Replace with actual paths
    "Sci-Fi": "background-scifi.jpg",  # Replace with actual paths
}

# Encabezado estilo marquesina de cine
st.markdown("<h1 style='text-align: center; color: red;'>🎬 Cinema Carousel 🎬</h1>", unsafe_allow_html=True)

# Seleccionar género
genre = st.selectbox("Selecciona un género", df['genres'].explode().unique())

# Cambiar el fondo dinámico
if genre in backgrounds:
    # Check if the background image file exists
    try:
        with open(backgrounds[genre], "rb") as f:  # Try to open the file
            st.markdown(f"""
                <style>
                .stApp {{
                    background-image: url('{backgrounds[genre]}');
                    background-size: cover;
                }}
                </style>
            """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Background image '{backgrounds[genre]}' not found. Using default background.")
        # You could set a default background here if you have one.


# Obtener películas del género seleccionado
movies = get_movies_by_genre(genre)

# Carrusel de películas
st.write(f"### Películas de {genre}")
movie_titles = movies['title'].tolist()

if movie_titles: # Check if there are movies for the selected genre
    selected_movie = st.slider("Desliza para explorar películas", 0, len(movie_titles)-1, 0)

    # Mostrar cartel y nombre de la película seleccionada
    # Important: Make sure 'poster_path' contains valid URLs or local file paths.
    poster_path = movies.iloc[selected_movie]['poster_path']

    try:
        # Try displaying the image directly if it's a URL
        st.image(poster_path, caption=movies.iloc[selected_movie]['title'], width=200)
    except: # If it's not a URL, assume it's a local path
        try:
            st.image(poster_path, caption=movies.iloc[selected_movie]['title'], width=200)
        except FileNotFoundError:
            st.warning(f"Poster image '{poster_path}' not found.")
            st.write(f"**{movies.iloc[selected_movie]['title']}** (Poster not available)") # Display title even if poster is missing


    # Botón para agregar a la watchlist
    if st.button("Añadir a mi Watchlist"):
        if movies.iloc[selected_movie]['title'] not in st.session_state.watchlist: # Prevent duplicates
            st.session_state.watchlist.append(movies.iloc[selected_movie]['title'])
            st.success(f"{movies.iloc[selected_movie]['title']} añadida a la Watchlist")
        else:
            st.info(f"{movies.iloc[selected_movie]['title']} is already in your Watchlist.")

else:
    st.write("No movies found for this genre.")


# Display the watchlist
st.subheader("My Watchlist")
if st.session_state.watchlist:
    for movie in st.session_state.watchlist:
        st.write(f"- {movie}")
else:
    st.write("Your Watchlist is empty.")