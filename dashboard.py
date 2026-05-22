import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Colombianos Detenidos en el Exterior | UTB",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Definición de Colores UTB ────────────────────────────────────────────────
UTB_AZUL = "#303990"
UTB_VERDE = "#219C1C"
UTB_BLANCO = "#FFFFFF"
UTB_GRIS_FOND = "transparent" # Cambiado a transparente para unificación total
UTB_TEXTO = "#1E1E1E"
UTB_GRIS_SUB = "#333333"

# ── CSS personalizado (Enfoque Borderless y Unificado) ───────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');

/* Configuración General - Mantiene el fondo original intacto */
.stApp {{
    background: linear-gradient(135deg, #A8B0E8 0%, #A8DCA7 50%, #FFFFFF 100%);
    background-attachment: fixed;
    color: {UTB_TEXTO} !important;
    font-family: 'Inter', sans-serif;
}}

/* Forzar color de texto oscuro en todos los elementos nativos de Streamlit */
.stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp caption {{
    color: {UTB_TEXTO} !important;
}}

/* Sidebar Unificado con el Fondo */
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.15) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
}}
[data-testid="stSidebar"] * {{
    color: {UTB_TEXTO} !important;
}}
.sidebar-section {{
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {UTB_AZUL} !important;
    margin: 1.5rem 0 0.5rem;
}}

/* Inputs y Selectores Minimalistas Translucidos */
[data-baseweb="select"], [data-baseweb="multiselect"], .stSelectbox div, .stMultiSelect div {{
    background-color: rgba(255, 255, 255, 0.4) !important;
    color: {UTB_TEXTO} !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 6px !important;
}}
[data-baseweb="popover"] * {{
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: {UTB_TEXTO} !important;
}}
div[role="option"] {{
    background-color: transparent !important;
    color: {UTB_TEXTO} !important;
}}
div[role="option"]:hover {{
    background-color: rgba(48, 57, 144, 0.1) !important;
}}
svg {{
    fill: {UTB_TEXTO} !important;
}}

/* Header Principal Borderless */
.main-header {{
    background-color: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding: 2rem 1rem 1.5rem;
    margin: -1rem -1rem 2rem -1rem;
}}
.header-eyebrow {{
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    color: {UTB_AZUL} !important;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}}
.header-title {{
    font-weight: 700;
    font-size: 2.2rem;
    color: #000000 !important;
    line-height: 1.2;
    margin: 0;
}}
.header-subtitle {{
    font-size: 0.95rem;
    color: {UTB_TEXTO} !important;
    margin-top: 0.5rem;
    font-weight: 400;
}}

/* KPIs Integrados Sin Tarjetas Sólidas */
[data-testid="stMetric"] {{
    background-color: rgba(255, 255, 255, 0.25) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 0.8rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03) !important;
    backdrop-filter: blur(5px);
}}
[data-testid="stMetricLabel"] {{
    color: #222222 !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}}
[data-testid="stMetricValue"] {{
    color: #000000 !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
}}

/* Tabs Integrados */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    gap: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    background-color: transparent !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    height: 40px;
    font-weight: 500 !important;
    color: {UTB_TEXTO} !important;
    background-color: transparent !important;
    border: none !important;
    padding: 0 0.5rem !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: #000000 !important;
    border-bottom: 2px solid #000000 !important;
    font-weight: 700 !important;
}}

