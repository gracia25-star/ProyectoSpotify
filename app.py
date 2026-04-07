# app.py  –  Spotify Dashboard – Versión Premium con Plotly + Animaciones
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spotify Dashboard",
    page_icon="🎵",
    layout="wide",
)

# ─── CSS ANIMADO ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: #050505; }
.block-container { padding: 1.5rem 2rem 3rem 2rem; background: #050505; }
section[data-testid="stSidebar"] { background: #0a0a0a !important; border-right: 1px solid #1a1a1a; }

/* ── Animaciones ── */
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(29,185,84,0.15), 0 4px 24px rgba(0,0,0,0.5); }
    50%       { box-shadow: 0 0 40px rgba(29,185,84,0.35), 0 4px 24px rgba(0,0,0,0.5); }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.8); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes barFill {
    from { width: 0%; }
    to   { width: var(--w); }
}
@keyframes shimmer {
    0%   { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}
@keyframes spin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
@keyframes ripple {
    0%   { transform: scale(0); opacity: 1; }
    100% { transform: scale(4); opacity: 0; }
}

/* ── Header Banner ── */
.hero {
    background: linear-gradient(270deg, #1DB954, #158a3e, #0d2b1a, #1a0533, #1DB954);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite, fadeSlideDown 0.7s ease both;
    border-radius: 24px;
    padding: 2.8rem 3rem;
    margin-bottom: 2.2rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(29,185,84,0.2) 0%, transparent 70%);
    border-radius: 50%;
    animation: pulseGlow 3s ease-in-out infinite;
}
.hero-title {
    font-size: 3rem; font-weight: 900; color: #fff;
    letter-spacing: -1.5px; line-height: 1;
    text-shadow: 0 2px 30px rgba(0,0,0,0.4);
}
.hero-sub {
    font-size: 1rem; color: rgba(255,255,255,0.7);
    margin-top: 0.5rem; font-weight: 400;
}
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 50px;
    padding: 0.25rem 0.9rem; font-size: 0.75rem; color: #fff;
    font-weight: 600; letter-spacing: 0.5px; margin-top: 1rem;
    backdrop-filter: blur(8px);
}

/* ── KPI Cards ── */
.kpi-wrap { animation: fadeSlideUp 0.6s ease both; }
.kpi-wrap:nth-child(1) { animation-delay: 0.05s; }
.kpi-wrap:nth-child(2) { animation-delay: 0.12s; }
.kpi-wrap:nth-child(3) { animation-delay: 0.19s; }
.kpi-wrap:nth-child(4) { animation-delay: 0.26s; }

