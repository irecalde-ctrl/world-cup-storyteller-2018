
import streamlit as st
from html import escape
from textwrap import dedent

from app_config import get_team_name_es
from banderas import obtener_bandera_html


def format_number_es(value):

    return (
        f"{int(value):,}"
        .replace(",", ".")
    )


def render_match_hero(
    match_data,
    banderas_img,
    fase_slug
):

    hero = match_data["hero"]
    quality = match_data["data_quality"]

    team1 = hero["team1"]
    team2 = hero["team2"]

    team1_name = get_team_name_es(
        team1["name"]
    )

    team2_name = get_team_name_es(
        team2["name"]
    )

    winner_name = get_team_name_es(
        hero["winner"]
    )

    team1_flag = obtener_bandera_html(
        team1_name,
        banderas_img,
        css_class="hero-flag"
    )

    team2_flag = obtener_bandera_html(
        team2_name,
        banderas_img,
        css_class="hero-flag"
    )

    tweet_count = format_number_es(
        hero["tweet_count"]
    )

    stage_label = hero["stage"]["label"]
    date_display = hero["date"]["display"]

    team1_score = team1.get(
        "score",
        "-"
    )

    team2_score = team2.get(
        "score",
        "-"
    )

    st.markdown(
        dedent("""
        <style>

        .match-hero {
            position: relative;
            min-height: 92vh;
            box-sizing: border-box;
            overflow: hidden;

            display: flex;
            flex-direction: column;
            justify-content: center;

            padding: 48px 7% 72px;

            color: #ffffff;

            background:
                radial-gradient(
                    circle at 50% 20%,
                    rgba(38, 91, 126, 0.72) 0%,
                    rgba(8, 27, 41, 0.96) 48%,
                    #020609 100%
                );
        }

        .match-hero::before {
            content: "";
            position: absolute;
            inset: 0;

            background:
                linear-gradient(
                    115deg,
                    rgba(213, 43, 30, 0.10),
                    transparent 34%
                ),
                linear-gradient(
                    245deg,
                    rgba(29, 78, 158, 0.12),
                    transparent 34%
                );

            pointer-events: none;
        }

        .hero-worldcup-line {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 9px;

            background:
                linear-gradient(
                    90deg,
                    #d52b1e 0%,
                    #d52b1e 34%,
                    #1d4e9e 34%,
                    #1d4e9e 68%,
                    #d4af37 68%,
                    #d4af37 100%
                );
        }

        .hero-content {
            position: relative;
            z-index: 2;

            width: 100%;
            max-width: 1180px;
            margin: 0 auto;
        }

        .hero-back {
            display: inline-flex;
            align-items: center;
            margin-bottom: 55px;
            padding: 11px 16px;

            color: #ffffff !important;
            text-decoration: none !important;

            background: #081a28;
            border: 1px solid #d4af37;
            border-radius: 9px;

            box-shadow:
                0 6px 18px rgba(0, 0, 0, 0.25);

            font-size: 15px;
            font-weight: 750;
        }

        .hero-back:hover {
            color: #ffffff !important;
            background: #792d3b;
        }

        .hero-kicker {
            text-align: center;
            margin-bottom: 36px;

            color: #d4af37;

            font-size: 13px;
            font-weight: 850;
            letter-spacing: 2.2px;
            text-transform: uppercase;
        }

        .hero-scoreboard {
            display: grid;
            grid-template-columns:
                minmax(220px, 1fr)
                minmax(210px, 0.65fr)
                minmax(220px, 1fr);

            align-items: center;
            gap: 34px;
        }

        .hero-team {
            display: flex;
            flex-direction: column;
            align-items: center;

            text-align: center;
        }

        .hero-flag {
            width: 112px;
            height: 74px;

            object-fit: cover;

            border-radius: 7px;
            border: 1px solid rgba(255,255,255,0.28);

            box-shadow:
                0 12px 30px rgba(0,0,0,0.34);
        }

        .hero-team-name {
            margin-top: 20px;

            color: #ffffff;

            font-size: clamp(27px, 3vw, 43px);
            font-weight: 850;
            line-height: 1.05;
        }

        .hero-result {
            text-align: center;
        }

        .hero-score {
            color: #ffffff;

            font-size: clamp(65px, 9vw, 112px);
            font-weight: 900;
            letter-spacing: -6px;
            line-height: 0.95;

            text-shadow:
                0 8px 30px rgba(0,0,0,0.32);
        }

        .hero-score-separator {
            color: rgba(255,255,255,0.45);
            margin: 0 14px;
        }

        .hero-winner {
            margin-top: 22px;

            color: rgba(255,255,255,0.74);

            font-size: 13px;
            font-weight: 750;
            letter-spacing: 1.1px;
            text-transform: uppercase;
        }

        .hero-metrics {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 12px;

            margin-top: 58px;
        }

        .hero-pill {
            padding: 11px 17px;

            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.16);

            background: rgba(255,255,255,0.075);

            color: rgba(255,255,255,0.86);

            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }

        @media (max-width: 760px) {

            .match-hero {
                min-height: auto;
                padding:
                    34px 22px
                    60px;
            }

            .hero-back {
                margin-bottom: 38px;
            }

            .hero-scoreboard {
                grid-template-columns:
                    1fr 0.8fr 1fr;

                gap: 10px;
            }

            .hero-flag {
                width: 72px;
                height: 48px;
            }

            .hero-team-name {
                font-size: 20px;
            }

            .hero-score {
                font-size: 52px;
                letter-spacing: -4px;
            }

            .hero-score-separator {
                margin: 0 5px;
            }

            .hero-winner {
                font-size: 10px;
            }

            .hero-metrics {
                margin-top: 42px;
            }
        }

        </style>
        """),
        unsafe_allow_html=True
    )

    hero_html = f"""
    <section class="match-hero">

        <div class="hero-worldcup-line"></div>

        <div class="hero-content">

            <a
                href="?p=fases&amp;fase={escape(fase_slug)}"
                target="_self"
                class="hero-back"
            >
                ← Volver a la fase
            </a>

            <div class="hero-kicker">
                {escape(stage_label)}
                &nbsp;•&nbsp;
                {escape(date_display)}
            </div>

            <div class="hero-scoreboard">

                <div class="hero-team">
                    {team1_flag}

                    <div class="hero-team-name">
                        {escape(team1_name)}
                    </div>
                </div>

                <div class="hero-result">

                    <div class="hero-score">
                        {team1_score}
                        <span class="hero-score-separator">-</span>
                        {team2_score}
                    </div>

                    <div class="hero-winner">
                        Ganador: {escape(winner_name)}
                    </div>
                </div>

                <div class="hero-team">
                    {team2_flag}

                    <div class="hero-team-name">
                        {escape(team2_name)}
                    </div>
                </div>

            </div>

            <div class="hero-metrics">

                <div class="hero-pill">
                    {tweet_count} tuits analizados
                </div>

                <div class="hero-pill">
                    {escape(quality["label"])}
                </div>

            </div>

        </div>

    </section>
    """

    st.html(
    dedent(
        hero_html
    ).strip()
)
def render_match_story(
    match_data
):

    story = match_data["story"]

    story_blocks = [
        story["preview"],
        story["social_climate"],
        story["turning_point"],
        story["outcome"]
    ]

    story_rows = ""

    for position, block in enumerate(
        story_blocks,
        start=1
    ):

        story_rows += f"""
        <div class="story-row">

            <div class="story-chapter">

                <span class="story-number">
                    {position:02d}
                </span>

                <h3>
                    {escape(block["title"])}
                </h3>

            </div>

            <div class="story-text">
                {escape(block["text"])}
            </div>

        </div>
        """

    coverage_note = story.get(
        "coverage_note",
        ""
    )

    story_html = f"""
    <section class="match-story">

        <div class="story-container">

            <div class="story-heading">

                <div class="story-eyebrow">
                    LA HISTORIA DEL PARTIDO
                </div>

                <h2>
                    Así lo vivió Twitter
                </h2>

                <p>
                    Una reconstrucción narrativa a partir
                    de la conversación social.
                </p>

            </div>

            <div class="story-article">
                {story_rows}
            </div>

            <div class="story-note">
                {escape(coverage_note)}
            </div>

        </div>

    </section>
    """

    st.html(
        """
        <style>

        .match-story {
            box-sizing: border-box;

            padding: 105px 7% 115px;

            background:
                linear-gradient(
                    180deg,
                    #f5f1e9 0%,
                    #fffdf9 100%
                );

            color: #1d252b;
        }

        .story-container {
            max-width: 1040px;
            margin: 0 auto;
        }

        .story-heading {
            max-width: 760px;
            margin-bottom: 72px;
        }

        .story-eyebrow {
            margin-bottom: 17px;

            color: #9e3545;

            font-size: 13px;
            font-weight: 900;
            letter-spacing: 2.2px;
            text-transform: uppercase;
        }

        .story-heading h2 {
            margin: 0 0 18px;

            color: #20272d;

            font-size: clamp(38px, 5vw, 63px);
            font-weight: 900;
            letter-spacing: -2px;
            line-height: 1.02;
        }

        .story-heading p {
            margin: 0;

            color: #706d68;

            font-size: 19px;
            line-height: 1.6;
        }

        .story-article {
            border-top:
                1px solid rgba(32,39,45,0.17);
        }

        .story-row {
            display: grid;

            grid-template-columns:
                minmax(210px, 0.68fr)
                minmax(0, 1.7fr);

            gap: 55px;

            padding: 38px 0 42px;

            border-bottom:
                1px solid rgba(32,39,45,0.17);
        }

        .story-chapter {
            display: grid;

            grid-template-columns:
                42px 1fr;

            gap: 16px;
            align-items: start;
        }

        .story-number {
            color: #c0a052;

            font-size: 12px;
            font-weight: 900;
            letter-spacing: 1px;
        }

        .story-chapter h3 {
            margin: -4px 0 0;

            color: #792d3b;

            font-size: 21px;
            font-weight: 850;
            line-height: 1.18;
        }

        .story-text {
            color: #343a3e;

            font-family:
                Georgia,
                "Times New Roman",
                serif;

            font-size: 20px;
            line-height: 1.78;
        }

        .story-note {
            margin-top: 28px;

            color: #85817b;

            font-size: 12px;
            line-height: 1.5;
            font-style: italic;
        }

        @media (max-width: 760px) {

            .match-story {
                padding:
                    75px 24px
                    85px;
            }

            .story-heading {
                margin-bottom: 50px;
            }

            .story-row {
                grid-template-columns: 1fr;
                gap: 22px;

                padding: 30px 0 34px;
            }

            .story-text {
                font-size: 18px;
                line-height: 1.68;
            }
        }

        </style>
        """
    )

    st.html(
        dedent(
            story_html
        ).strip()
    )

