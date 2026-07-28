
import streamlit as st
import base64
import glob
from pathlib import Path
from textwrap import dedent
from banderas import cargar_banderas, obtener_bandera_html
from data_loader import (
    load_match_index,
    load_match_package,
    get_matches_by_stage,
    MatchDataError
)

from app_config import (
    STAGE_CONFIG,
    get_team_name_es
)
from match_components import (
    render_match_hero,
    render_match_story,
    render_share_of_voice,
    render_emotional_climate,
    render_protagonists,
    render_featured_tweets,
    render_final_radiography
)
from match_charts import render_twitter_momentum


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

ASSETS_DIR = (
    PROJECT_ROOT
    / "assets"
)

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Mundial Rusia 2018 desde Twitter",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ESTILOS GENERALES
# =========================================================

st.markdown(
    dedent("""
    <style>
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    div[data-testid="stVerticalBlock"] { gap: 0rem; }
    body { background-color: #06131d; }

    .btn-custom {
        display: inline-block;
        background-color: #87CEEB;
        color: #003366 !important;
        padding: 15px 45px;
        border-radius: 12px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 19px;
        margin-top: 30px;
        transition: 0.25s;
        box-shadow: 0 5px 18px rgba(0,0,0,0.40);
    }
    .btn-custom:hover { background-color: #B0E2FF; transform: translateY(-3px); }

    .btn-volver {
        display: inline-block;
        color: #87CEEB !important;
        text-decoration: none !important;
        font-size: 16px;
        font-weight: bold;
        margin-top: 35px;
    }

    .pagina {
        min-height: 100vh;
        box-sizing: border-box;
        background: radial-gradient(circle at top, #194564 0%, #081a28 48%, #020609 100%);
        color: white;
        padding: 65px 7%;
    }

    .grilla-fases { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
    .tarjeta-fase {
        display: block; padding: 32px 20px; border-radius: 18px; text-align: center;
        text-decoration: none !important; background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.14); transition: 0.25s; color: white !important;
    }
    .tarjeta-fase:hover { background: rgba(135,206,235,0.18); border-color: #87CEEB; transform: translateY(-5px); }
    .tarjeta-fase.activa { background: rgba(135,206,235,0.22); border-color: #87CEEB; }

    .seccion-partidos { margin-top: 55px; }
    .titulo-partidos { color: white; text-align: center; font-size: 30px; font-weight: 800; margin-bottom: 28px; }
    .grilla-partidos { display: grid; grid-template-columns: repeat(2, minmax(280px, 1fr)); gap: 18px; max-width: 1000px; margin: 0 auto; }
    .tarjeta-partido {
        min-height: 90px; display: flex; justify-content: center; align-items: center; box-sizing: border-box; padding: 22px;
        color: white !important; text-decoration: none !important; text-align: center; font-size: 21px; font-weight: 750;
        background: rgba(255,255,255,0.075); border: 1px solid rgba(255,255,255,0.14); border-radius: 16px; transition: 0.25s;
    }
    .tarjeta-partido:hover { color: #87CEEB !important; background: rgba(135,206,235,0.15); border-color: #87CEEB; transform: translateY(-3px); }

    .pantalla-partido { min-height: 100vh; box-sizing: border-box; padding: 65px 7%; color: white; background: radial-gradient(circle at top, #194564 0%, #081a28 48%, #020609 100%); }
    .nombre-partido-seleccionado { margin-top: 120px; color: white; text-align: center; font-size: 52px; font-weight: 850; }

    @media (max-width: 700px) {
        .grilla-partidos { grid-template-columns: 1fr; }
        .nombre-partido-seleccionado { font-size: 38px; }
    }
    </style>
    """),
    unsafe_allow_html=True
)

# =========================================================
# CARGAR IMÁGENES
# =========================================================

def cargar_imagen_base64(patrones):

    for patron in patrones:

        archivos = glob.glob(
            patron,
            recursive=True
        )

        if archivos:

            ruta = archivos[0]
            extension = ruta.lower().split(".")[-1]

            if extension == "jpg":
                extension = "jpeg"

            if extension in ["webp", "png", "jpeg"]:

                with open(ruta, "rb") as archivo:

                    imagen_base64 = base64.b64encode(
                        archivo.read()
                    ).decode()

                return imagen_base64, extension

    return "", "jpeg"


