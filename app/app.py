import html as html_lib

import altair as alt
import pandas as pd
import streamlit as st

from backend import (
    verificar_artefactos,
    cargar_artistas,
    cargar_metricas,
    cargar_metadata,
    cargar_importancia_shap,
    obtener_distribucion_clusters,
    filtrar_artistas,
    obtener_artista,
)


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Spotify Chile | Programación musical",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# COLORES
# ============================================================

GREEN = "#1DB954"
GREEN_LIGHT = "#1ED760"

BLACK = "#191414"
DARK = "#0F172A"

BLUE = "#2563EB"
ORANGE = "#F59E0B"
PURPLE = "#7C3AED"

BORDER = "#DCE3EA"
MUTED = "#64748B"


# ============================================================
# PERFILES
# ============================================================

PERFILES = {

    "Artistas consolidados de alto desempeño local": {
        "nombre": "Consolidado de alto desempeño local",
        "descripcion": (
            "Alta presencia, permanencia prolongada y "
            "buen posicionamiento en los rankings chilenos."
        ),
        "color": PURPLE,
        "icono": "🏆",
    },

    "Presencia sostenida en rankings chilenos": {
        "nombre": "Presencia sostenida",
        "descripcion": (
            "Mantiene una presencia frecuente y estable "
            "durante el periodo analizado."
        ),
        "color": GREEN,
        "icono": "↻",
    },

    "Aparición puntual o comportamiento emergente": {
        "nombre": "Aparición puntual o emergente",
        "descripcion": (
            "Presenta una trayectoria más breve o reciente, "
            "con posibles señales de crecimiento."
        ),
        "color": BLUE,
        "icono": "↗",
    },

    "Baja presencia o menor posicionamiento local": {
        "nombre": "Baja presencia o menor posicionamiento local",
        "descripcion": (
            "Registra menor permanencia o posiciones menos "
            "favorables dentro de los rankings observados."
        ),
        "color": ORANGE,
        "icono": "◌",
    },
}


# ============================================================
# CSS GENERAL
# ============================================================

st.html(
    f"""
    <style>

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    h1 {{
        color: {DARK};
        font-weight: 800;
        letter-spacing: -0.03em;
    }}

    h2,
    h3 {{
        color: {DARK};
        font-weight: 750;
    }}

    /* SIDEBAR */

    [data-testid="stSidebar"] {{
        background-color: {BLACK};
        border-right: 0;
    }}

    [data-testid="stSidebar"] * {{
        color: white;
    }}

    [data-testid="stSidebarNav"] a {{
        border-radius: 8px;
        margin-bottom: 5px;
    }}

    [data-testid="stSidebarNav"] a:hover {{
        background-color: #282828;
    }}

    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background-color: {GREEN};
    }}

    /* BOTONES */

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {{
        border-radius: 8px;
        font-weight: 700;
        min-height: 2.7rem;
    }}

    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button[kind="primary"] {{
        background-color: {GREEN};
        border-color: {GREEN};
        color: white;
    }}

    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {{
        background-color: {GREEN_LIGHT};
        border-color: {GREEN_LIGHT};
        color: {BLACK};
    }}

    div.stButton > button[kind="secondary"],
    div[data-testid="stFormSubmitButton"] > button[kind="secondary"] {{
        background-color: white;
        color: {BLACK};
        border: 1px solid {BORDER};
    }}

    /* INPUTS */

    div[data-baseweb="input"] > div {{
        border: 1px solid #AAB4C0 !important;
        background: white !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="input"] > div:focus-within {{
        border: 2px solid {GREEN} !important;
    }}

    div[data-baseweb="select"] > div {{
        border: 1px solid #AAB4C0 !important;
        background: white !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="select"] > div:focus-within {{
        border: 2px solid {GREEN} !important;
    }}

    /* TABLAS */

    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}

    </style>
    """
)


# ============================================================
# VERIFICACIÓN
# ============================================================

try:

    verificar_artefactos()

except FileNotFoundError as error:

    st.error(
        "No fue posible iniciar la aplicación."
    )

    st.code(
        str(error)
    )

    st.stop()


# ============================================================
# CARGA DE DATOS
# ============================================================

@st.cache_data
def cargar_datos_app():
    return cargar_artistas()


@st.cache_data
def cargar_metricas_app():
    return cargar_metricas()


@st.cache_data
def cargar_metadata_app():
    return cargar_metadata()


@st.cache_data
def cargar_shap_app():
    return cargar_importancia_shap()


artistas = cargar_datos_app()
metricas = cargar_metricas_app()
metadata = cargar_metadata_app()
shap_global = cargar_shap_app()


# ============================================================
# SCROLL
# ============================================================