# =========================================================
# QUIÉN DOMINÓ LA CONVERSACIÓN
# =========================================================

from banderas import obtener_bandera_html
from app_config import get_team_name_es
from chart_config import get_match_colors



def build_share_interpretation_es(
    team1_es,
    team2_es,
    percentage1,
    percentage2
):

    difference = abs(
        percentage1
        -
        percentage2
    )

    percentage1_es = (
        f"{percentage1:.1f}"
        .replace(".", ",")
    )

    percentage2_es = (
        f"{percentage2:.1f}"
        .replace(".", ",")
    )

    difference_es = (
        f"{difference:.1f}"
        .replace(".", ",")
    )

    if difference < 0.05:

        return (
            f"{team1_es} y {team2_es} tuvieron "
            "la misma participación en la conversación, "
            f"con un {percentage1_es}% de las menciones "
            "para cada equipo."
        )

    if percentage1 > percentage2:

        return (
            f"{team1_es} dominó la conversación con el "
            f"{percentage1_es}% de las menciones, una "
            f"diferencia de {difference_es} puntos "
            f"porcentuales respecto de {team2_es}."
        )

    return (
        f"{team2_es} dominó la conversación con el "
        f"{percentage2_es}% de las menciones, una "
        f"diferencia de {difference_es} puntos "
        f"porcentuales respecto de {team1_es}."
    )


