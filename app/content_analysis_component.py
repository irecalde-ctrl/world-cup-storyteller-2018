
import streamlit as st

from html import escape
from textwrap import dedent

from app_config import get_team_name_es
from banderas import obtener_bandera_html



def compact_html(value):

    return "\n".join(
        line.strip()
        for line in value.splitlines()
    )


def format_percentage_es(value):

    return (
        f"{float(value):.1f}"
        .replace(".", ",")
    )


def select_display_terms(
    terms,
    maximum=4
):
    # Evita mostrar simultáneamente términos redundantes,
    # por ejemplo: di, maria y di maria.

    ordered_terms = sorted(
        [
            str(term).strip()
            for term in terms
            if str(term).strip()
        ],
        key=lambda term: (
            len(term.split()),
            len(term)
        ),
        reverse=True
    )

    selected = []
    selected_tokens = []

    for term in ordered_terms:

        term_tokens = set(
            term.lower().split()
        )

        if any(
            term_tokens.issubset(
                existing_tokens
            )
            for existing_tokens in selected_tokens
        ):
            continue

        selected.append(
            term
        )

        selected_tokens.append(
            term_tokens
        )

        if len(selected) >= maximum:
            break

    return selected


def build_topic_card(
    topic,
    topic_number
):

    percentage = format_percentage_es(
        topic.get(
            "prevalence",
            0
        )
    )

    terms = select_display_terms(
        topic.get(
            "terms_display_es",
            []
        )
    )

    terms_html = "".join(
        (
            '<span class="content-term">'
            f'{escape(term)}'
            '</span>'
        )
        for term in terms
    )

    representative_tweet = escape(
        str(
            topic.get(
                "representative_tweet_es",
                ""
            )
        )
    )

    return f'''
        <div class="content-topic">
            <div class="content-topic-header">
                <span>EJE {topic_number:02d}</span>
                <strong>{percentage}%</strong>
            </div>

            <div class="content-terms">
                {terms_html}
            </div>

            <div class="content-original-label">
                TUIT REPRESENTATIVO · TRADUCCIÓN AUTOMÁTICA
            </div>

            <blockquote class="content-tweet">
                “{representative_tweet}”
            </blockquote>
        </div>
    '''


def build_team_content_card(
    team_result,
    banderas_img,
    accent_class
):

    team = team_result.get(
        "team",
        ""
    )

    team_es = get_team_name_es(
        team
    )

    flag = obtener_bandera_html(
        team_es,
        banderas_img,
        css_class="content-flag"
    )

    topics = team_result.get(
        "topics",
        []
    )

    topics_html = "".join(
        build_topic_card(
            topic,
            position
        )
        for position, topic in enumerate(
            topics,
            start=1
        )
    )

    if topics:

        principal_topic = topics[0]

        principal_terms = select_display_terms(
            principal_topic.get(
                "terms_display_es",
                []
            ),
            maximum=3
        )

        principal_percentage = (
            format_percentage_es(
                principal_topic.get(
                    "prevalence",
                    0
                )
            )
        )

        terms_sentence = ", ".join(
            escape(term)
            for term in principal_terms
        )

        automatic_summary = (
            f"El eje principal concentró el "
            f"{principal_percentage}% del peso temático "
            f"y estuvo asociado con {terms_sentence}."
        )

    else:

        automatic_summary = (
            "No se identificaron temas con suficiente "
            "consistencia."
        )

    sample_size = int(
        team_result.get(
            "sample_size",
            0
        )
    )

    sample_size_es = (
        f"{sample_size:,}"
        .replace(",", ".")
    )

    return f'''
        <article class="content-team-card {accent_class}">
            <div class="content-team-heading">
                {flag}

                <div>
                    <h3>{escape(team_es)}</h3>
                    <p>{sample_size_es} tuits analizados</p>
                </div>
            </div>

            <p class="content-team-summary">
                {automatic_summary}
            </p>

            {topics_html}
        </article>
    '''