def scroll_arriba():

    st.html(
        """
        <script>

        function subirPagina() {

            const main =
                document.querySelector('[data-testid="stMain"]')
                ||
                document.querySelector('[data-testid="stAppViewContainer"]');

            if (main) {
                main.scrollTo({
                    top: 0,
                    left: 0,
                    behavior: "auto"
                });
            }

            window.scrollTo({
                top: 0,
                left: 0,
                behavior: "auto"
            });
        }

        subirPagina();
        setTimeout(subirPagina, 100);
        setTimeout(subirPagina, 300);

        </script>
        """,
        unsafe_allow_javascript=True,
    )


def entrar_pagina(nombre):

    pagina_anterior = st.session_state.get(
        "_pagina_actual"
    )

    if pagina_anterior != nombre:

        st.session_state[
            "_pagina_actual"
        ] = nombre

        scroll_arriba()


def scroll_al_detalle():

    """
    Al seleccionar un artista, desplaza automáticamente
    la pantalla al bloque de detalle.
    """

    st.html(
        """
        <div
            id="detalle-artista-seleccionado"
            style="height:1px; scroll-margin-top:25px;"
        ></div>

        <script>

        function irAlDetalle() {

            const destino =
                document.getElementById(
                    "detalle-artista-seleccionado"
                );

            if (destino) {

                destino.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        }

        setTimeout(irAlDetalle, 150);
        setTimeout(irAlDetalle, 350);

        </script>
        """,
        unsafe_allow_javascript=True,
    )


# ============================================================
# FUNCIONES VISUALES
# ============================================================

def texto_intro(texto):

    st.html(
        f"""
        <div style="
            color:#334155;
            font-size:20px;
            line-height:1.65;
            max-width:1250px;
            margin-top:5px;
            margin-bottom:30px;
        ">
            {texto}
        </div>
        """
    )


def tarjeta_metrica(
    titulo,
    valor,
    color=GREEN,
    subtitulo=None,
):

    subtitulo_html = ""

    if subtitulo:

        subtitulo_html = f"""
        <div style="
            color:{MUTED};
            font-size:12px;
            margin-top:5px;
        ">
            {subtitulo}
        </div>
        """

    st.html(
        f"""
        <div style="
            background:white;
            border:1px solid {BORDER};
            border-radius:10px;
            padding:15px 16px;
            min-height:92px;
            border-left:6px solid {color};
        ">

            <div style="
                font-size:12px;
                font-weight:700;
                color:{MUTED};
                margin-bottom:6px;
            ">
                {titulo}
            </div>

            <div style="
                font-size:26px;
                font-weight:800;
                color:{DARK};
                line-height:1.1;
            ">
                {valor}
            </div>

            {subtitulo_html}

        </div>
        """
    )


def titulo_tarjeta(texto):

    st.html(
        f"""
        <div style="
            font-size:18px;
            font-weight:800;
            color:{DARK};
            margin-bottom:8px;
        ">
            {texto}
        </div>
        """
    )


def encabezado_resultados(
    cantidad
):

    st.html(
        f"""
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:20px;
            margin-bottom:12px;
            min-height:34px;
        ">

            <div style="
                font-size:20px;
                font-weight:800;
                color:{DARK};
                white-space:nowrap;
            ">
                Resultados
            </div>

            <div style="
                color:{MUTED};
                font-size:13px;
                text-align:right;
                line-height:1.3;
            ">
                <strong>{cantidad}</strong> artistas
                &nbsp;·&nbsp;
                Seleccione uno para ver su detalle
            </div>

        </div>
        """
    )


def tarjeta_perfil(
    icono,
    nombre,
    descripcion,
    color,
):

    st.html(
        f"""
        <div style="
            background:white;
            border:1px solid {BORDER};
            border-top:5px solid {color};
            border-radius:14px;
            padding:18px;
            min-height:190px;
            box-shadow:0 2px 8px rgba(15,23,42,0.04);
        ">

            <div style="
                width:44px;
                height:44px;
                border-radius:50%;
                background:{color};
                color:white;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:21px;
                font-weight:800;
                margin-bottom:14px;
            ">
                {icono}
            </div>

            <div style="
                font-size:17px;
                font-weight:800;
                color:{DARK};
                line-height:1.25;
                margin-bottom:10px;
            ">
                {nombre}
            </div>

            <div style="
                font-size:14px;
                color:#475569;
                line-height:1.55;
            ">
                {descripcion}
            </div>

        </div>
        """
    )


def caja_aviso(
    texto,
    tipo="amarillo",
):

    if tipo == "verde":

        fondo = "#EAFBF0"
        borde = "#9ADBB2"
        color_texto = "#176B38"

    elif tipo == "azul":

        fondo = "#EFF6FF"
        borde = "#BFDBFE"
        color_texto = "#1D4ED8"

    else:

        fondo = "#FFF7D6"
        borde = "#F1D675"
        color_texto = "#674B00"

    st.html(
        f"""
        <div style="
            background:{fondo};
            border:1px solid {borde};
            border-radius:9px;
            padding:14px 17px;
            color:{color_texto};
            font-size:14px;
            line-height:1.6;
        ">
            {texto}
        </div>
        """
    )