def render_share_of_voice(
    match_data,
    banderas_img
):
    """
    Muestra el Share of Voice como una barra horizontal
    dividida entre ambos equipos.
    """

    share = match_data.get(
        "share_of_voice",
        {}
    )

    quality = match_data.get(
        "data_quality",
        {}
    )

    team1_data = share.get(
        "team1",
        {}
    )

    team2_data = share.get(
        "team2",
        {}
    )

    team1 = team1_data.get(
        "name",
        ""
    )

    team2 = team2_data.get(
        "name",
        ""
    )

    team1_es = get_team_name_es(
        team1
    )

    team2_es = get_team_name_es(
        team2
    )

    # -----------------------------------------------------
    # SECCIÓN SIN INFORMACIÓN SOCIAL
    # -----------------------------------------------------

    if (
    not quality.get(
        "show_social_analysis",
        False
    )
    or not share.get(
        "available",
        False
    )
):

      render_unavailable_section(
        kicker="LA CONVERSACIÓN",
        title="Quién dominó la conversación",
        message=(
            "No hay suficientes menciones para comparar "
            "la conversación entre ambos equipos."
        ),
        theme="light"
    )

      return

    # -----------------------------------------------------
    # DATOS
    # -----------------------------------------------------

    percentage1 = float(
        team1_data.get(
            "percentage",
            0
        )
    )

    percentage2 = float(
        team2_data.get(
            "percentage",
            0
        )
    )

    mentions1 = int(
        team1_data.get(
            "mentions",
            0
        )
    )

    mentions2 = int(
        team2_data.get(
            "mentions",
            0
        )
    )

    color1, color2 = get_match_colors(
        match_data.get(
            "match",
            ""
        ),
        team1,
        team2
    )

    flag1 = obtener_bandera_html(
        team1_es,
        banderas_img,
        css_class="sov-flag"
    )

    flag2 = obtener_bandera_html(
        team2_es,
        banderas_img,
        css_class="sov-flag"
    )

    interpretation = build_share_interpretation_es(
        team1_es,
        team2_es,
        percentage1,
        percentage2
    )

    # -----------------------------------------------------
    # HTML
    # -----------------------------------------------------

    share_html = f"""
    <style>

        .sov-section {{
            width: 100%;
            box-sizing: border-box;
            background: transparent;
            padding: 75px 7% 80px 7%;
        }}

        .sov-container {{
            width: min(980px, 100%);
            margin: 0 auto;
        }}

        .sov-kicker {{
            color: #C5253D;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2.2px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }}

        .sov-title {{
            color: #081A28;
            font-size: clamp(31px, 4vw, 48px);
            line-height: 1.05;
            font-weight: 850;
            margin: 0 0 42px 0;
        }}

        .sov-team-row {{
            display: grid;
            grid-template-columns: 180px 1fr 180px;
            align-items: center;
            gap: 22px;
        }}

        .sov-team {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .sov-team-right {{
            justify-content: flex-end;
        }}

        .sov-flag {{
            width: 68px;
            height: 45px;
            object-fit: cover;
            border-radius: 6px;
            border: 1px solid rgba(8, 26, 40, 0.18);
            box-shadow: 0 4px 12px rgba(8, 26, 40, 0.13);
            flex-shrink: 0;
        }}

        .sov-team-name {{
            color: #081A28;
            font-size: 17px;
            font-weight: 800;
        }}

        .sov-bar {{
            display: flex;
            width: 100%;
            height: 48px;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 5px 16px rgba(8, 26, 40, 0.14);
        }}

        .sov-segment {{
            min-width: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            font-size: 17px;
            font-weight: 850;
            transition: width 0.35s ease;
        }}

        .sov-segment-1 {{
            background: {color1};
            width: {percentage1}%;
        }}

        .sov-segment-2 {{
            background: {color2};
            width: {percentage2}%;
            border-left: 2px solid rgba(255, 255, 255, 0.85);
        }}

        .sov-mentions-row {{
            display: grid;
            grid-template-columns: 180px 1fr 180px;
            gap: 22px;
            margin-top: 10px;
        }}

        .sov-mentions {{
            color: #5A6872;
            font-size: 12px;
            font-weight: 650;
        }}

        .sov-mentions-right {{
            text-align: right;
        }}

        .sov-interpretation {{
            max-width: 720px;
            margin: 35px auto 0 auto;
            color: #344653;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.65;
            text-align: center;
        }}

        .sov-unavailable {{
            padding: 24px 28px;
            color: #566570;
            background: rgba(8, 26, 40, 0.05);
            border-left: 4px solid #D5B536;
            font-size: 16px;
            line-height: 1.55;
        }}

        @media (max-width: 760px) {{

            .sov-section {{
                padding: 55px 6%;
            }}

            .sov-team-row {{
                grid-template-columns: 1fr 1fr;
                gap: 18px;
            }}

            .sov-team-right {{
                justify-content: flex-end;
            }}

            .sov-bar {{
                grid-column: 1 / -1;
                grid-row: 2;
            }}

            .sov-mentions-row {{
                display: none;
            }}

            .sov-team-name {{
                font-size: 15px;
            }}

            .sov-flag {{
                width: 58px;
                height: 38px;
            }}

        }}

    </style>

    <section class="sov-section">

        <div class="sov-container">

            <div class="sov-kicker">
                LA CONVERSACIÓN
            </div>

            <h2 class="sov-title">
                Quién dominó la conversación
            </h2>

            <div class="sov-team-row">

                <div class="sov-team">
                    {flag1}

                    <span class="sov-team-name">
                        {team1_es}
                    </span>
                </div>

                <div class="sov-bar">

                    <div class="sov-segment sov-segment-1">
                        {percentage1:.1f}%
                    </div>

                    <div class="sov-segment sov-segment-2">
                        {percentage2:.1f}%
                    </div>

                </div>

                <div class="sov-team sov-team-right">

                    <span class="sov-team-name">
                        {team2_es}
                    </span>

                    {flag2}

                </div>

            </div>

            <div class="sov-mentions-row">

                <div class="sov-mentions">
                    {mentions1:,} menciones
                </div>

                <div></div>

                <div class="sov-mentions sov-mentions-right">
                    {mentions2:,} menciones
                </div>

            </div>

            <div class="sov-interpretation">
                {interpretation}
            </div>

        </div>

    </section>
    """

    st.html(
        dedent(
            share_html
        ).strip()
    )