/* Secciones */
.section-header {{
    font-size: 1.3rem;
    font-weight: 600;
    color: #000000 !important;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}}
.section-badge {{
    font-size: 0.65rem;
    background-color: rgba(255, 255, 255, 0.3);
    color: {UTB_AZUL} !important;
    border: 1px solid rgba(255, 255, 255, 0.4);
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-weight: 600;
}}

/* Hallazgos Flotantes Sin Contenedor Blanco */
.hallazgo {{
    background-color: rgba(255, 255, 255, 0.2) !important;
    backdrop-filter: blur(5px);
    border-left: 4px solid #000000;
    padding: 1.2rem;
    border-radius: 8px;
    font-size: 0.9rem;
    color: {UTB_TEXTO} !important;
    margin-top: 1rem;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
}}
.hallazgo strong {{
    color: #000000 !important;
}}

/* Dataframes Transparentes */
[data-testid="stDataFrame"] {{
    background-color: rgba(255, 255, 255, 0.15) !important;
    backdrop-filter: blur(10px);
    border-radius: 8px;
}}
[data-testid="stDataFrame"] * {{
    color: {UTB_TEXTO} !important;
}}

div[data-testid="column"] {{ gap: 0.5rem; }}
</style>
""", unsafe_allow_html=True)

# ── Configuración Maestra de Plotly (Modo Unificado y Borderless) ───────────
PLOTLY_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="rgba(0,0,0,0)", # 100% Transparente para fundirse con el fondo
    plot_bgcolor="rgba(0,0,0,0)",  # 100% Transparente
    font=dict(family="'Inter', sans-serif", color="#000000", size=11), # Forzado Negro
    title_font=dict(color="#000000", size=14, family="'Inter', sans-serif"), # Forzado Negro
    legend=dict(
        font=dict(color="#000000", size=10), # Forzado Negro
        bgcolor="rgba(255,255,255,0.2)",
        title=dict(font=dict(color="#000000", size=10)) # Forzado Negro
    ),
    xaxis=dict(
        gridcolor="rgba(255, 255, 255, 0.25)",
        linecolor="rgba(0, 0, 0, 0.1)",
        tickcolor="rgba(0, 0, 0, 0.2)",
        tickfont=dict(color="#000000", size=10), # Forzado Negro
        title_font=dict(color="#000000", size=11), # Forzado Negro
        zerolinecolor="rgba(255, 255, 255, 0.3)"
    ),
    yaxis=dict(
        gridcolor="rgba(255, 255, 255, 0.25)",
        linecolor="rgba(0, 0, 0, 0.1)",
        tickcolor="rgba(0, 0, 0, 0.2)",
        tickfont=dict(color="#000000", size=10), # Forzado Negro
        title_font=dict(color="#000000", size=11), # Forzado Negro
        zerolinecolor="rgba(255, 255, 255, 0.3)"
    ),
    margin=dict(t=60, b=50, l=10, r=10),
    colorway=[UTB_AZUL, UTB_VERDE, "#5C6BC0", "#81C784", "#3F51B5", "#A5D6A7"],
)

def L(**overrides):
    import copy
    base = copy.deepcopy(PLOTLY_LAYOUT)
    for key, value in overrides.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            base[key].update(value)
        else:
            base[key] = value
    return base

# ── Carga y limpieza de datos ────────────────────────────────────────────────
@st.cache_data(show_spinner="Cargando dataset…")
def cargar_datos():
    df = pd.read_csv(
        "Colombianos_detenidos_en_el_exterior_20260427.csv",
        encoding="utf-8", on_bad_lines="skip", low_memory=False,
    )
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    reemplazos = {
        "NARCOTR\ufffdFICO": "NARCOTRÁFICO",
        "ESPA\ufffdA": "ESPAÑA",
        "EN INVESTIGACI\ufffdN": "EN INVESTIGACIÓN",
        "EN ESPERA DE DEPORTACI\ufffdN": "EN ESPERA DE DEPORTACIÓN",
        "NO REPORTA \ufffd CONFIDENCIALIDAD ESTATAL": "CONFIDENCIALIDAD ESTATAL",
    }
    for col in df.select_dtypes(include="object").columns:
        for malo, bueno in reemplazos.items():
            df[col] = df[col].astype(str).str.replace(malo, bueno, regex=False)

    df["FECHA PUBLICACIÓN"] = pd.to_datetime(df["FECHA PUBLICACIÓN"], errors="coerce")
    df["AÑO"] = df["FECHA PUBLICACIÓN"].dt.year.astype("Int64")
    df["AÑO_MES"] = df["FECHA PUBLICACIÓN"].dt.to_period("M")

    def a_float(v):
        try: return float(str(v).replace(",", "."))
        except: return np.nan

    df["LATITUD"]  = df["LATITUD"].apply(a_float)
    df["LONGITUD"] = df["LONGITUD"].apply(a_float)

    df["GÉNERO"] = df["GÉNERO"].str.strip().str.upper()
    df["GÉNERO"] = df["GÉNERO"].replace({"DESCONOCIDO": "NO REPORTA"})

    return df

try:
    df_raw = cargar_datos()
except FileNotFoundError:
    st.error("No se encontró el archivo CSV. Asegúrate de que esté en la misma carpeta.")
    st.stop()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:0.5rem 0 0.5rem;'>
        <div style='font-family:Inter,sans-serif;font-size:0.65rem;letter-spacing:0.2em;color:{UTB_AZUL};font-weight:600;text-transform:uppercase;margin-bottom:0.2rem;'>Sistema de Filtros</div>
        <div style='font-family:Inter,sans-serif;font-size:1.2rem;color:#000000;font-weight:700;'>Panel de Control</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<div class='sidebar-section'>Rango de años</div>", unsafe_allow_html=True)
    años_disp = sorted([int(a) for a in df_raw["AÑO"].dropna().unique()])
    col_d, col_h = st.columns(2)
    with col_d:
        desde = st.selectbox("Desde", años_disp, index=0)
    with col_h:
        años_hasta = [a for a in años_disp if a >= desde]
        hasta = st.selectbox("Hasta", años_hasta, index=len(años_hasta)-1)
    rango_años = (desde, hasta)

    st.markdown("<div class='sidebar-section'>País de detención</div>", unsafe_allow_html=True)
    paises_disp = sorted([p for p in df_raw["PAIS PRISIÓN"].unique() if p not in ("DESCONOCIDO", "nan", "EXTRADICION")])
    pais_sel = st.multiselect("", paises_disp, placeholder="Todos los países", label_visibility="collapsed")

    st.markdown("<div class='sidebar-section'>Situación jurídica</div>", unsafe_allow_html=True)
    sj_disp = sorted([s for s in df_raw["SITUACIÓN JURÍDICA"].unique() if "CONFIDENCIALIDAD" not in s and s != "nan"])
    sj_sel = st.multiselect("", sj_disp, placeholder="Todas", label_visibility="collapsed")

    st.markdown("<div class='sidebar-section'>Género</div>", unsafe_allow_html=True)
    gen_disp = ["MASCULINO", "FEMENINO", "OTRO", "NO REPORTA"]
    gen_sel = st.multiselect("", gen_disp, placeholder="Todos", label_visibility="collapsed")

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.7rem;color:#333333;font-family:Inter,sans-serif;'>
        Fuente: Cancillería de Colombia<br>datos.gov.co · 2018–2025
    </div>""", unsafe_allow_html=True)

# ── Aplicar filtros ──────────────────────────────────────────────────────────
df = df_raw.copy()
df = df[df["AÑO"].between(rango_años[0], rango_años[1])]
if pais_sel:
    df = df[df["PAIS PRISIÓN"].isin(pais_sel)]
if sj_sel:
    df = df[df["SITUACIÓN JURÍDICA"].isin(sj_sel)]
if gen_sel:
    df = df[df["GÉNERO"].isin(gen_sel)]

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='main-header'>
    <div class='header-eyebrow'>Universidad Tecnológica de Bolívar · datos.gov.co</div>
    <h1 class='header-title'>Colombianos Detenidos en el Exterior</h1>
    <p class='header-subtitle'>Análisis exploratorio · Período {rango_años[0]}–{rango_años[1]} · {len(df):,} registros activos</p>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────────────────────
total_det  = df["CANTIDAD"].sum()
n_paises   = df[~df["PAIS PRISIÓN"].isin(["DESCONOCIDO","EXTRADICION"])]["PAIS PRISIÓN"].nunique()
_s_delito  = df[df["DELITO"]!="DESCONOCIDO"].groupby("DELITO")["CANTIDAD"].sum()
top_delito = _s_delito.idxmax() if not _s_delito.empty else "—"
_s_pais    = df[~df["PAIS PRISIÓN"].str.contains("DESCONOCIDO|EXTRADICION|REPATRIACION", na=True) & (df["DELITO"] != "DESCONOCIDO")].groupby("PAIS PRISIÓN")["CANTIDAD"].sum()
top_pais   = _s_pais.idxmax() if not _s_pais.empty else "—"

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Detenidos", f"{total_det:,.0f}")
with col2:
    st.metric("Países Involucrados", f"{n_paises}")
with col3:
    st.metric("Registros", f"{len(df):,}")
with col4:
    st.metric("Delito Principal", top_delito.title()[:20])
with col5:
    st.metric("País #1", top_pais.title()[:18])

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Países & Delitos",
    "Género & Edad",
    "Evolución Temporal",
    "Datos Crudos",
])

