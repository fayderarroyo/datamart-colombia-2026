import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataMart Colombia · Planeación Estratégica 2026",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────
# COORDENADAS DE CIUDADES (lat/lon para el mapa)
# ─────────────────────────────────────────────────────────────────────
COORDENADAS = {
    "Bogotá D.C.":        (4.7110, -74.0721),
    "Medellín A.M.":      (6.2442, -75.5812),
    "Cali A.M.":          (3.4516, -76.5320),
    "Barranquilla A.M.":  (10.9685, -74.7813),
    "Bucaramanga A.M.":   (7.1193, -73.1227),
    "Manizales A.M.":     (5.0703, -75.5138),
    "Pasto":              (1.2136, -77.2811),
    "Pereira A.M.":       (4.8087, -75.6906),
    "Cúcuta A.M.":        (7.8939, -72.5078),
    "Ibagué":             (4.4389, -75.2322),
    "Cartagena":          (10.3910, -75.4794),
    "Villavicencio":      (4.1420, -73.6266),
    "Soacha":             (4.5793, -74.2159),
    "Valledupar":         (10.4631, -73.2532),
    "Montería":           (8.7479, -75.8814),
    "Tunja":              (5.5353, -73.3678),
    "Florencia":          (1.6144, -75.6062),
    "Popayán":            (2.4448, -76.6147),
    "Quibdó":             (5.6919, -76.6583),
    "Neiva":              (2.9273, -75.2819),
    "Riohacha":           (11.5444, -72.9072),
    "Armenia":            (4.5339, -75.6811),
    "Sincelejo":          (9.3047, -75.3978),
    "Buenaventura":       (3.8801, -77.0311),
    "Barrancabermeja":    (7.0650, -73.8547),
    "Tumaco":             (1.7993, -78.7624),
    "Arauca":             (7.0897, -70.7619),
    "Yopal":              (5.3378, -72.3959),
    "Rionegro (Antioquia)": (6.1546, -75.3741),
    "Mocoa":              (1.1523, -76.6492),
    "San Andrés":         (12.5847, -81.7006),
    "Leticia":            (-4.2153, -69.9406),
    "Inírida":            (3.8653, -67.9239),
    "San José del Guaviare": (2.5688, -72.6411),
    "Mitú":               (1.2535, -70.2339),
    "Puerto Carreño":     (6.1892, -67.4849),
}