# =========================================================
# CLIMA EMOCIONAL
# =========================================================

EMOTION_ORDER_APP = [
    "Euforia",
    "Tensión",
    "Conflicto",
    "Tristeza"
]

EMOTION_COLORS_APP = {
    "Euforia": "#2ECC71",
    "Tensión": "#F1C40F",
    "Conflicto": "#E67E22",
    "Tristeza": "#3498DB"
}


def build_emotion_bar_html(
    summary
):
    """
    Construye una barra emocional apilada.
    """

    percentages = summary.get(
        "percentages",
        {}
    )

    segments = []

    for emotion in EMOTION_ORDER_APP:

        percentage = float(
            percentages.get(
                emotion,
                0
            )
        )

        if percentage <= 0:
            continue

        color = EMOTION_COLORS_APP[
            emotion
        ]

        # Los porcentajes muy pequeños no llevan texto
        # porque quedarían superpuestos.
        visible_label = (
            f"{percentage:.1f}%"
            if percentage >= 7
            else ""
        )

        text_color = (
            "#10212D"
            if emotion == "Tensión"
            else "#FFFFFF"
        )

        segments.append(
            f"""
            <div
                class="emotion-segment"
                style="
                    width: {percentage}%;
                    background: {color};
                    color: {text_color};
                "
                title="{emotion}: {percentage:.1f}%"
            >
                {visible_label}
            </div>
            """
        )

    return "".join(
        segments
    )