.kpi-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 20px;
    padding: 1.5rem 1.6rem 1.3rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.25s cubic-bezier(.34,1.56,.64,1), border-color 0.25s ease;
    cursor: default;
    margin-bottom: 1rem;
}
.kpi-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: var(--c);
    box-shadow: 0 16px 40px rgba(0,0,0,0.6), 0 0 0 1px var(--c);
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--c), transparent);
}
.kpi-glow {
    position: absolute; top: -30px; right: -30px;
    width: 120px; height: 120px;
    background: radial-gradient(circle, var(--c), transparent 70%);
    opacity: 0.12; border-radius: 50%;
    transition: opacity 0.3s;
}
.kpi-card:hover .kpi-glow { opacity: 0.25; }
.kpi-emoji { font-size: 1.6rem; margin-bottom: 0.7rem; }
.kpi-label {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 1.5px;
    color: #555; font-weight: 700; margin-bottom: 0.3rem;
}
.kpi-value {
    font-size: 2rem; font-weight: 900; color: #fff; line-height: 1;
    animation: countUp 0.5s cubic-bezier(.34,1.56,.64,1) both;
}
.kpi-value.small { font-size: 1.1rem; line-height: 1.35; }
.kpi-unit { font-size: 0.9rem; font-weight: 400; color: #666; }
.kpi-sub { font-size: 0.72rem; color: #444; margin-top: 0.45rem; }
.kpi-bar-bg {
    height: 3px; background: #1e1e2e; border-radius: 2px;
    margin-top: 0.9rem; overflow: hidden;
}
.kpi-bar {
    height: 100%; border-radius: 2px;
    background: linear-gradient(90deg, var(--c), rgba(255,255,255,0.3));
    animation: barFill 1s ease both 0.3s;
    width: var(--w);
}

/* ── Section headers ── */
.sec-header {
    font-size: 1.2rem; font-weight: 800; color: #fff;
    margin: 2rem 0 1rem; display: flex; align-items: center; gap: 0.5rem;
    animation: fadeSlideDown 0.5s ease both;
}
.sec-header::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, #2a2a3a, transparent);
    margin-left: 0.8rem;
}

/* ── Filter Pill Tags ── */
.pill {
    display: inline-block; background: #1DB95420; color: #1DB954;
    border: 1px solid #1DB95440; border-radius: 50px;
    padding: 0.2rem 0.75rem; font-size: 0.75rem; font-weight: 600;
    margin: 0.15rem;
}

/* ── Song ranking list ── */
.song-row {
    display: flex; align-items: center; gap: 0.8rem;
    padding: 0.65rem 1rem; border-radius: 12px; margin-bottom: 0.4rem;
    background: #111118; border: 1px solid #1e1e2e;
    transition: background 0.2s, border-color 0.2s, transform 0.2s;
    animation: fadeSlideUp 0.4s ease both;
}
.song-row:hover { background: #1a1a28; border-color: #333; transform: translateX(4px); }
.song-rank { font-size: 1rem; font-weight: 800; color: #333; width: 24px; text-align: right; }
.song-rank.gold   { color: #eab308; }
.song-rank.silver { color: #9ca3af; }
.song-rank.bronze { color: #f97316; }
.song-info { flex: 1; min-width: 0; }
.song-name { font-size: 0.87rem; font-weight: 600; color: #e5e7eb; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.song-artist { font-size: 0.72rem; color: #555; margin-top: 1px; }
.song-pop-bar { flex: 0 0 80px; }
.pop-bg { height: 4px; background: #1e1e2e; border-radius: 2px; overflow: hidden; }
.pop-fill { height: 100%; background: linear-gradient(90deg, #1DB954, #4ade80); border-radius: 2px; }
.song-pop-num { font-size: 0.72rem; color: #666; text-align: right; margin-top: 2px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 4px; }

/* ── Expander filtros ── */
[data-testid="stExpander"] {
    background: #111118 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 16px !important;
}
[data-testid="stExpander"] summary {
    color: #9ca3af !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}
[data-testid="stExpander"] summary:hover { color: #1DB954 !important; }

/* ── Plotly dark bg ── */
.js-plotly-plot .plotly .modebar { background: transparent !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── CARGA DE DATOS ───────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    for fname in ["dataset.csv", "playlist.csv"]:
        try:
            return pd.read_csv(fname)
        except FileNotFoundError:
            continue
    st.error("❌ No se encontró 'dataset.csv' ni 'playlist.csv'. Ejecuta primero Spotify_fetch1.py.")
    st.stop()

df_raw = load_data()

# Convertir duration_ms a minutos
if 'duration_ms' in df_raw.columns:
    df_raw['duration_min'] = (df_raw['duration_ms'] / 60000).round(2)


# ─── FILTROS (inline, sin sidebar) ──────────────────────────────────────────
pop_min, pop_max = int(df_raw['popularity'].min()), int(df_raw['popularity'].max())
all_artists = sorted(df_raw['artist'].unique())
all_albums  = sorted(df_raw['album'].unique()) if 'album' in df_raw.columns else []

with st.expander("🎛️  Filtros  —  haz clic para mostrar/ocultar", expanded=False):
    fc1, fc2, fc3 = st.columns([2, 3, 3])
    with fc1:
        pop_range = st.slider("🔥 Popularidad", pop_min, pop_max, (pop_min, pop_max))
    with fc2:
        selected_artists = st.multiselect("🎤 Artistas", all_artists, placeholder="Todos los artistas")
    with fc3:
        selected_albums = st.multiselect("📀 Álbumes", all_albums, placeholder="Todos los álbumes")


# ─── APLICAR FILTROS ──────────────────────────────────────────────────────────
df = df_raw.copy()
df = df[(df['popularity'] >= pop_range[0]) & (df['popularity'] <= pop_range[1])]
if selected_artists:
    df = df[df['artist'].isin(selected_artists)]
if selected_albums and 'album' in df.columns:
    df = df[df['album'].isin(selected_albums)]

if df.empty:
    st.warning("🔍 No hay canciones con los filtros aplicados.")
    st.stop()


# ─── MÉTRICAS ─────────────────────────────────────────────────────────────────
total_songs     = len(df)
total_artists   = df['artist'].nunique()
total_albums    = df['album'].nunique() if 'album' in df.columns else 0
avg_pop         = round(df['popularity'].mean(), 1)
max_pop         = int(df['popularity'].max())
avg_dur_min     = round(df['duration_min'].mean(), 2) if 'duration_min' in df.columns else 0
total_hours     = round(df['duration_min'].sum() / 60, 1) if 'duration_min' in df.columns else 0
pct_popular     = round((df[df['popularity'] >= 70].shape[0] / total_songs) * 100, 1)
top_song        = df.loc[df['popularity'].idxmax(), 'track_name'] if 'track_name' in df.columns else "N/A"
top_artist_name = df['artist'].value_counts().idxmax()
top_artist_cnt  = df['artist'].value_counts().max()
rarest_album    = df['album'].value_counts()[-1:].index[0] if 'album' in df.columns and total_albums > 0 else "N/A"
pop_std         = round(df['popularity'].std(), 1)


# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-title">🎵 Proyecto Spotify</div>
    <div class="hero-sub">Análisis interactivo de tu playlist de música</div>
    <div class="hero-badge">✦ {total_songs} canciones · {total_artists} artistas · {total_albums} álbumes</div>
</div>
""", unsafe_allow_html=True)

# Filtros activos
if selected_artists or selected_albums or pop_range != (pop_min, pop_max):
    pills = ""
    if pop_range != (pop_min, pop_max):
        pills += f'<span class="pill">🔥 Pop {pop_range[0]}-{pop_range[1]}</span>'
    for a in selected_artists:
        pills += f'<span class="pill">🎤 {a}</span>'
    for al in selected_albums:
        pills += f'<span class="pill">📀 {al}</span>'
    st.markdown(f'<div style="margin-bottom:1rem">{pills}</div>', unsafe_allow_html=True)


# ─── KPIs FILA 1 ──────────────────────────────────────────────────────────────
st.markdown('<div class="sec-header">📊 Indicadores Clave</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

def kpi(col, emoji, label, value, unit="", sub="", color="#1DB954", bar_pct=0):
    bar_w = f"{min(bar_pct, 100):.0f}%"
    bar_html = f"""<div class="kpi-bar-bg"><div class="kpi-bar" style="--w:{bar_w};--c:{color}"></div></div>""" if bar_pct else ""
    small_cls = "small" if len(str(value)) > 12 else ""
    with col:
        st.markdown(f"""
        <div class="kpi-wrap">
          <div class="kpi-card" style="--c:{color}">
            <div class="kpi-glow"></div>
            <div class="kpi-emoji">{emoji}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value {small_cls}">{value}<span class="kpi-unit">{unit}</span></div>
            <div class="kpi-sub">{sub}</div>
            {bar_html}
          </div>
        </div>""", unsafe_allow_html=True)

kpi(c1, "🎵", "Total Canciones",    total_songs,      sub=f"{total_albums} álbumes distintos",       color="#1DB954", bar_pct=(total_songs/max(len(df_raw),1))*100)
kpi(c2, "🎤", "Artistas Únicos",    total_artists,    sub=f"Top: {top_artist_name[:20]}",            color="#4f8ef7", bar_pct=(total_artists/max(len(all_artists),1))*100)
kpi(c3, "🔥", "Popularidad Prom.",  avg_pop, unit=" pts", sub=f"Máxima: {max_pop} · Desv: {pop_std}", color="#f97316", bar_pct=avg_pop)
kpi(c4, "⏱️", "Duración Promedio",  avg_dur_min, unit=" min", sub=f"Total: {total_hours}h de música",  color="#a855f7", bar_pct=(avg_dur_min/10)*100)

c5, c6, c7, c8 = st.columns(4)
top_name_short = top_song[:25] + "…" if len(top_song) > 25 else top_song
kpi(c5, "⭐", "Canción Más Popular", top_name_short, sub=f"Score: {max_pop} / 100",                   color="#ec4899")
kpi(c6, "🏆", "Artista Dominante",   top_artist_name[:20] + ("…" if len(top_artist_name)>20 else ""),
    sub=f"{top_artist_cnt} canciones en la lista",                                                     color="#14b8a6")
kpi(c7, "🚀", "Canciones Virales",   f"{pct_popular}%", sub="Popularidad ≥ 70",                       color="#eab308", bar_pct=pct_popular)
kpi(c8, "📀", "Álbumes Distintos",   total_albums,   sub=f"Promedio {total_songs//max(total_albums,1)} canciones/álbum", color="#ef4444", bar_pct=(total_albums/max(len(all_albums),1))*100)


# ─── GRÁFICOS ─────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#0d0d12",
    plot_bgcolor="#0d0d12",
    font=dict(family="Inter", color="#9ca3af", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    hoverlabel=dict(bgcolor="#1a1a2e", font_color="white", font_size=13, bordercolor="#333"),
    xaxis=dict(gridcolor="#1a1a2e", zeroline=False),
    yaxis=dict(gridcolor="#1a1a2e", zeroline=False),
)

# ─── Fila de gráficos – Top canciones + Donut Artistas ────────────────────────
st.markdown('<div class="sec-header">🎯 Top Canciones & Artistas</div>', unsafe_allow_html=True)
col_l, col_r = st.columns([3, 2], gap="medium")

with col_l:
    top10 = df.sort_values('popularity', ascending=False).head(10).copy()
    top10['label'] = top10['track_name'].str[:32]

    palette = px.colors.sequential.Plasma_r[:10]
    fig = go.Figure(go.Bar(
        x=top10['popularity'],
        y=top10['label'],
        orientation='h',
        marker=dict(
            color=top10['popularity'],
            colorscale='Plasma',
            line=dict(width=0),
        ),
        text=top10['popularity'],
        textposition='outside',
        textfont=dict(size=11, color='#9ca3af'),
        customdata=top10[['artist', 'album']],
        hovertemplate="<b>%{y}</b><br>👤 %{customdata[0]}<br>💿 %{customdata[1]}<br>🔥 %{x} pts<extra></extra>",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="🏅 Top 10 más populares",
                      title_font=dict(size=14, color="#e5e7eb"),
                      xaxis_range=[0, 110])
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=11))
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col_r:
    artist_counts = df['artist'].value_counts().head(9)
    fig2 = go.Figure(go.Pie(
        labels=artist_counts.index,
        values=artist_counts.values,
        hole=0.62,
        marker=dict(
            colors=px.colors.qualitative.Vivid,
            line=dict(color='#050505', width=3)
        ),
        textinfo='none',
        hovertemplate="<b>%{label}</b><br>%{value} canciones · %{percent}<extra></extra>",
    ))
    fig2.add_annotation(
        text=f"<b>{total_artists}</b><br><span style='font-size:11px'>artistas</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color='white'),
    )
    fig2.update_layout(**PLOTLY_LAYOUT, title="🎤 Distribución de artistas",
                       title_font=dict(size=14, color="#e5e7eb"),
                       legend=dict(font=dict(size=10), bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})


# ─── Distribución de popularidad ──────────────────────────────────────────────
st.markdown('<div class="sec-header">📈 Distribución de Popularidad</div>', unsafe_allow_html=True)

fig3 = go.Figure()
fig3.add_trace(go.Histogram(
    x=df['popularity'], nbinsx=25,
    marker=dict(
        color='#1DB954',
        line=dict(width=0),
    ),
    name="Canciones",
    hovertemplate="Popularidad %{x}<br>%{y} canciones<extra></extra>",
    opacity=0.85,
))
fig3.add_vline(x=avg_pop, line_dash="dash", line_color="#f97316", line_width=2,
               annotation_text=f"Media {avg_pop}", annotation_font_color="#f97316")
fig3.add_vline(x=70, line_dash="dot", line_color="#ef4444", line_width=1.5,
               annotation_text="Viral", annotation_font_color="#ef4444")
fig3.add_vrect(x0=70, x1=df['popularity'].max()+1,
               fillcolor="rgba(239,68,68,0.05)", line_width=0,
               annotation_text="Zona viral", annotation_position="top left",
               annotation_font_color="#ef4444", annotation_font_size=11)
fig3.update_layout(**PLOTLY_LAYOUT, height=280,
                   title="Histograma de popularidad", title_font=dict(size=14, color="#e5e7eb"))
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})


# ─── Fila – Scatter + Top Artistas barras ────────────────────────────────────
st.markdown('<div class="sec-header">🔬 Análisis Profundo</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2, gap="medium")

with col3:
    fig4 = px.scatter(
        df, x='duration_min', y='popularity',
        color='popularity',
        color_continuous_scale='Teal',
        hover_name='track_name' if 'track_name' in df.columns else None,
        hover_data={'artist': True, 'album': True, 'duration_min': ':.2f', 'popularity': True},
        labels={'duration_min': 'Duración (min)', 'popularity': 'Popularidad'},
        title="⏱️ Duración vs Popularidad",
        size_max=10,
    )
    fig4.update_traces(marker=dict(size=7, opacity=0.8, line=dict(width=0)))
    fig4.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                       title_font=dict(size=14, color="#e5e7eb"))
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

with col4:
    top_artists_df = df.groupby('artist').agg(
        canciones=('track_name', 'count'),
        pop_promedio=('popularity', 'mean')
    ).sort_values('canciones', ascending=False).head(10).reset_index()

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=top_artists_df['artist'],
        y=top_artists_df['canciones'],
        name='Canciones',
        marker=dict(
            color=top_artists_df['pop_promedio'],
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title="Pop. prom.", tickfont=dict(size=9), thickness=10),
        ),
        hovertemplate="<b>%{x}</b><br>🎵 %{y} canciones<br>🔥 Pop: %{marker.color:.1f}<extra></extra>",
    ))
    fig5.update_layout(**PLOTLY_LAYOUT, title="🎤 Artistas por n.º de canciones",
                       title_font=dict(size=14, color="#e5e7eb"),
                       xaxis_tickangle=-35)
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})





# ─── TOP 10 lista visual ──────────────────────────────────────────────────────
st.markdown('<div class="sec-header">🎖️ Ranking Visual</div>', unsafe_allow_html=True)
cols_rank = st.columns(2)
top15 = df.sort_values('popularity', ascending=False).head(14)

for idx, (_, row) in enumerate(top15.iterrows()):
    col_idx = idx % 2
    rank = idx + 1
    rank_cls = "gold" if rank == 1 else "silver" if rank == 2 else "bronze" if rank == 3 else ""
    name = row.get('track_name', 'N/A')[:40]
    artist = row.get('artist', 'N/A')[:30]
    pop = int(row['popularity'])
    pop_pct = f"{pop}%"
    delay = f"{0.05 * idx:.2f}s"
    with cols_rank[col_idx]:
        st.markdown(f"""
        <div class="song-row" style="animation-delay:{delay}">
            <div class="song-rank {rank_cls}">#{rank}</div>
            <div class="song-info">
                <div class="song-name">{name}</div>
                <div class="song-artist">{artist}</div>
            </div>
            <div class="song-pop-bar">
                <div class="pop-bg"><div class="pop-fill" style="width:{pop_pct}"></div></div>
                <div class="song-pop-num">{pop} pts</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ─── TABLA INTERACTIVA ────────────────────────────────────────────────────────
st.markdown('<div class="sec-header">🗂️ Explorador de Canciones</div>', unsafe_allow_html=True)

search = st.text_input("🔍 Buscar canción o artista...", placeholder="Escribe para filtrar...")
df_show = df.copy()
if search:
    mask = (
        df_show['track_name'].str.contains(search, case=False, na=False) |
        df_show['artist'].str.contains(search, case=False, na=False)
    )
    df_show = df_show[mask]

display_cols = [c for c in ['track_name', 'artist', 'album', 'popularity', 'duration_min'] if c in df_show.columns]
df_display = df_show[display_cols].copy()

st.dataframe(
    df_display,
    use_container_width=True,
    height=420,
    column_config={
        "track_name":   st.column_config.TextColumn("🎵 Canción"),
        "artist":       st.column_config.TextColumn("🎤 Artista"),
        "album":        st.column_config.TextColumn("💿 Álbum"),
        "popularity":   st.column_config.ProgressColumn("🔥 Popularidad", min_value=0, max_value=100, format="%d"),
        "duration_min": st.column_config.NumberColumn("⏱️ Min", format="%.2f"),
    },
    hide_index=True,
)

st.markdown(f"<p style='color:#333;font-size:0.72rem;text-align:right'>Mostrando {len(df_show)} de {total_songs} canciones</p>", unsafe_allow_html=True)