# ─────────────────────────────────────────────────────────────────────
# CSS PREMIUM
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #070b14 0%, #0d1526 50%, #091020 100%);
    min-height: 100vh;
}
/* Header */
.hero-header {
    background: linear-gradient(135deg, rgba(37,99,235,0.15) 0%, rgba(139,92,246,0.15) 100%);
    border: 1px solid rgba(99,179,237,0.2);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 28px 40px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 8px 32px rgba(37,99,235,0.1), inset 0 1px 0 rgba(255,255,255,0.05);
}
.hero-title {
    font-size: 1.85rem;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    margin: 0;
}
.hero-sub {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 4px;
    font-weight: 400;
}
/* KPI cards */
.kpi-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99,179,237,0.15);
    backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent-color, linear-gradient(90deg, #2563eb, #7c3aed));
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 6px 0 4px;
    background: var(--value-gradient, linear-gradient(90deg, #60a5fa, #a78bfa));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.kpi-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #64748b;
    font-weight: 600;
}
.kpi-delta {
    font-size: 0.8rem;
    margin-top: 6px;
    color: #34d399;
}
/* Section headers */
.section-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #475569;
    font-weight: 700;
    margin: 28px 0 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(71,85,105,0.3);
}
/* Badge */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.badge-blue { background: rgba(37,99,235,0.2); color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }
.badge-green { background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.badge-orange { background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-red { background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
/* Insight box */
.insight-box {
    background: rgba(37,99,235,0.08);
    border: 1px solid rgba(96,165,250,0.2);
    border-left: 4px solid #2563eb;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.6;
}
.insight-box strong { color: #60a5fa; }
/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(5, 8, 16, 0.95) !important;
    border-right: 1px solid rgba(99,179,237,0.1) !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
/* Metric override */
div[data-testid="metric-container"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
div[data-testid="stMetricLabel"] p { color: #64748b !important; }
div[data-testid="stMetricValue"] { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# SUPABASE CONNECTION
# ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def init_connection() -> Client:
    load_dotenv()
    url = os.environ.get("SUPABASE_URL", "https://bqouxvxmfvlnaenmbnmn.supabase.co")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)

supabase = init_connection()

# ─────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def load_all_data():
    # 1. Vista cobertura (pre-agregada en Supabase)
    resp_cob = supabase.table('vw_cobertura_intermedia').select("*").execute()
    df_cob = pd.DataFrame(resp_cob.data)

    # 2. Datos de ciudad (36 filas)
    resp_dc = supabase.table('datos_ciudad').select("*").execute()
    df_dc = pd.DataFrame(resp_dc.data)

    # 3. Ciudades puente (36 filas)
    resp_cp = supabase.table('ciudades_puente').select("*").execute()
    df_cp = pd.DataFrame(resp_cp.data)

    return df_cob, df_dc, df_cp

with st.spinner("Cargando datos desde Supabase..."):
    df_cob, df_dc, df_cp = load_all_data()

if df_cob.empty or df_dc.empty or df_cp.empty:
    st.error("⚠️ No hay datos disponibles. Verifica la conexión con Supabase y que la vista `vw_cobertura_intermedia` esté creada.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────
# DATA PROCESSING
# ─────────────────────────────────────────────────────────────────────
df_cob['pct_4g'] = df_cob['filas_4g'] / df_cob['total_filas']

# Merge principal
df_full = (df_cob
    .merge(df_cp[['nombre_geih','clasificacion','es_intermedia_estricta','poblacion_2024','cumple_100k_500k']], 
           left_on='ciudad', right_on='nombre_geih', how='left')
    .merge(df_dc[['ciudad','tasa_de_desocupacion_td','tasa_de_ocupacion_to',
                  'tasa_global_de_participacion_tgp','pct_poblacion_en_edad_de_trabajar',
                  'poblacion_ocupada','poblacion_total','fuerza_de_trabajo_potencial']],
           on='ciudad', how='left')
)

# Calcular métricas avanzadas
max_des = df_dc['tasa_de_desocupacion_td'].max()
df_full['IPD'] = df_full['pct_4g'] * (max_des - df_full['tasa_de_desocupacion_td']) * 10
df_full['score_eficiencia'] = (1 / df_full['tasa_de_desocupacion_td']) * 100
df_full['indice_dinamismo_digital'] = df_full['tasa_de_ocupacion_to'] * df_full['pct_4g']
df_full['mercado_digital_potencial'] = df_full['poblacion_ocupada'] * df_full['pct_4g']  # miles
df_full['tasa_sub_empleo_inv'] = 100 - df_full.get('tasa_de_subocupacion_ts', 0)

# Añadir coordenadas
df_full['lat'] = df_full['ciudad'].map(lambda c: COORDENADAS.get(c, (None,None))[0])
df_full['lon'] = df_full['ciudad'].map(lambda c: COORDENADAS.get(c, (None,None))[1])

# Forzar el foco exclusivo en ciudades intermedias (es_intermedia_estricta == 'SÍ')
df_full = df_full[df_full['clasificacion'] == 'Intermedia'].copy()

# ─────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size: 1.6rem; font-weight: 900; background: linear-gradient(90deg,#60a5fa,#a78bfa);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            DataMart
        </div>
        <div style='font-size: 0.7rem; color: #475569; letter-spacing: 2px; text-transform:uppercase;'>
            Colombia · Analytics
        </div>
    </div>
    <hr style='border-color: rgba(99,179,237,0.1); margin: 10px 0 20px;'>
    """, unsafe_allow_html=True)

    st.markdown("**🗓 Período de Análisis**")
    anos_disponibles = sorted(df_full['ano'].dropna().unique().astype(int).tolist())
    ano_rango = st.select_slider(
        "Años",
        options=anos_disponibles,
        value=(min(anos_disponibles), max(anos_disponibles)),
        label_visibility="collapsed"
    )

    st.markdown("<br>**📈 Métrica Principal del Mapa**", unsafe_allow_html=True)
    metrica_mapa = st.selectbox(
        "Métrica",
        options=["IPD (Índice Potencial Digital)", "% Cobertura 4G LTE", 
                 "Tasa de Ocupación", "Mercado Digital Potencial"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: rgba(99,179,237,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#334155; line-height:1.8; margin-bottom: 20px;'>
        📊 Fuentes: MinTIC · DANE GEIH<br>
        📅 Cobertura: 2015–2023<br>
        🏙 Ciudades Intermedias Estratégicas
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.85rem; font-weight:600; color:#e2e8f0; margin-bottom:10px;'>🎓 Recursos Académicos (Evaluación)</div>", unsafe_allow_html=True)
    
    try:
        with open("visualizacion 1/visualizacion 1.pbix", "rb") as f:
            st.download_button(label="📊 Descargar PBIX Original", data=f.read(), file_name="Visualizacion_1.pbix", mime="application/octet-stream", use_container_width=True)
    except FileNotFoundError:
        pass

    try:
        with open("Ciudades-intermedias-la-nueva-frontera-del-marketing-digital-en-Colombia.pdf", "rb") as f:
            st.download_button(label="📑 Descargar PDF (Presentación)", data=f.read(), file_name="Ciudades_Intermedias_Presentacion.pdf", mime="application/pdf", use_container_width=True)
    except FileNotFoundError:
        pass

    with st.expander("🛠️ Stack Tecnológico & Documentación"):
        st.markdown("""
        <div style='font-size:0.75rem; color:#cbd5e1; line-height:1.6; margin-bottom: 10px;'>
        <b>Frontend UI:</b> Streamlit, CSS Custom (Glassmorphism), HTML5.<br>
        <b>Data Viz:</b> Plotly Graph Objects & Express (Scatter Mapbox).<br>
        <b>Data & Backend:</b> Python 3, Pandas, NumPy.<br>
        <b>Arquitectura:</b> Pantalla de alta densidad (100% width), control dinámico de componentes y renderizado interactivo sin scroll forzado.
        </div>
        """, unsafe_allow_html=True)
        
        try:
            with open("README.txt", "r", encoding="utf-8") as f:
                readme_content = f.read()
            st.download_button(label="📄 Descargar README.txt", data=readme_content, file_name="README.txt", mime="text/plain", use_container_width=True)
            with st.expander("👀 Leer README completo"):
                st.code(readme_content, language="markdown")
        except FileNotFoundError:
            pass

# ─────────────────────────────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────────────────────────────
df_filtered = df_full[
    (df_full['ano'] >= ano_rango[0]) &
    (df_full['ano'] <= ano_rango[1])
].copy()

# Dataset del año más reciente para ciudad
anio_ref = df_filtered['ano'].max() if not df_filtered.empty else max(anos_disponibles)
df_ciudad_ref = df_filtered[df_filtered['ano'] == anio_ref].copy()
df_ciudad_ref = df_ciudad_ref.drop_duplicates(subset='ciudad')

# ─────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div style="font-size: 2.5rem;">📡</div>
    <div>
        <p class="hero-title">PLANEACIÓN ESTRATÉGICA · DATAMART COLOMBIA</p>
        <p class="hero-sub">Dashboard de inteligencia geográfica para redistribución de pauta digital — Clase de Visualización de Datos</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# KPIs ROW
# ─────────────────────────────────────────────────────────────────────
# Calcular agregados
total_filas_agg = df_filtered['total_filas'].sum()
total_4g_agg   = df_filtered['filas_4g'].sum()
pct_cob_global = (total_4g_agg / total_filas_agg * 100) if total_filas_agg > 0 else 0

ipd_promedio        = df_ciudad_ref['IPD'].mean() if not df_ciudad_ref.empty else 0
score_ef_promedio   = df_ciudad_ref['score_eficiencia'].mean() if not df_ciudad_ref.empty else 0
din_digital_prom    = df_ciudad_ref['indice_dinamismo_digital'].mean() if not df_ciudad_ref.empty else 0
top_ipd_ciudad      = df_ciudad_ref.loc[df_ciudad_ref['IPD'].idxmax(), 'ciudad'] if not df_ciudad_ref.empty else "—"

# Crecimiento 4G (primer vs último año)
df_early = df_full[df_full['ano'] == min(anos_disponibles)][['ciudad','pct_4g']].rename(columns={'pct_4g':'pct_early'})
df_late  = df_full[df_full['ano'] == max(anos_disponibles)][['ciudad','pct_4g']].rename(columns={'pct_4g':'pct_late'})
df_growth = pd.merge(df_early, df_late, on='ciudad')
growth_promedio = (df_growth['pct_late'] - df_growth['pct_early']).mean() * 100

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="kpi-card" style="--accent-color: linear-gradient(90deg,#2563eb,#3b82f6);">
        <div class="kpi-label">% Cobertura 4G LTE</div>
        <div class="kpi-value" style="--value-gradient: linear-gradient(90deg,#60a5fa,#93c5fd);">{pct_cob_global:.1f}%</div>
        <div class="kpi-delta">↑ Año {int(anio_ref)}</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card" style="--accent-color: linear-gradient(90deg,#7c3aed,#8b5cf6);">
        <div class="kpi-label" title="Métrica compuesta que evalúa el atractivo comercial digital de una ciudad, integrando la cobertura 4G con la capacidad económica poblacional.">Índice Potencial Digital <span style="cursor:help; opacity:0.9; font-size:1.1em; color:#93c5fd; margin-left: 4px;">ⓘ</span></div>
        <div class="kpi-value" style="--value-gradient: linear-gradient(90deg,#a78bfa,#c4b5fd);">{ipd_promedio:.2f}</div>
        <div class="kpi-delta">★ Top: {top_ipd_ciudad.split(' ')[0]}</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card" style="--accent-color: linear-gradient(90deg,#059669,#10b981);">
        <div class="kpi-label" title="Indicador de retorno de inversión potencial. Un mayor score indica que cuesta menos impactar a un usuario con capacidad adquisitiva real.">Score Eficiencia Costo <span style="cursor:help; opacity:0.9; font-size:1.1em; color:#6ee7b7; margin-left: 4px;">ⓘ</span></div>
        <div class="kpi-value" style="--value-gradient: linear-gradient(90deg,#34d399,#6ee7b7);">{score_ef_promedio:.2f}</div>
        <div class="kpi-delta">1 / Tasa Desempleo × 100</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi-card" style="--accent-color: linear-gradient(90deg,#d97706,#f59e0b);">
        <div class="kpi-label" title="Mide qué tan activo es el mercado combinando la penetración de internet móvil con la ocupación laboral real de la ciudad.">Dinamismo Digital <span style="cursor:help; opacity:0.9; font-size:1.1em; color:#fde68a; margin-left: 4px;">ⓘ</span></div>
        <div class="kpi-value" style="--value-gradient: linear-gradient(90deg,#fbbf24,#fde68a);">{din_digital_prom:.1f}%</div>
        <div class="kpi-delta">Ocupación × Cobertura 4G</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""
    <div class="kpi-card" style="--accent-color: linear-gradient(90deg,#dc2626,#ef4444);">
        <div class="kpi-label">Crecimiento 4G {min(anos_disponibles)}-{max(anos_disponibles)}</div>
        <div class="kpi-value" style="--value-gradient: linear-gradient(90deg,#f87171,#fca5a5);">+{growth_promedio:.1f}pp</div>
        <div class="kpi-delta">Penetración adicional</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────────────────────────────
# MAPA INTERACTIVO + TENDENCIA TEMPORAL
# ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🗺 INTELIGENCIA GEOGRÁFICA · MAPA INTERACTIVO DE COBERTURA</div>', unsafe_allow_html=True)

df_map = df_ciudad_ref.dropna(subset=['lat', 'lon']).copy()

# Seleccionar métrica del mapa
metrica_col_map = {
    "IPD (Índice Potencial Digital)": "IPD",
    "% Cobertura 4G LTE": "pct_4g",
    "Tasa de Ocupación": "tasa_de_ocupacion_to",
    "Mercado Digital Potencial": "mercado_digital_potencial",
}[metrica_mapa]

metrica_label = {
    "IPD": "IPD",
    "pct_4g": "% Cobertura 4G",
    "tasa_de_ocupacion_to": "Tasa Ocupación (%)",
    "mercado_digital_potencial": "Mercado Digital (miles)",
}[metrica_col_map]

# ─────────────────────────────────────────────────────────────────────
# ESTRUCTURA DE PESTAÑAS (ELIMINAR SCROLL VERTICAL)
# ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🗺️ Inteligencia Geográfica", "📊 Rankings Estratégicos"])

# ─────────────────────────────────────────────────────────────────────
# PESTAÑA 1: INTELIGENCIA GEOGRÁFICA
# ─────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">🗺️ INTELIGENCIA GEOGRÁFICA · ANÁLISIS ESPACIAL IPD</div>', unsafe_allow_html=True)
    col_map_tab1, col_sc_tab1 = st.columns(2)

    with col_map_tab1:
        df_map = df_ciudad_ref.dropna(subset=['lat', 'lon']).copy()

        # Mapa de burbujas nativo (go.Scattergeo) forzado al modo oscuro local
        fig_map = go.Figure()
        
        # Escalar el tamaño de los marcadores dinámicamente según la métrica seleccionada
        if metrica_col_map == 'IPD':
            marker_sizes = df_map[metrica_col_map] / 5.0
        elif metrica_col_map == 'mercado_digital_potencial':
            marker_sizes = df_map[metrica_col_map] / 15.0
        else:
            marker_sizes = df_map[metrica_col_map] / 3.0

        fig_map.add_trace(go.Scattergeo(
            lat=df_map['lat'],
            lon=df_map['lon'],
            mode='markers',
            marker=dict(
                size=marker_sizes,
                color=df_map[metrica_col_map],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title=dict(text=metrica_label, font=dict(size=10, color='#94a3b8')),
                    thicknessmode="pixels", thickness=12,
                    lenmode="fraction", len=0.6,
                    yanchor="middle", y=0.5,
                    tickfont=dict(size=8, color='#94a3b8')
                ),
                line=dict(width=0)
            ),
            hovertext=df_map['ciudad'],
            customdata=np.stack((
                df_map['IPD'],
                df_map['pct_4g'],
                df_map['tasa_de_desocupacion_td'],
                df_map['tasa_de_ocupacion_to'],
                df_map['poblacion_2024']
            ), axis=-1),
            hovertemplate=(
                "<b>%{hovertext}</b><br><br>"
                f"{metrica_label}: <b>%{{marker.color:.2f}}</b><br>"
                "IPD: %{customdata[0]:.2f}<br>"
                "Cobertura 4G LTE: %{customdata[1]:.1%}<br>"
                "Tasa de Desempleo: %{customdata[2]:.1f}%<br>"
                "Tasa de Ocupación: %{customdata[3]:.1f}%<br>"
                "Población: %{customdata[4]:,}<br>"
                "<extra></extra>"
            )
        ))

        fig_map.update_layout(
            geo=dict(
                scope='south america',
                showland=True,
                landcolor='rgb(15, 23, 42)',      # Color oscuro del contenedor para glassmorphism
                countrycolor='rgb(51, 65, 85)',   # Fronteras grises
                subunitcolor='rgb(51, 65, 85)',
                showlakes=False,
                center=dict(lat=4.5, lon=-74.2),
                projection_scale=6.0              # Escala óptima para enmarcar a Colombia
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=40, b=0),
            font=dict(family='Inter', color='#94a3b8'),
            height=600
        )
        st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"<p style='font-size:0.72rem; color:#475569; text-align:center;'>Mapa interactivo basado en <b style='color:#60a5fa;'>{{metrica_label}}</b></p>", unsafe_allow_html=True)

    with col_sc_tab1:
        # Bubble chart: Cobertura 4G vs Desempleo vs Tamaño mercado
        df_sc = df_ciudad_ref.dropna(subset=['tasa_de_desocupacion_td','pct_4g']).copy()
        df_sc['pct_4g_pct'] = df_sc['pct_4g'] * 100

        # Scatter plot interactivo con burbujas de tamaño armonizado a size_max=20
        fig_sc = px.scatter(
            df_sc,
            x='tasa_de_desocupacion_td',
            y='pct_4g_pct',
            size='poblacion_2024',
            color='IPD',
            text=df_sc['ciudad'].str.split(' ').str[0],
            size_max=20,
            color_continuous_scale='Viridis',
            height=530
        )

        # Cuadrantes basados en las medianas de las ciudades intermedias
        x_med = df_sc['tasa_de_desocupacion_td'].median()
        y_med = df_sc['pct_4g_pct'].median()
        fig_sc.add_hline(y=y_med, line_dash='dot', line_color='rgba(255,255,255,0.2)', line_width=1)
        fig_sc.add_vline(x=x_med, line_dash='dot', line_color='rgba(255,255,255,0.2)', line_width=1)

        # Anotación cuadrante ideal
        fig_sc.add_annotation(
            x=x_med - 1.0, y=y_med + 4,
            text="★ ZONA IDEAL (Alto IPD)",
            showarrow=False,
            font=dict(color='#34d399', size=9, family='Inter', weight='bold'),
            xanchor='right'
        )

        fig_sc.update_traces(
            textposition='top center',
            textfont=dict(size=8, color='rgba(203,213,225,0.8)'),
            hovertemplate=(
                "<b>%{hovertext}</b><br><br>"
                "Tasa Desempleo: <b>%{x:.1f}%</b><br>"
                "Cobertura 4G LTE: <b>%{y:.1f}%</b><br>"
                "IPD: %{customdata[0]:.2f}<br>"
                "Población: %{marker.size:,}<br>"
                "<extra></extra>"
            ),
            hovertext=df_sc['ciudad'],
            customdata=np.stack((df_sc['IPD'],), axis=-1)
        )

        fig_sc.update_layout(
            title=dict(text="Cuadrante de Decisión Estratégica", font=dict(size=16, color='#e2e8f0'), x=0.01),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(13,21,38,0.5)',
            font=dict(family='Inter', color='#94a3b8', size=10),
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(title="Tasa Desempleo (%)", showgrid=True, gridcolor='rgba(71,85,105,0.15)', color='#475569'),
            yaxis=dict(title="% Cobertura 4G LTE", showgrid=True, gridcolor='rgba(71,85,105,0.15)', color='#475569'),
            coloraxis_colorbar=dict(
                title=dict(text="IPD", font=dict(size=10, color='#94a3b8')),
                thicknessmode="pixels", thickness=12,
                lenmode="fraction", len=0.6,
                yanchor="middle", y=0.5,
                tickfont=dict(size=8, color='#94a3b8')
            )
        )
        st.plotly_chart(fig_sc, use_container_width=True, config={'displayModeBar': False})



    
        col_top1, col_top2 = st.columns(2)
        
        with col_top1:
            df_ipd = df_ciudad_ref.sort_values('IPD', ascending=False).head(10).copy()
            df_ipd = df_ipd.sort_values('IPD', ascending=True)
            df_ipd['ciudad_str'] = df_ipd['ciudad'].str.split(' ').str[0]
            fig_ipd = go.Figure(go.Bar(
                x=df_ipd['IPD'],
                y=df_ipd['ciudad_str'],
                orientation='h',
                marker=dict(color='#3b82f6', opacity=0.9),
                text=df_ipd['IPD'].apply(lambda v: f"{v:.1f}"),
                textposition='outside',
                textfont=dict(size=9, color='#94a3b8')
            ))
            fig_ipd.update_layout(
                title=dict(text="Top 10 Índice Potencial Digital", font=dict(size=15, color='#e2e8f0'), x=0.01),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(13,21,38,0.5)',
                font=dict(family='Inter', color='#94a3b8', size=10),
                height=350, margin=dict(l=20, r=20, t=40, b=20),
                xaxis=dict(showgrid=True, gridcolor='rgba(71,85,105,0.15)', color='#475569'),
                yaxis=dict(showgrid=False, color='#e2e8f0', title='')
            )
            st.plotly_chart(fig_ipd, use_container_width=True, config={'displayModeBar': False})

        with col_top2:
            df_ef = df_ciudad_ref.sort_values('score_eficiencia', ascending=False).head(10).copy()
            df_ef = df_ef.sort_values('score_eficiencia', ascending=True)
            df_ef['ciudad_str'] = df_ef['ciudad'].str.split(' ').str[0]
            fig_ef = go.Figure(go.Bar(
                x=df_ef['score_eficiencia'],
                y=df_ef['ciudad_str'],
                orientation='h',
                marker=dict(color='#8b5cf6', opacity=0.9),
                text=df_ef['score_eficiencia'].apply(lambda v: f"{v:.1f}"),
                textposition='outside',
                textfont=dict(size=9, color='#94a3b8')
            ))
            fig_ef.update_layout(
                title=dict(text="Top 10 Score Eficiencia Costo", font=dict(size=15, color='#e2e8f0'), x=0.01),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(13,21,38,0.5)',
                font=dict(family='Inter', color='#94a3b8', size=10),
                height=350, margin=dict(l=20, r=20, t=40, b=20),
                xaxis=dict(showgrid=True, gridcolor='rgba(71,85,105,0.15)', color='#475569'),
                yaxis=dict(showgrid=False, color='#e2e8f0', title='')
            )
            st.plotly_chart(fig_ef, use_container_width=True, config={'displayModeBar': False})

# ─────────────────────────────────────────────────────────────────────
# PESTAÑA 2: RANKINGS ESTRATÉGICOS
# ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">📊 RANKINGS ESTRATÉGICOS · ANÁLISIS DE ACELERACIÓN DIGITAL</div>', unsafe_allow_html=True)
    # Dos columnas simétricas abajo (50% / 50%) para los remanentes de aceleración
    col_acc1, col_acc2 = st.columns(2)

    with col_acc1:
        # Crecimiento 4G por ciudad 2015→2023
        df_early_f = df_full[df_full['ano']==min(anos_disponibles)][['ciudad','pct_4g','clasificacion']].rename(columns={'pct_4g':'pct_early'})
        df_late_f  = df_full[df_full['ano']==max(anos_disponibles)][['ciudad','pct_4g']].rename(columns={'pct_4g':'pct_late'})
        df_growth_f = pd.merge(df_early_f, df_late_f, on='ciudad').dropna()
        df_growth_f['crecimiento_pp'] = (df_growth_f['pct_late'] - df_growth_f['pct_early']) * 100
        df_growth_f = df_growth_f.sort_values('crecimiento_pp', ascending=True).tail(10)

        fig_growth = go.Figure(go.Bar(
            x=df_growth_f['crecimiento_pp'],
            y=df_growth_f['ciudad'].str.split(' ').str[0],
            orientation='h',
            marker=dict(
                color=df_growth_f['crecimiento_pp'],
                colorscale='Viridis',
                opacity=0.9,
                line=dict(width=0)
            ),
            text=df_growth_f['crecimiento_pp'].apply(lambda v: f"+{v:.1f}pp"),
            textposition='outside',
            textfont=dict(size=9, color='#94a3b8'),
        ))
        fig_growth.update_layout(
            title=dict(text=f"Crecimiento Cobertura 4G {min(anos_disponibles)}→{max(anos_disponibles)} (pp)", 
                       font=dict(size=15, color='#e2e8f0'), x=0.01),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(13,21,38,0.5)',
            font=dict(family='Inter', color='#94a3b8', size=10),
            height=350, 
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(71,85,105,0.15)', ticksuffix='pp', color='#475569'),
            yaxis=dict(showgrid=False, color='#e2e8f0', title=''),
        )
        st.plotly_chart(fig_growth, use_container_width=True, config={'displayModeBar': False})

    with col_acc2:
        # Índice de Dinamismo Digital (Ocupación × Cobertura 4G)
        df_din = df_ciudad_ref.sort_values('indice_dinamismo_digital', ascending=False).head(10)
        df_din_s = df_din.sort_values('indice_dinamismo_digital', ascending=True)

        fig_din = go.Figure()
        fig_din.add_trace(go.Bar(
            x=df_din_s['indice_dinamismo_digital'],
            y=df_din_s['ciudad'].str.split(' ').str[0],
            orientation='h',
            marker=dict(
                color=df_din_s['indice_dinamismo_digital'],
                colorscale='Cividis',
                opacity=0.85,
            ),
            name='Índice Dinamismo',
            text=df_din_s['indice_dinamismo_digital'].apply(lambda v: f"{v:.1f}%"),
            textposition='outside',
            textfont=dict(size=9, color='#94a3b8'),
        ))
        fig_din.update_layout(
            title=dict(text="Índice de Dinamismo Digital (Ocupación × Cobertura 4G)", 
                       font=dict(size=15, color='#e2e8f0'), x=0.01),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(13,21,38,0.5)',
            font=dict(family='Inter', color='#94a3b8', size=10),
            height=350, 
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(71,85,105,0.15)', ticksuffix='%', color='#475569'),
            yaxis=dict(showgrid=False, color='#e2e8f0', title=''),
        )
        st.plotly_chart(fig_din, use_container_width=True, config={'displayModeBar': False})

# ─────────────────────────────────────────────────────────────────────
# INSIGHT BOX — Conclusión estratégica (Exclusiva de Ciudades Intermedias)
# ─────────────────────────────────────────────────────────────────────
top3 = df_ciudad_ref.sort_values('IPD', ascending=False).head(3)
top3_names = ', '.join(top3['ciudad'].str.split(' ').str[0].tolist())

st.markdown(f"""
<div class="insight-box" style="margin-top: 15px;">
    🎯 <strong>Conclusión Estratégica {int(anio_ref)}:</strong>
    La pregunta para 2026 no es <em>¿dónde vive más gente?</em>, sino 
    <em>¿dónde está creciendo más rápido el consumidor digital de mercados emergentes?</em><br><br>
    Los datos indican que las ciudades intermedias <strong>{top3_names}</strong> concentran el mayor 
    <strong>Índice de Potencial Digital (IPD)</strong>, combinando alta cobertura 4G LTE con 
    condiciones económicas favorables (baja tasa de desempleo y alta ocupación). 
    Redirigir hasta el <strong>30% del presupuesto de pauta</strong> hacia estas plazas 
    permitirá capturar mercados digitales en rápida aceleración con menor saturación competitiva 
    y la mayor eficiencia de costo por impacto de Colombia.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:15px 0 10px; font-size:0.7rem; color:#334155;'>
    DataMart Colombia · Dashboard de Visualización Estratégica · 
    Fuentes: MinTIC (Cobertura Móvil 2015–2023) · DANE GEIH (Año Móvil Abr 2025–Mar 2026)
</div>
""", unsafe_allow_html=True)