def render_emotional_climate(
    match_data,
    banderas_img
):
    """
    Muestra el clima emocional general y la comparación
    entre las conversaciones de ambos equipos.
    """

    emotional_data = match_data.get(
        "emotional_climate",
        {}
    )

    quality = match_data.get(
        "data_quality",
        {}
    )

    # -----------------------------------------------------
    # SECCIÓN SIN INFORMACIÓN EMOCIONAL
    # -----------------------------------------------------

    if (
    not quality.get(
        "show_social_analysis",
        False
    )
    or not emotional_data.get(
        "available",
        False
    )
):

      render_unavailable_section(
        kicker="LAS EMOCIONES",
        title="Clima emocional",
        message=(
            "No hay suficientes tuits para reconstruir "
            "el clima emocional de este partido."
        ),
        theme="warm"
    )

      return

    # -----------------------------------------------------
    # DATOS
    # -----------------------------------------------------

    overall = emotional_data.get(
        "overall",
        {}
    )

    team1_data = emotional_data.get(
        "team1",
        {}
    )

    team2_data = emotional_data.get(
        "team2",
        {}
    )

    team1 = team1_data.get(
        "name",
        ""
    )

    team2 = team2_data.get(
        "name",
        ""
    )

    team1_es = get_team_name_es(
        team1
    )

    team2_es = get_team_name_es(
        team2
    )

    team1_summary = team1_data.get(
        "summary",
        {}
    )

    team2_summary = team2_data.get(
        "summary",
        {}
    )

    flag1 = obtener_bandera_html(
        team1_es,
        banderas_img,
        css_class="emotion-flag"
    )

    flag2 = obtener_bandera_html(
        team2_es,
        banderas_img,
        css_class="emotion-flag"
    )

    overall_bar = build_emotion_bar_html(
        overall
    )

    team1_bar = build_emotion_bar_html(
        team1_summary
    )

    team2_bar = build_emotion_bar_html(
        team2_summary
    )

    interpretation = emotional_data.get(
        "interpretation",
        ""
    )

    classification_rate = float(
        overall.get(
            "classification_rate",
            0
        )
    )

    classified_tweets = int(
        overall.get(
            "classified_tweets",
            0
        )
    )

    # -----------------------------------------------------
    # LEYENDA
    # -----------------------------------------------------

    legend_items = []

    for emotion in EMOTION_ORDER_APP:

        legend_items.append(
            f"""
            <div class="emotion-legend-item">

                <span
                    class="emotion-legend-color"
                    style="
                        background:
                        {EMOTION_COLORS_APP[emotion]};
                    "
                ></span>

                <span>
                    {emotion}
                </span>

            </div>
            """
        )

    legend_html = "".join(
        legend_items
    )

    # -----------------------------------------------------
    # HTML
    # -----------------------------------------------------

    emotion_html = f"""
    <style>

        .emotion-section {{
            width: 100%;
            box-sizing: border-box;
            background: #F4F1EA;
            padding: 80px 7% 85px 7%;
        }}

        .emotion-container {{
            width: min(980px, 100%);
            margin: 0 auto;
        }}

        .emotion-kicker {{
            color: #C5253D;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2.2px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }}

        .emotion-title {{
            color: #081A28;
            font-size: clamp(31px, 4vw, 48px);
            line-height: 1.05;
            font-weight: 850;
            margin: 0;
        }}

        .emotion-legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 14px 25px;
            margin: 30px 0 42px 0;
        }}

        .emotion-legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #344653;
            font-size: 14px;
            font-weight: 750;
        }}

        .emotion-legend-color {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
            flex-shrink: 0;
        }}

        .emotion-chart {{
            display: flex;
            flex-direction: column;
            gap: 25px;
        }}

        .emotion-row {{
            display: grid;
            grid-template-columns: 155px 1fr;
            align-items: center;
            gap: 24px;
        }}

        .emotion-row-label {{
            display: flex;
            align-items: center;
            gap: 12px;
            color: #081A28;
            font-size: 16px;
            font-weight: 800;
        }}

        .emotion-overall-label {{
            padding-left: 5px;
        }}

        .emotion-flag {{
            width: 53px;
            height: 35px;
            object-fit: cover;
            border-radius: 5px;
            border: 1px solid rgba(8, 26, 40, 0.18);
            box-shadow: 0 3px 9px rgba(8, 26, 40, 0.12);
            flex-shrink: 0;
        }}

        .emotion-bar {{
            display: flex;
            width: 100%;
            height: 39px;
            overflow: hidden;
            border-radius: 6px;
            background: rgba(8, 26, 40, 0.08);
            box-shadow: 0 3px 10px rgba(8, 26, 40, 0.09);
        }}

        .emotion-segment {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 0;
            height: 100%;
            box-sizing: border-box;
            font-size: 12px;
            font-weight: 850;
            border-right: 1px solid rgba(255, 255, 255, 0.35);
        }}

        .emotion-segment:last-child {{
            border-right: none;
        }}

        .emotion-reading {{
            max-width: 760px;
            margin: 42px auto 0 auto;
            padding-top: 28px;
            border-top: 1px solid rgba(8, 26, 40, 0.17);
            text-align: center;
        }}

        .emotion-interpretation {{
            color: #243947;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 18px;
            line-height: 1.65;
        }}

        .emotion-method {{
            margin-top: 10px;
            color: #6A777F;
            font-size: 12px;
            line-height: 1.45;
        }}

        .emotion-unavailable {{
            margin-top: 35px;
            padding: 24px 28px;
            color: #566570;
            background: rgba(8, 26, 40, 0.05);
            border-left: 4px solid #D5B536;
            font-size: 16px;
            line-height: 1.55;
        }}

        @media (max-width: 700px) {{

            .emotion-section {{
                padding: 58px 6%;
            }}

            .emotion-row {{
                grid-template-columns: 1fr;
                gap: 10px;
            }}

            .emotion-chart {{
                gap: 28px;
            }}

            .emotion-bar {{
                height: 35px;
            }}

            .emotion-legend {{
                margin-bottom: 34px;
            }}

        }}

    </style>

    <section class="emotion-section">

        <div class="emotion-container">

            <div class="emotion-kicker">
                LAS EMOCIONES
            </div>

            <h2 class="emotion-title">
                Clima emocional
            </h2>

            <div class="emotion-legend">
                {legend_html}
            </div>

            <div class="emotion-chart">

                <div class="emotion-row">

                    <div class="
                        emotion-row-label
                        emotion-overall-label
                    ">
                        Partido
                    </div>

                    <div class="emotion-bar">
                        {overall_bar}
                    </div>

                </div>

                <div class="emotion-row">

                    <div class="emotion-row-label">
                        {flag1}
                        <span>{team1_es}</span>
                    </div>

                    <div class="emotion-bar">
                        {team1_bar}
                    </div>

                </div>

                <div class="emotion-row">

                    <div class="emotion-row-label">
                        {flag2}
                        <span>{team2_es}</span>
                    </div>

                    <div class="emotion-bar">
                        {team2_bar}
                    </div>

                </div>

            </div>

            <div class="emotion-reading">

                <div class="emotion-interpretation">
                    {interpretation}
                </div>

                <div class="emotion-method">
                    {classified_tweets:,} tuits contenían
                    señales emocionales:
                    {classification_rate:.1f}% de la muestra analizada.
                </div>

            </div>

        </div>

    </section>
    """

    st.html(
        dedent(
            emotion_html
        ).strip()
    )

# =========================================================
# PROTAGONISTAS
# =========================================================