def render_content_analysis(
    match_data,
    banderas_img
):

    content = match_data.get(
        "content_analysis",
        {}
    )

    if not content.get(
        "available",
        False
    ):

        st.markdown(
            compact_html(
                '''
                <section class="content-section content-unavailable">
                    <div class="content-container">
                        <div class="content-kicker">
                            EL CONTENIDO DE LA CONVERSACIÓN
                        </div>

                        <h2>¿De qué habló Twitter?</h2>

                        <p>
                            No existe una cantidad suficiente de
                            tuits por selección para identificar
                            temas de conversación con criterios
                            confiables.
                        </p>
                    </div>
                </section>
                '''
            ),
            unsafe_allow_html=True
        )

        return

    team1_html = build_team_content_card(
        content.get(
            "team1",
            {}
        ),
        banderas_img,
        "content-accent-red"
    )

    team2_html = build_team_content_card(
        content.get(
            "team2",
            {}
        ),
        banderas_img,
        "content-accent-blue"
    )

    st.markdown(
        compact_html(
            f'''
            <style>
                .content-section {{
                    background:
                        radial-gradient(
                            circle at top left,
                            #173e55 0%,
                            #071c2b 52%,
                            #04131f 100%
                        );
                    color: #ffffff;
                    padding: 5.5rem 2rem 6rem;
                }}

                .content-container {{
                    max-width: 1080px;
                    margin: 0 auto;
                }}

                .content-kicker {{
                    color: #f4c928;
                    font-size: 0.76rem;
                    font-weight: 900;
                    letter-spacing: 0.22em;
                    margin-bottom: 0.7rem;
                }}

                .content-section h2 {{
                    color: #ffffff;
                    font-size: clamp(2.3rem, 5vw, 4rem);
                    line-height: 1;
                    margin: 0 0 1rem;
                }}

                .content-intro {{
                    color: #bfd1dc;
                    font-family: Georgia, serif;
                    font-size: 1.08rem;
                    line-height: 1.6;
                    margin: 0 0 2.8rem;
                    max-width: 760px;
                }}

                .content-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                    gap: 1.25rem;
                }}

                .content-team-card {{
                    background: rgba(19, 47, 64, 0.94);
                    border: 1px solid rgba(255,255,255,0.13);
                    border-radius: 16px;
                    overflow: hidden;
                    padding: 1.5rem;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.2);
                }}

                .content-accent-red {{
                    border-top: 5px solid #dc2940;
                }}

                .content-accent-blue {{
                    border-top: 5px solid #2f6feb;
                }}

                .content-team-heading {{
                    align-items: center;
                    display: flex;
                    gap: 0.9rem;
                    margin-bottom: 1rem;
                }}

                .content-flag {{
                    border-radius: 5px;
                    height: 42px;
                    object-fit: cover;
                    width: 62px;
                }}

                .content-team-heading h3 {{
                    color: #ffffff;
                    font-size: 1.55rem;
                    margin: 0;
                }}

                .content-team-heading p {{
                    color: #93adbc;
                    font-size: 0.78rem;
                    font-weight: 700;
                    margin: 0.2rem 0 0;
                    text-transform: uppercase;
                }}

                .content-team-summary {{
                    border-bottom: 1px solid rgba(255,255,255,0.12);
                    color: #dce7ed;
                    font-family: Georgia, serif;
                    line-height: 1.55;
                    margin: 0 0 1.3rem;
                    padding-bottom: 1.3rem;
                }}

                .content-topic + .content-topic {{
                    border-top: 1px solid rgba(255,255,255,0.12);
                    margin-top: 1.3rem;
                    padding-top: 1.3rem;
                }}

                .content-topic-header {{
                    align-items: center;
                    color: #91acbb;
                    display: flex;
                    font-size: 0.72rem;
                    font-weight: 900;
                    justify-content: space-between;
                    letter-spacing: 0.15em;
                }}

                .content-topic-header strong {{
                    color: #f4c928;
                    font-size: 0.9rem;
                }}

                .content-terms {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.45rem;
                    margin: 0.8rem 0 1rem;
                }}

                .content-term {{
                    background: rgba(255,255,255,0.09);
                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 999px;
                    color: #ffffff;
                    font-size: 0.78rem;
                    font-weight: 700;
                    padding: 0.35rem 0.65rem;
                }}

                .content-original-label {{
                    color: #7692a2;
                    font-size: 0.62rem;
                    font-weight: 900;
                    letter-spacing: 0.13em;
                    margin-bottom: 0.45rem;
                }}

                .content-tweet {{
                    border-left: 3px solid #f4c928;
                    color: #eaf1f4;
                    font-family: Georgia, serif;
                    font-size: 0.94rem;
                    line-height: 1.5;
                    margin: 0;
                    padding-left: 0.85rem;
                }}

                .content-unavailable {{
                    background: #f4efe7;
                    color: #082339;
                }}

                .content-unavailable h2 {{
                    color: #082339;
                }}

                .content-unavailable p {{
                    color: #4f6572;
                    font-family: Georgia, serif;
                    font-size: 1.05rem;
                    line-height: 1.6;
                    max-width: 720px;
                }}

                @media (max-width: 760px) {{
                    .content-section {{
                        padding: 4rem 1.2rem;
                    }}

                    .content-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>

            <section class="content-section">
                <div class="content-container">
                    <div class="content-kicker">
                        EL CONTENIDO DE LA CONVERSACIÓN
                    </div>

                    <h2>¿De qué habló Twitter?</h2>

                    <p class="content-intro">
                        Dos modelos temáticos reconstruyen los
                        asuntos que concentraron la conversación
                        alrededor de cada selección.
                    </p>

                    <div class="content-grid">
                        {team1_html}
                        {team2_html}
                    </div>
                </div>
            </section>
            '''
        ),
        unsafe_allow_html=True
    )