# ================================================================================
# TAB 1 — Países y Delitos
# ================================================================================
with tab1:
    st.markdown("""
    <div class='section-header'>
        ¿En qué países y por qué delitos?
    </div>
    """, unsafe_allow_html=True)

    _excluir_pais = df["PAIS PRISIÓN"].str.contains("DESCONOCIDO|EXTRADICION|REPATRIACION", na=True)
    df_p1 = df[~_excluir_pais & (df["DELITO"] != "DESCONOCIDO")]
    df_delitos = df[df["DELITO"] != "DESCONOCIDO"]

    top_del = (df_delitos.groupby("DELITO")["CANTIDAD"]
               .sum().sort_values(ascending=False).reset_index())
    top_del.columns = ["Delito", "Total"]
    top_del["Porcentaje"] = (top_del["Total"] / top_del["Total"].sum() * 100).round(1)

    paises_disponibles = not df_p1.empty

    if not paises_disponibles:
        col_aviso, col_b = st.columns([3, 2])
        with col_aviso:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.2); backdrop-filter: blur(5px); border-left:3px solid #E74C3C;
                        padding:1.4rem 1.6rem; border-radius:8px; margin-top:0.5rem;'>
                <div style='font-family:Inter,sans-serif; font-size:0.65rem; letter-spacing:0.2em;
                            text-transform:uppercase; color:#E74C3C; margin-bottom:0.7rem; font-weight:600;'>
                    ⚠ Dato no disponible para el período seleccionado
                </div>
                <div style='font-family:Inter,sans-serif; font-size:0.9rem; color:{UTB_TEXTO}; line-height:1.7;'>
                    A partir de <strong>2023</strong>, la Cancillería de Colombia dejó de publicar el país de detención en el dataset oficial.
                    Todos los registros de este período aparecen como <code style='background:rgba(255, 255, 255, 0.3); padding:0.1rem 0.4rem;
                    border-radius:4px; color:#000000;'>DESCONOCIDO</code>.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        top15 = (df_p1.groupby("PAIS PRISIÓN")["CANTIDAD"]
                 .sum().sort_values(ascending=False).head(15).reset_index())
        top15.columns = ["País", "Total"]
        top15["Porcentaje"] = (top15["Total"] / top15["Total"].sum() * 100).round(1)

        col_a, col_b = st.columns([3, 2])
        with col_a:
            p10 = top15.head(10).iloc[::-1]
            colores_p = [UTB_AZUL if i < 3 else UTB_VERDE if i < 6 else "#5C6BC0" for i in range(len(p10))]

            fig_paises = go.Figure(go.Bar(
                y=p10["País"], x=p10["Total"],
                orientation="h",
                marker_color=colores_p,
                text=p10.apply(lambda r: f"  {r['Total']:,.0f} ({r['Porcentaje']}%)", axis=1),
                textposition="outside",
                textfont=dict(color="#000000", size=10), # Forzado Negro
                hovertemplate="<b>%{y}</b><br>Total: %{x:,.0f}<extra></extra>",
            ))
            fig_paises.update_layout(**L(
                title="<b>Top 10 Países con Más Colombianos Detenidos</b>",
                height=380, xaxis_title="Total de detenidos", yaxis_title="", showlegend=False
            ))
            fig_paises.update_xaxes(range=[0, p10["Total"].max() * 1.35])
            st.plotly_chart(fig_paises, use_container_width=True)

    if not top_del.empty:
        with col_b:
            d8 = top_del.head(7)
            resto = top_del.iloc[7:]["Total"].sum()
            labels = d8["Delito"].tolist() + (["OTROS"] if resto > 0 else [])
            values = d8["Total"].tolist() + ([resto]   if resto > 0 else [])
            colores_d = [UTB_AZUL, UTB_VERDE, "#5C6BC0", "#81C784", "#3F51B5", "#A5D6A7", "#9FA8DA"]

            pct_top = top_del.iloc[0]["Porcentaje"]
            nombre_top = top_del.iloc[0]["Delito"].lower()

            fig_donut = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.55,
                marker=dict(colors=colores_d[:len(labels)], line=dict(color="rgba(255,255,255,0.4)", width=1.5)),
                textfont=dict(color="#000000", size=10), # Forzado Negro
                hovertemplate="<b>%{label}</b><br>%{value:,.0f} detenidos<br>%{percent}<extra></extra>",
            ))
            fig_donut.add_annotation(
                text=f"<b>{pct_top}%</b><br><span style='font-size:10px;color:#000000'>{nombre_top[:14]}</span>",
                x=0.5, y=0.5, showarrow=False, font=dict(color="#000000", size=14), # Forzado Negro
            )
            fig_donut.update_layout(**L(
                title="<b>Distribución por Delito</b>", height=380,
                legend=dict(font=dict(size=9, color="#000000"), orientation="v", x=1, y=0.5), # Forzado Negro
            ))
            st.plotly_chart(fig_donut, use_container_width=True)

    if paises_disponibles and not top_del.empty:
        top8_p = top15["País"].head(8).tolist()
        top5_d = top_del["Delito"].head(5).tolist()
        pivot = (df_p1[df_p1["PAIS PRISIÓN"].isin(top8_p) & df_p1["DELITO"].isin(top5_d)]
                 .groupby(["PAIS PRISIÓN", "DELITO"])["CANTIDAD"]
                 .sum().unstack(fill_value=0))

        if not pivot.empty:
            fig_heat = px.imshow(
                pivot,
                color_continuous_scale=[[0, "rgba(255,255,255,0.2)"], [0.2, "rgba(48, 57, 144, 0.1)"], [0.7, UTB_AZUL], [1, "#1A237E"]],
                text_auto=",", aspect="auto",
            )
            fig_heat.update_layout(**L(
                title="<b>Heatmap — Detenidos por País y Delito</b>", height=340,
                coloraxis=dict(colorbar=dict(tickfont=dict(color="#000000"), title=dict(font=dict(color="#000000")))) # Forzado Negro
            ))
            fig_heat.update_traces(textfont=dict(size=10, color="#000000")) # Forzado Negro
            st.plotly_chart(fig_heat, use_container_width=True)