def render_protagonists(
    match_data,
    banderas_img
):
    """
    Muestra el ranking de los jugadores más mencionados.
    """

    protagonists = match_data.get(
        "protagonists",
        {}
    )

    quality = match_data.get(
        "data_quality",
        {}
    )

    ranking = protagonists.get(
        "ranking",
        []
    )

    # -----------------------------------------------------
    # EQUIPOS Y COLORES
    # -----------------------------------------------------

    hero = match_data.get(
        "hero",
        {}
    )

    team1 = hero.get(
        "team1",
        {}
    ).get(
        "name",
        ""
    )

    team2 = hero.get(
        "team2",
        {}
    ).get(
        "name",
        ""
    )

    color1, color2 = get_match_colors(
        match_data.get(
            "match",
            ""
        ),
        team1,
        team2
    )

    # -----------------------------------------------------
    # SECCIÓN SIN INFORMACIÓN
    # -----------------------------------------------------

    if (
    not quality.get(
        "show_social_analysis",
        False
    )
    or not protagonists.get(
        "available",
        False
    )
    or not ranking
):

      render_unavailable_section(
        kicker="LOS NOMBRES DEL PARTIDO",
        title="Protagonistas",
        message=(
            "No hay suficientes menciones para construir "
            "un ranking de protagonistas."
        ),
        theme="dark"
    )

      return

    # -----------------------------------------------------
    # FILAS DEL RANKING
    # -----------------------------------------------------

    max_mentions = max(
        int(
            player.get(
                "mentions",
                0
            )
        )
        for player in ranking
    )

    rows_html = []

    for player_data in ranking:

        rank = int(
            player_data.get(
                "rank",
                0
            )
        )

        player = player_data.get(
            "player",
            ""
        )

        team = player_data.get(
            "team",
            ""
        )

        mentions = int(
            player_data.get(
                "mentions",
                0
            )
        )

        team_es = get_team_name_es(
            team
        )

        flag = obtener_bandera_html(
            team_es,
            banderas_img,
            css_class="players-flag"
        )

        player_color = (
            color1
            if team == team1
            else color2
        )

        if max_mentions > 0:

            relative_width = round(
                mentions
                / max_mentions
                * 100,
                1
            )

        else:
            relative_width = 0

        rows_html.append(
            f"""
            <div class="players-row">

                <div class="players-rank">
                    {rank:02d}
                </div>

                <div class="players-identity">

                    {flag}

                    <div class="players-name-block">

                        <div class="players-name">
                            {player}
                        </div>

                        <div class="players-team">
                            {team_es}
                        </div>

                    </div>

                </div>

                <div class="players-bar-track">

                    <div
                        class="players-bar-fill"
                        style="
                            width: {relative_width}%;
                            background: {player_color};
                        "
                    ></div>

                </div>

                <div class="players-count">

                    <strong>
                        {mentions:,}
                    </strong>

                    <span>
                        menciones
                    </span>

                </div>

            </div>
            """
        )

    ranking_html = "".join(
        rows_html
    )

    interpretation = protagonists.get(
        "interpretation",
        ""
    )

    # -----------------------------------------------------
    # HTML
    # -----------------------------------------------------

    players_html = f"""
    <style>

        .players-section {{
            width: 100%;
            box-sizing: border-box;
            background:
                radial-gradient(
                    circle at top left,
                    #194564 0%,
                    #0B2232 42%,
                    #06131D 100%
                );
            padding: 82px 7% 88px 7%;
        }}

        .players-container {{
            width: min(980px, 100%);
            margin: 0 auto;
        }}

        .players-kicker {{
            color: #E1C33A;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2.2px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }}

        .players-title {{
            color: #FFFFFF;
            font-size: clamp(31px, 4vw, 48px);
            line-height: 1.05;
            font-weight: 850;
            margin: 0 0 45px 0;
        }}

        .players-ranking {{
            display: flex;
            flex-direction: column;
        }}

        .players-row {{
            display: grid;
            grid-template-columns:
                42px
                235px
                minmax(190px, 1fr)
                105px;
            align-items: center;
            gap: 20px;
            min-height: 79px;
            border-top:
                1px solid rgba(255, 255, 255, 0.13);
        }}

        .players-row:last-child {{
            border-bottom:
                1px solid rgba(255, 255, 255, 0.13);
        }}

        .players-rank {{
            color: #E1C33A;
            font-size: 14px;
            font-weight: 850;
            letter-spacing: 1px;
        }}

        .players-identity {{
            display: flex;
            align-items: center;
            gap: 14px;
            min-width: 0;
        }}

        .players-flag {{
            width: 48px;
            height: 32px;
            object-fit: cover;
            border-radius: 4px;
            border:
                1px solid rgba(255, 255, 255, 0.35);
            flex-shrink: 0;
        }}

        .players-name-block {{
            min-width: 0;
        }}

        .players-name {{
            color: #FFFFFF;
            font-size: 18px;
            font-weight: 820;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .players-team {{
            margin-top: 3px;
            color: rgba(255, 255, 255, 0.58);
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}

        .players-bar-track {{
            width: 100%;
            height: 13px;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 20px;
        }}

        .players-bar-fill {{
            height: 100%;
            min-width: 3px;
            border-radius: 20px;
        }}

        .players-count {{
            color: #FFFFFF;
            text-align: right;
        }}

        .players-count strong {{
            display: block;
            font-size: 17px;
            font-weight: 850;
        }}

        .players-count span {{
            display: block;
            margin-top: 2px;
            color: rgba(255, 255, 255, 0.57);
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .players-interpretation {{
            max-width: 730px;
            margin: 38px auto 0 auto;
            color: rgba(255, 255, 255, 0.85);
            font-family: Georgia, "Times New Roman", serif;
            font-size: 18px;
            line-height: 1.65;
            text-align: center;
        }}

        .players-unavailable {{
            padding: 24px 28px;
            color: rgba(255, 255, 255, 0.74);
            background: rgba(255, 255, 255, 0.07);
            border-left: 4px solid #E1C33A;
            font-size: 16px;
            line-height: 1.55;
        }}

        @media (max-width: 760px) {{

            .players-section {{
                padding: 58px 6%;
            }}

            .players-row {{
                grid-template-columns:
                    30px
                    minmax(145px, 1fr)
                    75px;
                gap: 13px;
            }}

            .players-bar-track {{
                display: none;
            }}

            .players-flag {{
                width: 41px;
                height: 28px;
            }}

            .players-name {{
                font-size: 15px;
            }}

            .players-count strong {{
                font-size: 15px;
            }}

        }}

    </style>

    <section class="players-section">

        <div class="players-container">

            <div class="players-kicker">
                LOS NOMBRES DEL PARTIDO
            </div>

            <h2 class="players-title">
                Protagonistas
            </h2>

            <div class="players-ranking">
                {ranking_html}
            </div>

            <div class="players-interpretation">
                {interpretation}
            </div>

        </div>

    </section>
    """

    st.html(
        dedent(
            players_html
        ).strip()
    )

# =========================================================
# TWEETS DESTACADOS
# =========================================================

def format_social_number(
    value
):
    """
    Formatea números con separador de miles en español.
    """

    return (
        f"{int(value):,}"
        .replace(
            ",",
            "."
        )
    )


