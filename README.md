# 📊 Spotify Playlist KPI Dashboard

Aplicación interactiva desarrollada en **Python** utilizando **Streamlit** y **Plotly** para analizar y visualizar métricas (KPIs) de playlists de Spotify de manera dinámica y con animaciones.

Este proyecto permite explorar atributos musicales, popularidad y tendencias de canciones de forma visual e intuitiva.

---

# 🚀 Características principales

* 🎨 Dashboard interactivo con gráficos y tablas
* 📈 KPIs destacados de la playlist (canciones, artistas, álbumes, popularidad, duración)
* 🔥 Visualizaciones animadas con Plotly:

  * Top canciones
  * Distribución de popularidad
  * Scatter plots Duración vs Popularidad
  * Distribución de artistas
* 📋 Tabla interactiva para filtrar canciones por nombre o artista
* 🎛️ Filtros dinámicos: popularidad, artistas y álbumes
* ✨ Estética moderna con animaciones CSS y diseño dark mode

---

# 🧠 Objetivo del proyecto

Brindar una herramienta visual para analizar playlists de Spotify, facilitando:

* Comprender el perfil musical de la playlist
* Identificar patrones de popularidad y duración
* Destacar canciones y artistas más relevantes
* Explorar datos de manera interactiva

Ideal como proyecto de **Data Analytics / Data Science** o para mostrar en un portfolio profesional.

---

# 🛠️ Tecnologías utilizadas

* Python 3.9+
* Streamlit
* Plotly Express y Graph Objects
* Pandas
* Numpy
* Spotify Web API (para obtener los datasets)

---

# 🔑 Requisitos

1. Tener Python instalado (recomendado ≥ 3.9)
2. Instalar dependencias del proyecto
3. Contar con datasets CSV de Spotify (`dataset.csv` o `playlist.csv`)

---

# ⚙️ Instalación

Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/tu_repo.git
cd tu_repo
```

Crea y activa un entorno virtual:

```bash
python -m venv venv
# Mac/Linux
tsource venv/bin/activate
# Windows
venv\\Scripts\\activate
```

---

# ▶️ Ejecución de la aplicación

```bash
python -m streamlit run app.py
```

---

# 📊 KPIs incluidos

* Total de canciones
* Artistas únicos y dominantes
* Álbumes distintos y más raros
* Popularidad promedio y máxima
* Desviación estándar de popularidad
* Duración promedio y total de la playlist
* % de canciones virales (popularidad ≥ 70)
* Canción más popular

---

# 📁 Estructura del proyecto

```
project/
│
├── app.py              # Dashboard principal
├── Spotify_Fetch.py    # Script para descargar las canciones
├── dataset.csv         # Datos de Spotify
├── .env                # Credenciales Spotify (si aplicable)
└── README.md
```

---

# 🔮 Mejoras futuras

* Comparación entre múltiples playlists
* Análisis por género o artista
* Clustering de canciones por atributos
* Exportación de reportes interactivos
* Sistema de recomendaciones de canciones

---

# 👨‍💻 Autor

Proyecto desarrollado por Mario Gracia
Ideal para mostrar habilidades en **Python, Data Visualization y Dashboards interactivos**.

Si te gusta el proyecto, ⭐ dale una estrella en GitHub.