# ================================================================================
# TAB 2 — Género y Edad
# ================================================================================
with tab2:
    st.markdown("""
    <div class='section-header'>
        ¿Diferencias según género y grupo de edad?
    </div>
    """, unsafe_allow_html=True)

    df_p2 = df[df["GÉNERO"].isin(["MASCULINO","FEMENINO"]) &
               ~df["SITUACIÓN JURÍDICA"].str.contains("NO REPORTA|EXTRADITA|CONFIDENCIALIDAD", na=False)]

    col_c, col_d = st.columns(2)
    colores_gen = [UTB_AZUL, UTB_VERDE, "#5C6BC0", "#81C784", "#3F51B5"]

    with col_c:
        tabla = pd.crosstab(
            df_p2["GÉNERO"], df_p2["SITUACIÓN JURÍDICA"],
            values=df_p2["CANTIDAD"], aggfunc="sum"
        ).fillna(0)
        tabla_pct = tabla.div(tabla.sum(axis=1), axis=0) * 100

        fig_gen = go.Figure()
        for i, sj in enumerate(tabla_pct.columns):
            fig_gen.add_trace(go.Bar(
                name=sj.title(), x=tabla_pct.index, y=tabla_pct[sj].round(1),
                marker_color=colores_gen[i % len(colores_gen)],
                text=tabla_pct[sj].apply(lambda x: f"{x:.1f}%"),
                textposition="outside",
                textfont=dict(color="#000000", size=9), # Forzado Negro
                hovertemplate="<b>%{x}</b><br>" + sj + ": %{y:.1f}%<extra></extra>",
            ))
        fig_gen.update_layout(**L(
            title="<b>Situación Jurídica por Género (%)</b>", barmode="group", height=370,
            yaxis_title="Porcentaje (%)", legend=dict(font=dict(size=9, color="#000000")), # Forzado Negro
        ))
        st.plotly_chart(fig_gen, use_container_width=True)

    with col_d:
        orden_edad = ["ADOLESCENTE","ADULTO JOVEN","ADULTO","ADULTO MAYOR"]
        df_edad = df[df["GRUPO EDAD"].isin(orden_edad) &
                     ~df["SITUACIÓN JURÍDICA"].str.contains("NO REPORTA|EXTRADITA|CONFIDENCIALIDAD", na=False)]
        tabla_edad = pd.crosstab(
            df_edad["GRUPO EDAD"], df_edad["SITUACIÓN JURÍDICA"],
            values=df_edad["CANTIDAD"], aggfunc="sum"
        ).fillna(0)
        tabla_edad_pct = tabla_edad.div(tabla_edad.sum(axis=1), axis=0) * 100
        tabla_edad_pct = tabla_edad_pct.reindex(orden_edad)

        fig_edad = go.Figure()
        for i, sj in enumerate(tabla_edad_pct.columns):
            fig_edad.add_trace(go.Bar(
                name=sj.title(), x=tabla_edad_pct.index, y=tabla_edad_pct[sj].round(1),
                marker_color=colores_gen[i % len(colores_gen)],
                hovertemplate="<b>%{x}</b><br>" + sj + ": %{y:.1f}%<extra></extra>",
            ))
        fig_edad.update_layout(**L(
            title="<b>Situación Jurídica por Grupo de Edad (%)</b>", barmode="stack", height=370,
            yaxis_title="Porcentaje (%)", legend=dict(font=dict(size=9, color="#000000"), orientation="h", y=-0.25), # Forzado Negro
        ))
        st.plotly_chart(fig_edad, use_container_width=True)

    col_e, col_f = st.columns([1, 2])

    with col_e:
        try:
            chi2_val, p_val, dof, _ = stats.chi2_contingency(tabla)
            sig = p_val < 0.05
            color_sig = UTB_VERDE if sig else "#E74C3C"
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.2); backdrop-filter: blur(5px); border-left:4px solid {color_sig};
                        padding:1.2rem; border-radius:8px;'>
                <div style='font-family:Inter,sans-serif; font-size:0.65rem; letter-spacing:0.15em;
                            text-transform:uppercase; color:#000000; margin-bottom:0.8rem; font-weight:700;'>
                    Prueba Chi² de Independencia
                </div>
                <div style='display:flex; flex-direction:column; gap:0.6rem;'>
                    <div>
                        <span style='font-size:0.8rem; color:{UTB_TEXTO}; font-weight:600;'>Valor χ²:</span>
                        <span style='font-size:1.2rem; color:#000000; font-weight:700; margin-left:0.5rem;'>{chi2_val:,.1f}</span>
                    </div>
                    <div>
                        <span style='font-size:0.8rem; color:{UTB_TEXTO}; font-weight:600;'>p-valor:</span>
                        <span style='font-size:0.9rem; color:#000000; font-family:monospace; font-weight:700; margin-left:0.5rem;'>{p_val:.2e}</span>
                    </div>
                    <div>
                        <span style='font-size:0.8rem; color:{UTB_TEXTO}; font-weight:600;'>Grados L.:</span>
                        <span style='font-size:0.9rem; color:#000000; font-weight:700; margin-left:0.5rem;'>{dof}</span>
                    </div>
                </div>
                <div style='margin-top:0.9rem; padding:0.4rem; background:rgba(255,255,255,0.2); border:1px solid {color_sig}; border-radius:4px;
                            font-size:0.75rem; color:{color_sig}; font-weight:700; text-align:center;'>
                    {"✓ Diferencia significativa" if sig else "✗ Sin diferencia significativa"}
                </div>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.info("Datos insuficientes para Chi².")

    with col_f:
        gen_total = df[df["GÉNERO"].isin(["MASCULINO","FEMENINO","OTRO"])].groupby("GÉNERO")["CANTIDAD"].sum()
        fig_pie_gen = go.Figure(go.Pie(
            labels=gen_total.index, values=gen_total.values, hole=0.5,
            marker=dict(colors=[UTB_AZUL, UTB_VERDE, "#5C6BC0"], line=dict(color="rgba(255,255,255,0.4)", width=1.5)),
            textfont=dict(color="#000000", size=10), # Forzado Negro
            hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig_pie_gen.update_layout(**L(
            title="<b>Distribución por Género</b>", height=260,
            legend=dict(orientation="h", y=-0.1, font=dict(color="#000000")), # Forzado Negro
        ))
        st.plotly_chart(fig_pie_gen, use_container_width=True)

    st.markdown(f"""
    <div class='hallazgo'>
         <strong>Hallazgo P2:</strong> La prueba Chi-cuadrado confirma que la situación jurídica <strong>sí varía significativamente según el género</strong> (p &lt; 0.05).
    </div>
    """, unsafe_allow_html=True)

# ================================================================================
# TAB 3 — Evolución Temporal
# ================================================================================
with tab3:
    st.markdown("""
    <div class='section-header'>
        Evolución temporal 2018–2025
    </div>
    """, unsafe_allow_html=True)

    serie_anual = df.groupby("AÑO")["CANTIDAD"].sum().reset_index()
    serie_anual.columns = ["AÑO", "TOTAL"]
    serie_anual = serie_anual.dropna()

    serie_mensual = df.groupby("AÑO_MES")["CANTIDAD"].sum().reset_index()
    serie_mensual["FECHA"] = serie_mensual["AÑO_MES"].dt.to_timestamp()
    serie_mensual["MM3"]   = serie_mensual["CANTIDAD"].rolling(3, center=True).mean()
    serie_mensual = serie_mensual.dropna(subset=["FECHA"])

    fig_serie = go.Figure()
    fig_serie.add_trace(go.Scatter(
        x=serie_mensual["FECHA"], y=serie_mensual["CANTIDAD"], mode="lines", name="Total mensual",
        line=dict(color=UTB_AZUL, width=1.5), fill="tozeroy", fillcolor="rgba(48, 57, 144, 0.05)",
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:,.0f} detenidos<extra></extra>",
    ))
    fig_serie.add_trace(go.Scatter(
        x=serie_mensual["FECHA"], y=serie_mensual["MM3"], mode="lines", name="Media móvil (3m)",
        line=dict(color=UTB_VERDE, width=2.5), hovertemplate="<b>%{x|%b %Y}</b><br>Media: %{y:,.0f}<extra></extra>",
    ))

    if rango_años[0] <= 2020 <= rango_años[1]:
        fig_serie.add_vrect(
            x0="2020-03-01", x1="2021-12-31", fillcolor="rgba(231, 76, 60, 0.08)", line_width=0,
            annotation_text="<b>COVID-19</b>", annotation_position="top left",
            annotation_font=dict(color="#000000", size=10), # Forzado Negro
        )
    fig_serie.update_layout(**L(
        title="<b>Evolución Mensual de Colombianos Detenidos en el Exterior</b>", height=320,
        yaxis_title="Total mensual", legend=dict(orientation="h", y=1.1, x=0, font=dict(color="#000000")), # Forzado Negro
    ))
    st.plotly_chart(fig_serie, use_container_width=True)

    serie_anual["VAR"] = serie_anual["TOTAL"].pct_change() * 100
    fig_anual = make_subplots(
        rows=1, cols=2, column_widths=[0.65, 0.35],
        subplot_titles=["<b>Total Anual de Detenidos</b>", "<b>Variación Anual (%)</b>"],
    )
    colores_bar = [UTB_VERDE if y in [2020,2021] else UTB_AZUL for y in serie_anual["AÑO"]]

    fig_anual.add_trace(go.Bar(
        x=serie_anual["AÑO"].astype(str), y=serie_anual["TOTAL"], marker_color=colores_bar,
        text=serie_anual["TOTAL"].apply(lambda x: f"{x:,.0f}"), textposition="outside",
        textfont=dict(color="#000000", size=10), # Forzado Negro
        hovertemplate="<b>%{x}</b><br>%{y:,.0f}<extra></extra>", showlegend=False,
    ), row=1, col=1)

    fig_anual.add_trace(go.Bar(
        x=serie_anual["AÑO"].astype(str), y=serie_anual["VAR"].round(1),
        marker_color=[UTB_VERDE if v < 0 else UTB_AZUL for v in serie_anual["VAR"].fillna(0)],
        text=serie_anual["VAR"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else ""), textposition="outside",
        textfont=dict(color="#000000", size=10), # Forzado Negro
        hovertemplate="<b>%{x}</b><br>Var: %{y:+.1f}%<extra></extra>", showlegend=False,
    ), row=1, col=2)

    fig_anual.update_layout(**L(height=320))
    fig_anual.update_xaxes(tickfont=dict(color="#000000", size=10), title_font=dict(color="#000000"), linecolor="rgba(0, 0, 0, 0.1)") # Forzado Negro
    fig_anual.update_yaxes(tickfont=dict(color="#000000", size=10), title_font=dict(color="#000000"), linecolor="rgba(0, 0, 0, 0.1)", gridcolor="rgba(255, 255, 255, 0.25)") # Forzado Negro

    for i in fig_anual['layout']['annotations']:
        i['font'] = dict(color="#000000", size=12) # Forzado Negro

    st.plotly_chart(fig_anual, use_container_width=True)

# ================================================================================
# TAB 4 — Datos Crudos
# ================================================================================
with tab4:
    st.markdown("""
    <div class='section-header'>
        Dataset Filtrado
        
    </div>
    """, unsafe_allow_html=True)

    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Registros visibles", f"{len(df):,}")
    with col_info2:
        st.metric("Total CANTIDAD", f"{df['CANTIDAD'].sum():,.0f}")
    with col_info3:
        st.metric("Mediana CANTIDAD", f"{df['CANTIDAD'].median():.0f}")

    cols_mostrar = ["FECHA PUBLICACIÓN","PAIS PRISIÓN","CONSULADO","DELITO",
                    "SITUACIÓN JURÍDICA","GÉNERO","GRUPO EDAD","CANTIDAD"]
    st.dataframe(
        df[cols_mostrar].sort_values("FECHA PUBLICACIÓN", ascending=False).head(500),
        use_container_width=True, hide_index=True,
        column_config={
            "FECHA PUBLICACIÓN": st.column_config.DateColumn("Fecha", format="YYYY-MM-DD"),
            "CANTIDAD": st.column_config.NumberColumn("Cantidad", format="%d"),
        },
    )
    st.caption("Mostrando máximo 500 registros con los filtros activos.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-top:3rem; padding:1rem 0; border-top:1px solid rgba(255, 255, 255, 0.3);
            font-size:0.75rem; color:{UTB_TEXTO}; display:flex; justify-content:space-between; font-family:Inter,sans-serif;'>
    <span>Universidad Tecnológica de Bolívar · Escuela de Transformacion Digital</span>
    <span>2026</span>
</div>
""", unsafe_allow_html=True)