def render_featured_tweets(
    match_data
):
    """
    Muestra las tres piezas editoriales seleccionadas
    para representar la conversación del partido.
    """

    featured = match_data.get(
        "featured_tweets",
        {}
    )

    quality = match_data.get(
        "data_quality",
        {}
    )

    tweets = featured.get(
        "tweets",
        []
    )

    # Si la muestra no permite una selección editorial
    # sólida, la sección no se muestra.
    if (
        not quality.get(
            "show_featured_tweets",
            False
        )
        or not featured.get(
            "available",
            False
        )
        or not tweets
    ):
        return

    cards_html = []

    card_accents = [
        "#C5253D",
        "#D5B536",
        "#2B67D9"
    ]

    for index, tweet in enumerate(
        tweets[:3]
    ):

        label = tweet.get(
            "label",
            "Tweet destacado"
        )

        # En la aplicación se prioriza la traducción
        # editorial al español.
        text = (
            tweet.get(
                "translation_es"
            )
            or tweet.get(
                "text",
                ""
            )
        )

        likes = int(
            tweet.get(
                "likes",
                0
            )
        )

        retweets = int(
            tweet.get(
                "retweets",
                0
            )
        )

        accent = card_accents[
            index % len(
                card_accents
            )
        ]

        likes_html = ""

        if likes > 0:

            likes_html = f"""
            <span class="tweet-stat">
                ♥ {format_social_number(likes)}
            </span>
            """

        retweets_html = ""

        if retweets > 0:

            retweets_html = f"""
            <span class="tweet-stat">
                ↻ {format_social_number(retweets)}
            </span>
            """

        cards_html.append(
            f"""
            <article
                class="tweet-card"
                style="
                    border-top-color: {accent};
                "
            >

                <div class="tweet-card-label">
                    {label}
                </div>

                <blockquote class="tweet-card-text">
                    “{text}”
                </blockquote>

                <div class="tweet-card-footer">
                    {likes_html}
                    {retweets_html}
                </div>

            </article>
            """
        )

    cards_content = "".join(
        cards_html
    )

    tweets_html = f"""
    <style>

        .featured-section {{
            width: 100%;
            box-sizing: border-box;
            background: #FFFFFF;
            padding: 82px 7% 90px 7%;
        }}

        .featured-container {{
            width: min(1080px, 100%);
            margin: 0 auto;
        }}

        .featured-kicker {{
            color: #C5253D;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2.2px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }}

        .featured-title {{
            color: #081A28;
            font-size: clamp(31px, 4vw, 48px);
            line-height: 1.05;
            font-weight: 850;
            margin: 0 0 46px 0;
        }}

        .featured-grid {{
            display: grid;
            grid-template-columns:
                repeat(3, minmax(0, 1fr));
            gap: 22px;
            align-items: stretch;
        }}

        .tweet-card {{
            min-height: 285px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            padding: 28px 27px 23px 27px;
            background: #F4F1EA;
            border-top: 6px solid;
            border-radius: 4px 4px 12px 12px;
            box-shadow:
                0 8px 24px rgba(8, 26, 40, 0.10);
        }}

        .tweet-card-label {{
            color: #52616B;
            font-size: 11px;
            font-weight: 850;
            letter-spacing: 0.9px;
            text-transform: uppercase;
        }}

        .tweet-card-text {{
            flex: 1;
            margin: 24px 0;
            padding: 0;
            border: none;
            color: #102938;
            font-family:
                Georgia,
                "Times New Roman",
                serif;
            font-size: 18px;
            line-height: 1.58;
        }}

        .tweet-card-footer {{
            min-height: 20px;
            display: flex;
            align-items: center;
            gap: 18px;
            padding-top: 17px;
            border-top:
                1px solid rgba(8, 26, 40, 0.13);
        }}

        .tweet-stat {{
            color: #60717B;
            font-size: 12px;
            font-weight: 750;
        }}

        @media (max-width: 850px) {{

            .featured-grid {{
                grid-template-columns: 1fr;
            }}

            .tweet-card {{
                min-height: 220px;
            }}

        }}

        @media (max-width: 600px) {{

            .featured-section {{
                padding: 58px 6% 65px 6%;
            }}

            .tweet-card {{
                min-height: 0;
            }}

            .tweet-card-text {{
                font-size: 17px;
            }}

        }}

    </style>

    <section class="featured-section">

        <div class="featured-container">

            <div class="featured-kicker">
                LAS VOCES DEL PARTIDO
            </div>

            <h2 class="featured-title">
                Tweets destacados
            </h2>

            <div class="featured-grid">
                {cards_content}
            </div>

        </div>

    </section>
    """

    st.html(
        dedent(
            tweets_html
        ).strip()
    )

# =========================================================
# RADIOGRAFÍA FINAL
# =========================================================