# Imagen de la portada: pelota y copa

img_b64, ext_img = cargar_imagen_base64([
    str(
        ASSETS_DIR
        / "portada.*"
    )
])


# Imagen de la pantalla de fases: estadio

estadio_b64, ext_estadio = cargar_imagen_base64([
    str(
        ASSETS_DIR
        / "estadio.*"
    )
])
banderas_img = cargar_banderas()
# =========================================================
# CARGAR ÍNDICE DE LOS 16 PARTIDOS
# =========================================================

try:

    match_index = load_match_index()

except MatchDataError as error:

    st.error(
        "No fue posible cargar los datos "
        "de los partidos."
    )

    st.code(
        str(error)
    )

    st.stop()
# =========================================================
# NAVEGACIÓN Y CONTENIDO
# =========================================================

pantalla = st.query_params.get("p", "inicio")
fase_activa = st.query_params.get("fase", "")
partido_activo = st.query_params.get("partido", "")

if pantalla == "inicio":
    fondo_css = f"background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.7)), url('data:image/{ext_img};base64,{img_b64}');" if img_b64 else "background: #06131d;"
    st.markdown(f"""
        <div style="{fondo_css} height: 100vh; background-size: cover; background-position: center; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; color: white; width: 100%;">
            <div style="max-width: 900px; padding: 20px;">
                <div style="letter-spacing: 4px; font-size: 14px; opacity: 0.8; margin-bottom: 20px;">SEMINARIO FIUBA 9216 • TWITTER MINING</div>
                <h1 style="font-size: clamp(40px, 8vw, 75px); font-weight: 850; margin: 0; line-height: 1.1;">MUNDIAL RUSIA 2018</h1>
                <h2 style="font-size: clamp(20px, 4vw, 40px); font-weight: 300; margin-bottom: 30px;">DESDE TWITTER</h2>
                <p style="font-size: 19px; opacity: 0.9;">La historia de las fases finales reconstruida a partir de más de 500.000 tweets.</p>
                <a href="?p=fases" target="_self" class="btn-custom">Explorar partidos</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif pantalla == "fases":
      # =====================================================
    # ESTÉTICA DE LA PANTALLA DE FASES
    # =====================================================

      if estadio_b64:

        fondo_fases = (
            "linear-gradient("
            "rgba(0, 0, 0, 0.28), "
            "rgba(0, 0, 0, 0.65)"
            "), "
            f"url('data:image/{ext_estadio};base64,{estadio_b64}')"
        )

      else:

        fondo_fases = (
            "linear-gradient("
            "#2d2b2a, "
            "#121212"
            ")"
        )

      st.markdown(
        dedent(f"""
        <style>

        /* FONDO CON LA FOTO DEL ESTADIO */

        .pagina {{
            min-height: 100vh;
            box-sizing: border-box;

            background-image: {fondo_fases};
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;

            color: #20272d;
            padding: 58px 6%;
        }}


        /* TÍTULO PRINCIPAL */

        .pagina > div:first-child h1 {{
            color: #ffffff !important;
            font-size: 48px !important;
            font-weight: 800 !important;
            letter-spacing: -1px;
            text-shadow: 0 3px 14px rgba(0, 0, 0, 0.55);
        }}

        .pagina > div:first-child p {{
            color: rgba(255, 255, 255, 0.88) !important;
            font-size: 18px !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.50);
        }}


        /* TARJETAS DE LAS FASES */

        .grilla-fases {{
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(190px, 1fr));

            gap: 16px;
            max-width: 1250px;
            margin: 0 auto;
        }}

        .tarjeta-fase {{
            min-height: 125px;
            box-sizing: border-box;

            display: flex;
            flex-direction: column;
            justify-content: center;

            padding: 24px 18px;
            border-radius: 12px;

            text-align: center;
            text-decoration: none !important;

            background: rgba(255, 255, 255, 0.90);
            border: 1px solid rgba(95, 69, 62, 0.20);

            box-shadow:
                0 8px 22px rgba(47, 39, 32, 0.11);

            backdrop-filter: blur(5px);
            transition: 0.22s ease;
        }}

        .tarjeta-fase h3 {{
            color: #792d3b !important;
            font-size: 19px;
            font-weight: 800;
            text-transform: uppercase;
            line-height: 1.2;
            margin: 0 0 10px 0;
        }}

        .tarjeta-fase p {{
            color: #756a63 !important;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin: 0;
        }}

        .tarjeta-fase:hover {{
            background: rgba(255, 255, 255, 0.98);
            border-color: #9e3545;

            box-shadow:
                0 12px 28px rgba(47, 39, 32, 0.16);

            transform: translateY(-3px);
        }}

        .tarjeta-fase.activa {{
            background: rgba(255, 255, 255, 0.98);
            border: 2px solid #9e3545;

            box-shadow:
                0 10px 25px rgba(85, 34, 43, 0.18);
        }}


        /* TÍTULO DE LA FASE SELECCIONADA */

        .titulo-partidos {{
            color: #792d3b !important;
            text-align: left;
            font-size: 24px;
            font-weight: 850;
            text-transform: uppercase;

            margin-bottom: 22px;
            padding-left: 15px;

            border-left: 4px solid #c0a052;
        }}


        /* TARJETAS DE LOS PARTIDOS */

        .grilla-partidos {{
            display: grid;
            grid-template-columns:
                repeat(2, minmax(280px, 1fr));

            gap: 14px;
            max-width: 1100px;
            margin: 0 auto;
        }}

                .tarjeta-partido {{
            min-height: 72px;
            box-sizing: border-box;

            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: 20px;

            padding: 18px 22px;
            border-radius: 10px;

            color: #27323a !important;
            text-decoration: none !important;
            text-align: center;

            font-size: 18px;
            font-weight: 750;

            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(95, 69, 62, 0.18);

            box-shadow:
                0 6px 18px rgba(47, 39, 32, 0.09);

            backdrop-filter: blur(5px);
            transition: 0.20s ease;
        }}

        .lado-partido {{
            display: flex;
            align-items: center;
            gap: 10px;
            color: #27323a;
        }}

        .lado-izquierdo {{
            justify-content: flex-end;
            text-align: right;
        }}

        .lado-derecho {{
            justify-content: flex-start;
            text-align: left;
        }}

        .bandera-partido {{
            width: 42px;
            height: 28px;
            object-fit: cover;
            flex-shrink: 0;

            border-radius: 3px;
            border: 1px solid rgba(0, 0, 0, 0.12);

            box-shadow:
                0 2px 6px rgba(0, 0, 0, 0.22);
        }}

        .versus-partido {{
            color: #9e3545;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: 1.5px;
        }}

        .tarjeta-partido:hover {{
            color: #8c2939 !important;
            background: #ffffff;
            border-color: #9e3545;

            box-shadow:
                0 9px 22px rgba(47, 39, 32, 0.14);

            transform: translateY(-2px);
        }}


        /* BOTÓN PARA VOLVER */

        .pagina .btn-volver {{
            color: #792d3b !important;
            margin-top: 38px;
        }}

        .pagina .btn-volver:hover {{
            color: #4f1822 !important;
        }}


        /* VERSIÓN PARA CELULAR */

        @media (max-width: 700px) {{

            .pagina {{
                padding: 42px 20px;
                background-attachment: scroll;
            }}

            .pagina > div:first-child h1 {{
                font-size: 36px !important;
            }}

            .grilla-partidos {{
                grid-template-columns: 1fr;
            }}

            .tarjeta-fase {{
                min-height: 105px;
            }}
            .tarjeta-partido {{
    gap: 10px;
    padding-left: 12px;
    padding-right: 12px;
    font-size: 15px;
}}

            .bandera-partido {{
                width: 34px;
                height: 23px;
            }}
        }}

        </style>
        """).strip(),
        unsafe_allow_html=True
    )
            # =====================================================
      # FASES Y PARTIDOS DESDE index.json
      # =====================================================

      fases = {}

      for fase_slug, fase_config in (
          STAGE_CONFIG.items()
      ):

          partidos_de_la_fase = (
              get_matches_by_stage(
                  fase_config[
                      "stage_key"
                  ]
              )
          )

          partidos_visibles = []

          for match_record in (
              partidos_de_la_fase
          ):

              partidos_visibles.append(
                  (
                      match_record["slug"],

                      get_team_name_es(
                          match_record["team1"]
                      ),

                      get_team_name_es(
                          match_record["team2"]
                      )
                  )
              )

          fases[fase_slug] = {
              "nombre":
                  fase_config["nombre"],

              "cantidad":
                  fase_config["cantidad"],

              "partidos":
                  partidos_visibles
          }
      tarjetas_fases = ""
      for slug, datos in fases.items():
        clase = "tarjeta-fase activa" if fase_activa == slug else "tarjeta-fase"
        tarjetas_fases += (
            f'<a '
            f'href="?p=fases&amp;fase={slug}" '
            f'target="_self" '
            f'class="{clase}">'
                f'<h3>{datos["nombre"]}</h3>'
                f'<p>{datos["cantidad"]}</p>'
            f'</a>'
        )

      seccion_partidos = ""

      if fase_activa in fases:

          partidos_html = ""

          for partido_id, equipo1, equipo2 in fases[fase_activa]["partidos"]:

            bandera1 = obtener_bandera_html(
                equipo1,
                banderas_img
            )

            bandera2 = obtener_bandera_html(
                equipo2,
                banderas_img
            )

            partidos_html += (
                f'<a '
                f'href="?p=partido&amp;fase={fase_activa}&amp;partido={partido_id}" '
                f'target="_self" '
                f'class="tarjeta-partido">'

                    f'<span class="lado-partido lado-izquierdo">'
                        f'{bandera1}'
                        f'<span>{equipo1}</span>'
                    f'</span>'

                    f'<span class="versus-partido">'
                        f'VS'
                    f'</span>'

                    f'<span class="lado-partido lado-derecho">'
                        f'<span>{equipo2}</span>'
                        f'{bandera2}'
                    f'</span>'

                f'</a>'
            )

            seccion_partidos = (
            '<div class="seccion-partidos">'
                f'<div class="titulo-partidos">'
                    f'{fases[fase_activa]["nombre"]}'
                '</div>'
                f'<div class="grilla-partidos">'
                    f'{partidos_html}'
                '</div>'
            '</div>'
        )

      html_fases = (
        '<div class="pagina">'
            '<div style="text-align:center; margin-bottom:50px;">'
                '<h1 style="color:white; font-size:50px; margin-bottom:12px;">'
                    'Elegí una instancia'
                '</h1>'
                '<p style="color:#aec3d0; font-size:18px;">'
                    'Explorá cómo se vivieron los partidos decisivos.'
                '</p>'
            '</div>'
            f'<div class="grilla-fases">{tarjetas_fases}</div>'
            f'{seccion_partidos}'
            '<a href="?p=inicio" target="_self" class="btn-volver">'
                '← Volver al inicio'
            '</a>'
        '</div>'
    )

      st.markdown(
        html_fases,
        unsafe_allow_html=True
    )

elif pantalla == "partido":
        # =====================================================
    # CARGAR EL PARTIDO SELECCIONADO
    # =====================================================

    try:

        match_data = load_match_package(
            partido_activo
        )

    except MatchDataError as error:

        st.error(
            "No fue posible cargar "
            "el partido seleccionado."
        )

        st.code(
            str(error)
        )

        st.markdown(
            (
                f'<a '
                f'href="?p=fases&amp;fase={fase_activa}" '
                f'target="_self" '
                f'class="btn-volver">'
                f'← Volver a los partidos'
                f'</a>'
            ),
            unsafe_allow_html=True
        )

        st.stop()

    render_match_hero(
        match_data=match_data,
        banderas_img=banderas_img,
        fase_slug=fase_activa
    )
    render_match_story(
        match_data=match_data
    )
    render_twitter_momentum(
    match_data,
    banderas_img
)
    render_share_of_voice(
    match_data,
    banderas_img
)
    render_emotional_climate(
    match_data,
    banderas_img
)
    render_protagonists(
    match_data,
    banderas_img
)
    render_featured_tweets(
    match_data
)
    render_final_radiography(
    match_data
)
