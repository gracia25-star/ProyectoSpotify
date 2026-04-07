import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# =====================
# 1. CONFIGURACIÓN DE AUTENTICACIÓN
# =====================
CLIENT_ID = "cb95bf4bad0345538b2c550a2abcb082"
CLIENT_SECRET = "fdb4449072494f25b5e632be29d92092"
REDIRECT_URI = "http://127.0.0.1:8888/callback"  # Debe coincidir con la app de Spotify
SCOPE = "playlist-read-private"

# Crear objeto de autenticación
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# =====================
# 2. FUNCIONES
# =====================
def fetch_playlist_tracks(playlist_id):
    """
    Devuelve todas las canciones de una playlist en una lista de diccionarios
    """
    results = sp.playlist_items(playlist_id, additional_types=["track"])
    tracks = results["items"]

    # Si hay más de 100 canciones, paginamos
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    all_tracks = []
    for item in tracks:
        track = item.get("track")
        if track:  # Verificamos que haya un track (para evitar errores)
            all_tracks.append({
                "track_name": track["name"],
                "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "popularity": track["popularity"],
                "duration_ms": track["duration_ms"],
                "track_url": track["external_urls"]["spotify"]
            })
    return all_tracks

# =====================
# 3. DESCARGAR PLAYLIST
# =====================
# Cambia esto por la URL o ID de tu playlist
playlist_id = "https://open.spotify.com/playlist/0HWA092vyoNiKlCip3rJ8j?si=ff0dde6a327d461e"

tracks_data = fetch_playlist_tracks(playlist_id)

# =====================
# 4. GUARDAR EN CSV
# =====================
df = pd.DataFrame(tracks_data)
df.to_csv("playlist.csv", index=False)
print(f"Se han descargado {len(df)} canciones y guardado en 'playlist.csv'")

# =====================
# 5. VISTA PREVIA
# =====================
print(df.head())