def render_final_radiography(
    match_data
):
    """
    Muestra el resumen ejecutivo final del partido.
    """

    radiography = match_data.get(
        "radiography",
        {}
    )

    cards = radiography.get(
        "cards",
        []
    )

    final_sentence = radiography.get(
        "final_sentence",
        ""
    )

    if not cards:
        return

    card_accents = {
        "result": "#C5253D",
        "tweets": "#D5B536",
        "conversation": "#2B67D9",
        "protagonist": "#74A9D3",
        "emotion": "#2ECC71",
        "peak": "#E67E22"
    }

    cards_html = []

    for card in cards:

        key = card.get(
            "key",
            ""
        )

        label = card.get(
            "label",
            ""
        )

        value = card.get(
            "value",
            ""
        )

        detail = card.get(
            "detail",
            ""
        )

        accent = card_accents.get(
            key,
            "#D5B536"
        )

        unavailable = (
            "sin datos" in str(value).lower()
            or "sin cobertura" in str(value).lower()
        )

        unavailable_class = (
            " radiography-card-unavailable"
            if unavailable
            else ""
        )

        detail_html = ""

        if detail:

            detail_html = f"""
            <div class="radiography-card-detail">
                {detail}
            </div>
            """

        cards_html.append(
            f"""
            <article
                class="
                    radiography-card
                    {unavailable_class}
                "
                style="
                    --card-accent: {accent};
                "
            >

                <div class="radiography-card-line"></div>

                <div class="radiography-card-label">
                    {label}
                </div>

                <div class="radiography-card-value">
                    {value}
                </div>

                {detail_html}

            </article>
            """
        )

    cards_content = "".join(
        cards_html
    )

    radiography_html = f"""
    <style>

        .radiography-section {{
            position: relative;
            width: 100%;
            box-sizing: border-box;
            overflow: hidden;
            background:
                radial-gradient(
                    circle at top,
                    #244B64 0%,
                    #0B2232 43%,
                    #040B10 100%
                );
            padding: 88px 7% 105px 7%;
        }}

        .radiography-section::after {{
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 7px;
            background:
                linear-gradient(
                    90deg,
                    #C5253D 0%,
                    #C5253D 33.33%,
                    #2B67D9 33.33%,
                    #2B67D9 66.66%,
                    #D5B536 66.66%,
                    #D5B536 100%
                );
        }}

        .radiography-container {{
            width: min(1080px, 100%);
            margin: 0 auto;
        }}

        .radiography-kicker {{
            color: #D5B536;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2.2px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }}

        .radiography-title {{
            color: #FFFFFF;
            font-size: clamp(32px, 4vw, 50px);
            line-height: 1.05;
            font-weight: 850;
            margin: 0 0 48px 0;
        }}

        .radiography-grid {{
            display: grid;
            grid-template-columns:
                repeat(3, minmax(0, 1fr));
            gap: 18px;
        }}

        .radiography-card {{
            position: relative;
            min-height: 165px;
            box-sizing: border-box;
            overflow: hidden;
            padding: 27px 25px 24px 25px;
            background: rgba(255, 255, 255, 0.075);
            border:
                1px solid rgba(255, 255, 255, 0.13);
            border-radius: 10px;
        }}

        .radiography-card-line {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: var(--card-accent);
        }}

        .radiography-card-label {{
            color: rgba(255, 255, 255, 0.57);
            font-size: 10px;
            font-weight: 850;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .radiography-card-value {{
            margin-top: 18px;
            color: #FFFFFF;
            font-size: clamp(21px, 2.3vw, 30px);
            line-height: 1.13;
            font-weight: 850;
        }}

        .radiography-card-detail {{
            margin-top: 12px;
            color: rgba(255, 255, 255, 0.67);
            font-size: 12px;
            font-weight: 650;
            line-height: 1.4;
        }}

        .radiography-card-unavailable {{
            opacity: 0.52;
        }}

        .radiography-ending {{
            max-width: 850px;
            margin: 58px auto 0 auto;
            padding-top: 38px;
            border-top:
                1px solid rgba(255, 255, 255, 0.18);
            color: #FFFFFF;
            font-family:
                Georgia,
                "Times New Roman",
                serif;
            font-size: clamp(22px, 2.7vw, 32px);
            line-height: 1.5;
            text-align: center;
        }}

        @media (max-width: 850px) {{

            .radiography-grid {{
                grid-template-columns:
                    repeat(2, minmax(0, 1fr));
            }}

        }}

        @media (max-width: 580px) {{

            .radiography-section {{
                padding: 60px 6% 78px 6%;
            }}

            .radiography-grid {{
                grid-template-columns: 1fr;
            }}

            .radiography-card {{
                min-height: 145px;
            }}

        }}

    </style>

    <section class="radiography-section">

        <div class="radiography-container">

            <div class="radiography-kicker">
                EL PARTIDO EN SEIS CLAVES
            </div>

            <h2 class="radiography-title">
                Radiografía final
            </h2>

            <div class="radiography-grid">
                {cards_content}
            </div>

            <div class="radiography-ending">
                {final_sentence}
            </div>

        </div>

    </section>
    """

    st.html(
        dedent(
            radiography_html
        ).strip()
    )

# =========================================================
# AVISO EDITORIAL PARA SECCIONES SIN DATOS
# =========================================================

def render_unavailable_section(
    kicker,
    title,
    message,
    theme="light"
):
    """
    Muestra una sección editorial cuando un análisis
    específico no se encuentra disponible.
    """

    if theme == "dark":

        background = """
            radial-gradient(
                circle at top left,
                #194564 0%,
                #0B2232 42%,
                #06131D 100%
            )
        """

        title_color = "#FFFFFF"
        text_color = "rgba(255,255,255,0.78)"
        kicker_color = "#E1C33A"
        notice_background = "rgba(255,255,255,0.07)"
        notice_border = "rgba(255,255,255,0.14)"

    elif theme == "warm":

        background = "#F4F1EA"
        title_color = "#081A28"
        text_color = "#52616B"
        kicker_color = "#C5253D"
        notice_background = "rgba(8,26,40,0.05)"
        notice_border = "rgba(8,26,40,0.13)"

    else:

        background = "#FFFFFF"
        title_color = "#081A28"
        text_color = "#52616B"
        kicker_color = "#C5253D"
        notice_background = "#F4F1EA"
        notice_border = "rgba(8,26,40,0.13)"

    unavailable_html = f"""
    <style>

        .unavailable-section {{
            width: 100%;
            box-sizing: border-box;
            background: {background};
            padding: 72px 7% 76px 7%;
        }}

        .unavailable-container {{
            width: min(980px, 100%);
            margin: 0 auto;
        }}

        .unavailable-kicker {{
            color: {kicker_color};
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2.2px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }}

        .unavailable-title {{
            color: {title_color};
            font-size: clamp(30px, 4vw, 46px);
            line-height: 1.05;
            font-weight: 850;
            margin: 0 0 34px 0;
        }}

        .unavailable-notice {{
            padding: 23px 27px;
            color: {text_color};
            background: {notice_background};
            border:
                1px solid {notice_border};
            border-left:
                5px solid {kicker_color};
            border-radius: 7px;
            font-size: 16px;
            font-weight: 600;
            line-height: 1.55;
        }}

        @media (max-width: 600px) {{

            .unavailable-section {{
                padding: 53px 6% 57px 6%;
            }}

        }}

    </style>

    <section class="unavailable-section">

        <div class="unavailable-container">

            <div class="unavailable-kicker">
                {kicker}
            </div>

            <h2 class="unavailable-title">
                {title}
            </h2>

            <div class="unavailable-notice">
                {message}
            </div>

        </div>

    </section>
    """

    st.html(
        dedent(
            unavailable_html
        ).strip()
    )