def perfil_amigable(perfil):

    datos = PERFILES.get(
        perfil
    )

    if datos:
        return datos["nombre"]

    return perfil


def descripcion_perfil(perfil):

    datos = PERFILES.get(
        perfil
    )

    if datos:
        return datos["descripcion"]

    return (
        "Este perfil resume patrones de comportamiento "
        "observados en los rankings de Spotify Chile."
    )


def color_perfil(perfil):

    datos = PERFILES.get(
        perfil
    )

    if datos:
        return datos["color"]

    return GREEN


def icono_perfil(perfil):

    datos = PERFILES.get(
        perfil
    )

    if datos:
        return datos["icono"]

    return "♪"


def iniciales_artista(nombre):

    palabras = (
        str(nombre)
        .replace("*", "")
        .split()
    )

    if len(palabras) == 0:
        return "AR"

    if len(palabras) == 1:
        return palabras[0][:2].upper()

    return (
        palabras[0][0]
        +
        palabras[1][0]
    ).upper()


def nombre_variable_amigable(variable):

    nombres = {

        "apariciones_chile":
            "Apariciones en Chile",

        "canciones_unicas_chile":
            "Canciones únicas",

        "rank_promedio_chile":
            "Rank promedio",

        "popularidad_promedio":
            "Popularidad promedio",

        "movimiento_diario_promedio":
            "Movimiento diario promedio",

        "movimiento_semanal_promedio":
            "Movimiento semanal promedio",

        "permanencia_dias":
            "Permanencia",

        "puntaje_posicion_chile":
            "Puntaje de posición",
    }

    return nombres.get(
        variable,
        variable
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.html(
    """
    <div style="
        font-size:25px;
        font-weight:800;
        color:white;
        margin-bottom:4px;
    ">
        🎵 Spotify Chile
    </div>

    <div style="
        font-size:12px;
        color:#B3B3B3;
        margin-bottom:16px;
        line-height:1.5;
    ">
        Apoyo a decisiones de programación musical
    </div>
    """
)


# ============================================================
# PÁGINA 1 - INICIO
# ============================================================

def pagina_inicio():

    entrar_pagina(
        "inicio"
    )

    st.title(
        "Sistema de apoyo a programación musical basado en Spotify Chile"
    )

    texto_intro(
        """
        Su objetivo es entregar información que pueda complementar
        las decisiones de <strong>productoras, equipos de marketing
        y encargados de programación musical</strong>, a partir del
        comportamiento observado de los artistas en los rankings
        diarios de Spotify Chile.
        """
    )

    st.subheader(
        "Cómo interpretar los resultados"
    )

    st.write(
        """
        El sistema organiza a los artistas en **cuatro perfiles**
        según patrones semejantes de presencia, permanencia y
        posicionamiento en los rankings de Spotify Chile.
        """
    )

    st.write("")

    columnas_perfiles = (
        st.columns(4)
    )

    perfiles_ordenados = [

        "Artistas consolidados de alto desempeño local",

        "Presencia sostenida en rankings chilenos",

        "Aparición puntual o comportamiento emergente",

        "Baja presencia o menor posicionamiento local",
    ]

    for columna, perfil in zip(
        columnas_perfiles,
        perfiles_ordenados,
    ):

        datos = (
            PERFILES[
                perfil
            ]
        )

        with columna:

            tarjeta_perfil(
                datos["icono"],
                datos["nombre"],
                datos["descripcion"],
                datos["color"],
            )

    st.write("")

    caja_aviso(
        """
        <strong>Importante:</strong>
        los perfiles describen comportamiento digital observado
        en Spotify Chile. No califican la calidad artística ni
        representan directamente la capacidad real de convocatoria.

        La base no incorpora ventas de entradas, asistencia histórica,
        costos de contratación ni capacidad de recintos.
        """
    )

    st.write("")

    with st.expander(
        "¿Cómo utilizar la aplicación?"
    ):

        st.write(
            """
            **Resumen general**

            Permite conocer la distribución de los artistas
            y los perfiles identificados.

            **Explorar artistas**

            Permite buscar y filtrar artistas. Al seleccionar
            uno en la tabla, la aplicación mostrará y llevará
            automáticamente a su información detallada.

            **Monitoreo técnico**

            Reúne información sobre el funcionamiento y
            desempeño del modelo utilizado por el sistema.
            """
        )


# ============================================================
# PÁGINA 2 - RESUMEN GENERAL
# ============================================================

def pagina_resumen():

    entrar_pagina(
        "resumen"
    )

    st.title(
        "Resumen general"
    )

    texto_intro(
        """
        Una visión rápida de los artistas presentes en la base
        y de los perfiles identificados a partir de su comportamiento
        en Spotify Chile.
        """
    )

    cantidad_artistas = len(
        artistas
    )

    cantidad_perfiles = int(
        artistas[
            "perfil_cluster"
        ]
        .nunique()
    )

    cantidad_variables = int(
        metricas[
            "n_variables"
        ]
    )

    columnas = st.columns(4)

    with columnas[0]:

        tarjeta_metrica(
            "Artistas analizados",
            cantidad_artistas,
            GREEN,
        )

    with columnas[1]:

        tarjeta_metrica(
            "Perfiles identificados",
            cantidad_perfiles,
            PURPLE,
        )

    with columnas[2]:

        tarjeta_metrica(
            "Variables consideradas",
            cantidad_variables,
            BLUE,
        )

    with columnas[3]:

        tarjeta_metrica(
            "Mercado analizado",
            "Chile",
            ORANGE,
            "Spotify",
        )

    st.write("")

    col1, col2 = (
        st.columns(2)
    )

    # --------------------------------------------------------
    # DISTRIBUCIÓN
    # --------------------------------------------------------

    with col1:

        with st.container(
            border=True
        ):

            titulo_tarjeta(
                "Distribución de artistas por perfil"
            )

            distribucion = (
                obtener_distribucion_clusters()
                .copy()
            )

            distribucion[
                "Perfil"
            ] = (
                distribucion[
                    "perfil"
                ]
                .apply(
                    perfil_amigable
                )
            )

            dominio = [

                "Consolidado de alto desempeño local",

                "Presencia sostenida",

                "Aparición puntual o emergente",

                "Baja presencia o menor posicionamiento local",
            ]

            colores = [
                PURPLE,
                GREEN,
                BLUE,
                ORANGE,
            ]

            grafico = (

                alt.Chart(
                    distribucion
                )

                .mark_bar()

                .encode(

                    x=alt.X(
                        "cantidad:Q",
                        title="Cantidad de artistas",
                    ),

                    y=alt.Y(
                        "Perfil:N",
                        title=None,
                        sort="-x",
                    ),

                    color=alt.Color(
                        "Perfil:N",
                        scale=alt.Scale(
                            domain=dominio,
                            range=colores,
                        ),
                        legend=None,
                    ),

                    tooltip=[
                        alt.Tooltip(
                            "Perfil:N",
                            title="Perfil",
                        ),

                        alt.Tooltip(
                            "cantidad:Q",
                            title="Artistas",
                        ),
                    ],
                )

                .properties(
                    height=280
                )
            )

            st.altair_chart(
                grafico,
                use_container_width=True,
            )

    # --------------------------------------------------------
    # ARTISTAS DESTACADOS
    # --------------------------------------------------------

    with col2:

        with st.container(
            border=True
        ):

            titulo_tarjeta(
                "Artistas con mayor presencia en rankings"
            )

            destacados = (

                artistas

                .sort_values(
                    [
                        "apariciones_chile",
                        "permanencia_dias",
                    ],
                    ascending=[
                        False,
                        False,
                    ],
                )

                .head(8)

                [
                    [
                        "artists",
                        "perfil_cluster",
                        "apariciones_chile",
                        "rank_promedio_chile",
                    ]
                ]

                .copy()
            )

            destacados.columns = [
                "Artista",
                "Perfil",
                "Apariciones",
                "Rank prom.",
            ]

            destacados[
                "Perfil"
            ] = (
                destacados[
                    "Perfil"
                ]
                .apply(
                    perfil_amigable
                )
            )

            destacados[
                "Rank prom."
            ] = (
                destacados[
                    "Rank prom."
                ]
                .round(2)
            )

            st.dataframe(
                destacados,
                hide_index=True,
                use_container_width=True,
                height=335,
            )

    st.write("")

    caja_aviso(
        """
        Utilice <strong>Explorar artistas</strong> para buscar,
        comparar y revisar en detalle un artista.
        """,
        tipo="verde",
    )


# ============================================================
# ESTADO DEL EXPLORADOR
# ============================================================

def inicializar_filtros():

    valores = {

        "filtro_texto_widget":
            "",

        "filtro_perfil_widget":
            "Todos",

        "filtro_texto_aplicado":
            "",

        "filtro_perfil_aplicado":
            "Todos",

        "version_tabla":
            0,
    }

    for clave, valor in valores.items():

        if clave not in st.session_state:

            st.session_state[
                clave
            ] = valor


def limpiar_filtros():

    st.session_state[
        "filtro_texto_widget"
    ] = ""

    st.session_state[
        "filtro_perfil_widget"
    ] = "Todos"

    st.session_state[
        "filtro_texto_aplicado"
    ] = ""

    st.session_state[
        "filtro_perfil_aplicado"
    ] = "Todos"

    st.session_state[
        "version_tabla"
    ] += 1


# ============================================================
# DETALLE INTEGRADO
# ============================================================

def mostrar_detalle_artista(
    nombre_artista
):

    detalle = obtener_artista(
        nombre_artista
    )

    if detalle is None:

        st.error(
            "No fue posible recuperar la información "
            "del artista seleccionado."
        )

        return

    perfil = detalle[
        "perfil_cluster"
    ]

    nombre_seguro = (
        html_lib.escape(
            str(
                detalle[
                    "artists"
                ]
            )
        )
    )

    perfil_visible = (
        perfil_amigable(
            perfil
        )
    )

    perfil_seguro = (
        html_lib.escape(
            perfil_visible
        )
    )

    icono = icono_perfil(
        perfil
    )

    descripcion = (
        html_lib.escape(
            descripcion_perfil(
                perfil
            )
        )
    )

    # --------------------------------------------------------
    # AQUÍ OCURRE EL SCROLL AUTOMÁTICO
    # --------------------------------------------------------

    scroll_al_detalle()

    st.subheader(
        f"Detalle de {detalle['artists']}"
    )

    st.caption(
        "Seleccione otro artista en la tabla para "
        "actualizar esta información."
    )

    # --------------------------------------------------------
    # FICHA PRINCIPAL
    # --------------------------------------------------------

    col_ficha, col_datos = (
        st.columns(
            [1, 2.7]
        )
    )

    with col_ficha:

        with st.container(
            border=True
        ):

            iniciales = (
                iniciales_artista(
                    detalle[
                        "artists"
                    ]
                )
            )

            st.html(
                f"""
                <div style="
                    display:flex;
                    align-items:center;
                    gap:14px;
                    margin-bottom:20px;
                ">

                    <div style="
                        width:64px;
                        min-width:64px;
                        height:64px;
                        border-radius:50%;
                        background:{DARK};
                        color:white;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:18px;
                        font-weight:800;
                    ">
                        {iniciales}
                    </div>

                    <div>

                        <div style="
                            font-size:22px;
                            font-weight:800;
                            color:{DARK};
                            line-height:1.2;
                        ">
                            {nombre_seguro}
                        </div>

                        <div style="
                            color:{MUTED};
                            font-size:13px;
                            margin-top:5px;
                        ">
                            Artista seleccionado
                        </div>

                    </div>

                </div>
                """
            )

            st.html(
                f"""
                <div style="
                    border-left:5px solid {color_perfil(perfil)};
                    background:#F8FAFC;
                    border-radius:8px;
                    padding:14px;
                ">

                    <div style="
                        font-size:27px;
                        margin-bottom:7px;
                    ">
                        {icono}
                    </div>

                    <div style="
                        color:{MUTED};
                        font-size:11px;
                        font-weight:700;
                        text-transform:uppercase;
                        letter-spacing:0.04em;
                        margin-bottom:5px;
                    ">
                        Perfil identificado
                    </div>

                    <div style="
                        color:{DARK};
                        font-size:16px;
                        font-weight:800;
                        line-height:1.35;
                    ">
                        {perfil_seguro}
                    </div>

                </div>
                """
            )

    # --------------------------------------------------------
    # MÉTRICAS
    # --------------------------------------------------------

    with col_datos:

        columnas = (
            st.columns(4)
        )

        with columnas[0]:

            tarjeta_metrica(
                "Apariciones",
                int(
                    detalle[
                        "apariciones_chile"
                    ]
                ),
                GREEN,
            )

        with columnas[1]:

            tarjeta_metrica(
                "Rank promedio",
                f"{detalle['rank_promedio_chile']:.2f}",
                BLUE,
            )

        with columnas[2]:

            tarjeta_metrica(
                "Permanencia",
                int(
                    detalle[
                        "permanencia_dias"
                    ]
                ),
                ORANGE,
                "días",
            )

        with columnas[3]:

            tarjeta_metrica(
                "Popularidad",
                f"{detalle['popularidad_promedio']:.2f}",
                PURPLE,
            )

        st.write("")

        with st.container(
            border=True
        ):

            titulo_tarjeta(
                "Cómo interpretar este perfil"
            )

            st.html(
                f"""
                <div style="
                    display:flex;
                    align-items:flex-start;
                    gap:16px;
                    border-left:5px solid {color_perfil(perfil)};
                    padding:10px 15px;
                ">

                    <div style="
                        font-size:28px;
                        line-height:1;
                    ">
                        {icono}
                    </div>

                    <div>

                        <div style="
                            color:{DARK};
                            font-size:16px;
                            font-weight:800;
                            margin-bottom:8px;
                        ">
                            {perfil_seguro}
                        </div>

                        <div style="
                            color:#475569;
                            font-size:14px;
                            line-height:1.6;
                        ">
                            {descripcion}
                        </div>

                    </div>

                </div>
                """
            )

    st.write("")

    # --------------------------------------------------------
    # SEÑALES OBSERVADAS
    # --------------------------------------------------------

    with st.container(
        border=True
    ):

        titulo_tarjeta(
            "Señales observadas del artista"
        )

        indicadores = (
            pd.DataFrame(
                {
                    "Indicador": [

                        "Apariciones en rankings",

                        "Canciones únicas",

                        "Rank promedio",

                        "Popularidad promedio",

                        "Movimiento diario promedio",

                        "Movimiento semanal promedio",

                        "Permanencia",

                        "Puntaje de posición",
                    ],

                    "Valor": [

                        int(
                            detalle[
                                "apariciones_chile"
                            ]
                        ),

                        int(
                            detalle[
                                "canciones_unicas_chile"
                            ]
                        ),

                        round(
                            detalle[
                                "rank_promedio_chile"
                            ],
                            2,
                        ),

                        round(
                            detalle[
                                "popularidad_promedio"
                            ],
                            2,
                        ),

                        round(
                            detalle[
                                "movimiento_diario_promedio"
                            ],
                            2,
                        ),

                        round(
                            detalle[
                                "movimiento_semanal_promedio"
                            ],
                            2,
                        ),

                        int(
                            detalle[
                                "permanencia_dias"
                            ]
                        ),

                        round(
                            detalle[
                                "puntaje_posicion_chile"
                            ],
                            2,
                        ),
                    ],
                }
            )
        )

        st.dataframe(
            indicadores,
            hide_index=True,
            use_container_width=True,
            height=315,
        )

    st.write("")

    caja_aviso(
        """
        El perfil resume comportamiento digital observado
        en Spotify Chile. No corresponde a una predicción
        directa de venta de entradas ni asistencia a eventos.
        """
    )


# ============================================================
# PÁGINA 3 - EXPLORAR ARTISTAS
# ============================================================

def pagina_explorador():

    entrar_pagina(
        "explorador"
    )

    inicializar_filtros()

    st.title(
        "Explorar artistas"
    )

    st.caption(
        "Busque o filtre artistas y seleccione uno "
        "para revisar su información."
    )

    perfiles = (
        sorted(
            artistas[
                "perfil_cluster"
            ]
            .dropna()
            .unique()
            .tolist()
        )
    )

    opciones_perfil = (
        ["Todos"]
        +
        perfiles
    )

    # ========================================================
    # FILTROS + RESULTADOS
    # ========================================================

    col_filtros, col_resultados = (
        st.columns(
            [1, 3]
        )
    )

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    with col_filtros:

        with st.container(
            border=True
        ):

            titulo_tarjeta(
                "Filtros"
            )

            with st.form(
                "formulario_filtros",
                enter_to_submit=True,
                border=False,
            ):

                st.text_input(
                    "Buscar artista",
                    placeholder=(
                        "Ej.: Bad Bunny"
                    ),
                    key=(
                        "filtro_texto_widget"
                    ),
                )

                st.selectbox(
                    "Perfil",
                    opciones_perfil,
                    key=(
                        "filtro_perfil_widget"
                    ),
                    format_func=(
                        lambda x:
                        "Todos"
                        if x == "Todos"
                        else perfil_amigable(x)
                    ),
                )

                botones = (
                    st.columns(2)
                )

                with botones[0]:

                    aplicar = (
                        st.form_submit_button(
                            "Aplicar filtros",
                            type="primary",
                            use_container_width=True,
                        )
                    )

                with botones[1]:

                    limpiar = (
                        st.form_submit_button(
                            "Limpiar",
                            use_container_width=True,
                            on_click=(
                                limpiar_filtros
                            ),
                        )
                    )

            if aplicar:

                st.session_state[
                    "filtro_texto_aplicado"
                ] = (
                    st.session_state[
                        "filtro_texto_widget"
                    ]
                    .strip()
                )

                st.session_state[
                    "filtro_perfil_aplicado"
                ] = (
                    st.session_state[
                        "filtro_perfil_widget"
                    ]
                )

                st.session_state[
                    "version_tabla"
                ] += 1

    # --------------------------------------------------------
    # RESULTADOS
    # --------------------------------------------------------

    resultados = (
        filtrar_artistas(
            texto=(
                st.session_state[
                    "filtro_texto_aplicado"
                ]
            ),
            cluster=None,
            senal=None,
        )
        .copy()
        .reset_index(
            drop=True
        )
    )

    perfil_aplicado = (
        st.session_state[
            "filtro_perfil_aplicado"
        ]
    )

    if perfil_aplicado != "Todos":

        resultados = (
            resultados[
                resultados[
                    "perfil_cluster"
                ]
                ==
                perfil_aplicado
            ]
            .copy()
            .reset_index(
                drop=True
            )
        )

    artista_seleccionado = None

    # --------------------------------------------------------
    # TABLA
    # --------------------------------------------------------

    with col_resultados:

        with st.container(
            border=True
        ):

            encabezado_resultados(
                len(resultados)
            )

            if resultados.empty:

                st.warning(
                    "No encontramos artistas con los "
                    "criterios seleccionados. Pruebe otro "
                    "nombre, perfil o limpie los filtros."
                )

            else:

                tabla = (
                    resultados[
                        [
                            "artists",
                            "perfil_cluster",
                            "apariciones_chile",
                            "rank_promedio_chile",
                            "popularidad_promedio",
                            "permanencia_dias",
                        ]
                    ]
                    .copy()
                    .reset_index(
                        drop=True
                    )
                )

                tabla.columns = [
                    "Artista",
                    "Perfil",
                    "Apariciones",
                    "Rank prom.",
                    "Popularidad",
                    "Permanencia",
                ]

                tabla[
                    "Perfil"
                ] = (
                    tabla[
                        "Perfil"
                    ]
                    .apply(
                        perfil_amigable
                    )
                )

                tabla[
                    "Rank prom."
                ] = (
                    tabla[
                        "Rank prom."
                    ]
                    .round(2)
                )

                tabla[
                    "Popularidad"
                ] = (
                    tabla[
                        "Popularidad"
                    ]
                    .round(2)
                )

                # =================================================
                # MÁXIMO CINCO FILAS VISIBLES
                # =================================================

                filas_visibles = min(
                    len(tabla),
                    5
                )

                altura_tabla = (
                    48
                    +
                    filas_visibles * 42
                )

                evento_tabla = (
                    st.dataframe(
                        tabla,
                        hide_index=True,
                        use_container_width=True,
                        height=altura_tabla,
                        on_select="rerun",
                        selection_mode="single-row",
                        key=(
                            f"tabla_artistas_"
                            f"{st.session_state['version_tabla']}"
                        ),
                    )
                )

                filas_seleccionadas = (
                    evento_tabla
                    .selection
                    .rows
                )

                if filas_seleccionadas:

                    posicion = (
                        filas_seleccionadas[
                            0
                        ]
                    )

                    artista_seleccionado = (
                        tabla.iloc[
                            posicion
                        ][
                            "Artista"
                        ]
                    )

    # ========================================================
    # SI TODAVÍA NO SELECCIONA
    # ========================================================

    if (
        not resultados.empty
        and
        artista_seleccionado is None
    ):

        st.write("")

        caja_aviso(
            """
            <strong>Seleccione un artista de la tabla.</strong>
            Puede desplazarse dentro de la lista si existen más
            resultados. Al seleccionar uno, la aplicación mostrará
            automáticamente su información.
            """,
            tipo="azul",
        )

    # ========================================================
    # DETALLE AUTOMÁTICO
    # ========================================================

    if artista_seleccionado is not None:

        mostrar_detalle_artista(
            artista_seleccionado
        )


# ============================================================
# PÁGINA 4 - MONITOREO TÉCNICO
# ============================================================

def pagina_monitoreo():

    entrar_pagina(
        "monitoreo"
    )

    st.title(
        "Monitoreo técnico"
    )

    st.caption(
        "Vista administrativa de la versión activa "
        "del modelo y sus indicadores de referencia."
    )

    columnas = (
        st.columns(6)
    )

    datos = [

        (
            "Estado",
            "Operativo",
            GREEN,
        ),

        (
            "Modelo",
            "MLP",
            PURPLE,
        ),

        (
            "Artistas",
            metricas[
                "n_artistas"
            ],
            GREEN,
        ),

        (
            "Accuracy",
            f"{metricas['accuracy']:.3f}",
            BLUE,
        ),

        (
            "AUC",
            f"{metricas['auc']:.3f}",
            GREEN,
        ),

        (
            "F1",
            f"{metricas['f1_score']:.3f}",
            GREEN,
        ),
    ]

    for columna, dato in zip(
        columnas,
        datos
    ):

        with columna:

            tarjeta_metrica(
                dato[0],
                dato[1],
                dato[2],
            )

    st.write("")

    caja_aviso(
        """
        <strong>Nota metodológica:</strong>
        el clasificador MLP utiliza internamente una etiqueta
        técnica binaria de alta/menor señal derivada de los perfiles.

        Para el usuario final se priorizan los cuatro perfiles,
        porque entregan una interpretación más detallada del
        comportamiento de cada artista.
        """,
        tipo="azul",
    )

    st.write("")

    col1, col2 = (
        st.columns(2)
    )

    # --------------------------------------------------------
    # MATRIZ DE CONFUSIÓN
    # --------------------------------------------------------

    with col1:

        with st.container(
            border=True
        ):

            titulo_tarjeta(
                "Matriz de confusión"
            )

            matriz = (
                pd.DataFrame(
                    [
                        [
                            metricas[
                                "verdaderos_negativos"
                            ],

                            metricas[
                                "falsos_positivos"
                            ],
                        ],

                        [
                            metricas[
                                "falsos_negativos"
                            ],

                            metricas[
                                "verdaderos_positivos"
                            ],
                        ],
                    ],

                    index=[
                        "Real: menor señal",
                        "Real: alta señal",
                    ],

                    columns=[
                        "Pred.: menor",
                        "Pred.: alta",
                    ],
                )
            )

            st.dataframe(
                matriz,
                use_container_width=True,
            )

    # --------------------------------------------------------
    # CONFIGURACIÓN
    # --------------------------------------------------------

    with col2:

        with st.container(
            border=True
        ):

            titulo_tarjeta(
                "Configuración del modelo"
            )

            configuracion = (
                pd.DataFrame(
                    {
                        "Parámetro": [
                            "Arquitectura",
                            "Dropout",
                            "Learning rate",
                            "Umbral",
                            "Variables",
                            "Clusters",
                        ],

                        "Valor": [
                            "16 → 8",
                            "0,30",
                            "0,001",
                            metricas[
                                "umbral_clasificacion"
                            ],
                            metricas[
                                "n_variables"
                            ],
                            metadata[
                                "numero_clusters"
                            ],
                        ],
                    }
                )
            )

            st.dataframe(
                configuracion,
                hide_index=True,
                use_container_width=True,
            )

    st.write("")

    # --------------------------------------------------------
    # SHAP
    # --------------------------------------------------------

    with st.container(
        border=True
    ):

        titulo_tarjeta(
            "Importancia global de variables del clasificador"
        )

        st.caption(
            "Permite observar qué variables presentan "
            "mayor influencia global sobre la clasificación técnica."
        )

        shap = (
            shap_global
            .copy()
        )

        shap[
            "Variable visible"
        ] = (
            shap[
                "Variable"
            ]
            .apply(
                nombre_variable_amigable
            )
        )

        grafico_shap = (

            alt.Chart(
                shap
            )

            .mark_bar(
                color=GREEN
            )

            .encode(

                x=alt.X(
                    "Importancia_SHAP:Q",
                    title="Importancia promedio absoluta",
                ),

                y=alt.Y(
                    "Variable visible:N",
                    title=None,
                    sort="-x",
                ),

                tooltip=[
                    alt.Tooltip(
                        "Variable visible:N",
                        title="Variable",
                    ),

                    alt.Tooltip(
                        "Importancia_SHAP:Q",
                        title="Importancia",
                        format=".4f",
                    ),
                ],
            )

            .properties(
                height=300
            )
        )

        st.altair_chart(
            grafico_shap,
            use_container_width=True,
        )

    st.write("")

    # --------------------------------------------------------
    # MÉTRICAS ADICIONALES
    # --------------------------------------------------------

    with st.expander(
        "Ver métricas adicionales"
    ):

        adicionales = (
            pd.DataFrame(
                {
                    "Métrica": [
                        "Precision",
                        "Recall",
                        "Accuracy",
                        "F1-score",
                        "AUC",
                    ],

                    "Valor": [
                        metricas[
                            "precision"
                        ],
                        metricas[
                            "recall"
                        ],
                        metricas[
                            "accuracy"
                        ],
                        metricas[
                            "f1_score"
                        ],
                        metricas[
                            "auc"
                        ],
                    ],
                }
            )
        )

        adicionales[
            "Valor"
        ] = (
            adicionales[
                "Valor"
            ]
            .round(4)
        )

        st.dataframe(
            adicionales,
            hide_index=True,
            use_container_width=True,
        )

    st.write("")

    caja_aviso(
        """
        <strong>Importante:</strong>
        estas métricas evalúan la capacidad del modelo de reproducir
        la etiqueta técnica construida a partir de los perfiles.

        No constituyen una validación externa contra ventas de
        entradas o asistencia real, ya que esas variables no se
        encuentran disponibles en el dataset.
        """
    )


# ============================================================
# NAVEGACIÓN
# ============================================================

inicio = (
    st.Page(
        pagina_inicio,
        title="Inicio",
        icon=":material/home:",
        default=True,
    )
)

resumen = (
    st.Page(
        pagina_resumen,
        title="Resumen general",
        icon=":material/dashboard:",
    )
)

explorador = (
    st.Page(
        pagina_explorador,
        title="Explorar artistas",
        icon=":material/search:",
    )
)

monitoreo = (
    st.Page(
        pagina_monitoreo,
        title="Monitoreo técnico",
        icon=":material/monitoring:",
    )
)


navegacion = (
    st.navigation(
        [
            inicio,
            resumen,
            explorador,
            monitoreo,
        ]
    )
)


# ============================================================
# PIE SIDEBAR
# ============================================================

st.sidebar.markdown(
    "---"
)

st.sidebar.html(
    """
    <div style="
        color:#B3B3B3;
        font-size:12px;
        line-height:1.6;
    ">
        Los perfiles presentados apoyan decisiones de
        programación musical y no representan una
        predicción directa de convocatoria.
    </div>
    """
)


# ============================================================
# EJECUTAR
# ============================================================

navegacion.run()