
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app_config import get_team_name_es
from banderas import normalizar_nombre

from chart_config import (
    get_event_team,
    get_event_type,
    get_match_colors,
    get_visible_line_color,
    hex_to_rgba
)


def get_flag_uri(
    team_name,
    banderas_img
):

    visible_name = get_team_name_es(
        team_name
    )

    flag_key = normalizar_nombre(
        visible_name
    )

    return banderas_img.get(
        flag_key,
        ""
    )


def get_missing_ranges(
    momentum
):

    missing = momentum.loc[
        ~momentum["has_coverage"],
        [
            "display_start",
            "display_end"
        ]
    ]

    if missing.empty:
        return []

    ranges = []

    current_start = float(
        missing.iloc[0][
            "display_start"
        ]
    )

    current_end = float(
        missing.iloc[0][
            "display_end"
        ]
    )

    for _, row in missing.iloc[1:].iterrows():

        start = float(
            row["display_start"]
        )

        end = float(
            row["display_end"]
        )

        if np.isclose(
            start,
            current_end
        ):
            current_end = end

        else:
            ranges.append(
                (
                    current_start,
                    current_end
                )
            )

            current_start = start
            current_end = end

    ranges.append(
        (
            current_start,
            current_end
        )
    )

    return ranges


def football_minute_to_display(
    minute,
    periods
):

    minute = float(minute)

    play_periods = [
        period
        for period in periods
        if period["type"] == "play"
    ]

    for period in play_periods:

        football_start = float(
            period["football_start"]
        )

        football_end = float(
            period["football_end"]
        )

        if (
            football_start
            <= minute
            <= football_end
        ):

            football_duration = (
                football_end
                - football_start
            )

            if football_duration <= 0:
                return None

            progress = (
                minute
                - football_start
            ) / football_duration

            return (
                float(
                    period["display_start"]
                )
                + progress
                * float(
                    period["display_width"]
                )
            )

    if play_periods:

        last_period = play_periods[-1]

        if minute >= float(
            last_period["football_end"]
        ):
            return float(
                last_period["display_end"]
            )

    return None


def shootout_order_to_display(
    order,
    periods,
    shootout
):

    shootout_period = next(
        (
            period
            for period in periods
            if period["key"] == "shootout"
        ),
        None
    )

    if shootout_period is None:
        return None

    total_penalties = max(
        len(shootout),
        1
    )

    start_x = float(
        shootout_period["display_start"]
    )

    width = float(
        shootout_period["display_width"]
    )

    return (
        start_x
        + (
            float(order)
            / (total_penalties + 1)
        )
        * width
    )


def build_final_axis(
    metadata
):

    tick_values = []
    tick_text = []
    guide_values = []

    for period in metadata["periods"]:

        start_x = float(
            period["display_start"]
        )

        end_x = float(
            period["display_end"]
        )

        if period["type"] == "play":

            football_start = float(
                period["football_start"]
            )

            football_end = float(
                period["football_end"]
            )

            football_duration = (
                football_end
                - football_start
            )

            if football_duration == 45:

                football_ticks = list(
                    np.arange(
                        football_start,
                        football_end + 0.1,
                        15
                    )
                )

            else:

                football_ticks = [
                    football_start,
                    football_end
                ]

            for football_minute in (
                football_ticks
            ):

                progress = (
                    football_minute
                    - football_start
                ) / football_duration

                display_x = (
                    start_x
                    + progress
                    * float(
                        period["display_width"]
                    )
                )

                tick_values.append(
                    display_x
                )

                tick_text.append(
                    f"{int(football_minute)}′"
                )

                guide_values.append(
                    display_x
                )

        else:

            center_x = (
                start_x + end_x
            ) / 2

            if (
                period["key"]
                == "extra_time_transition"
            ):

                label = (
                    "<b>TIEMPO<br>"
                    "SUPLEMENTARIO</b>"
                )

            else:

                label = (
                    f"<b>{period['label']}</b>"
                )

            tick_values.append(
                center_x
            )

            tick_text.append(
                label
            )

    return (
        tick_values,
        tick_text,
        guide_values
    )


def render_momentum_unavailable(
    match_data
):

    quality = match_data[
        "data_quality"
    ]

    st.html(
        f"""
        <section style="
            padding: 95px 7%;
            background: #050505;
            color: white;
            text-align: center;
        ">
            <div style="
                max-width: 760px;
                margin: 0 auto;
            ">
                <div style="
                    color: #d4af37;
                    font-size: 13px;
                    font-weight: 900;
                    letter-spacing: 2px;
                ">
                    PULSO DEL PARTIDO EN TWITTER
                </div>

                <h2 style="
                    margin: 18px 0;
                    font-size: 38px;
                ">
                    Sin línea temporal disponible
                </h2>

                <p style="
                    color: rgba(255,255,255,0.68);
                    font-size: 17px;
                    line-height: 1.6;
                ">
                    {quality["message"]}
                </p>
            </div>
        </section>
        """
    )


def render_twitter_momentum(
    match_data,
    banderas_img
):

    quality = match_data[
        "data_quality"
    ]

    if not quality.get(
        "show_momentum",
        False
    ):

        render_momentum_unavailable(
            match_data
        )

        return

    momentum_data = match_data[
        "momentum"
    ]

    metadata = momentum_data[
        "metadata"
    ]

    momentum = pd.DataFrame(
        momentum_data["series"]
    )

    if momentum.empty:

        render_momentum_unavailable(
            match_data
        )

        return

    for column in [
        "minute",
        "display_start",
        "display_end",
        "team1_mentions",
        "team2_mentions",
        "team2_plot"
    ]:

        momentum[column] = pd.to_numeric(
            momentum[column],
            errors="coerce"
        )

    momentum["has_coverage"] = (
        momentum["has_coverage"]
        .fillna(False)
        .astype(bool)
    )

    match_name = match_data["match"]

    team1 = metadata["team1"]
    team2 = metadata["team2"]

    (
        team1_color,
        team2_color
    ) = get_match_colors(
        match_name,
        team1,
        team2
    )

    team1_line = get_visible_line_color(
        team1_color
    )

    team2_line = get_visible_line_color(
        team2_color
    )

    available_mentions = pd.concat([
        momentum["team1_mentions"],
        momentum["team2_mentions"]
    ]).dropna()

    if (
        available_mentions.empty
        or available_mentions.max() <= 0
    ):
        max_mentions = 1.0

    else:
        max_mentions = float(
            available_mentions.max()
        )

    vertical_limit = (
        max_mentions * 1.30
    )

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=momentum["minute"],
            y=momentum[
                "team1_mentions"
            ],
            mode="lines",
            line={
                "color": team1_line,
                "width": 3,
                "shape": "spline",
                "smoothing": 1.10
            },
            fill="tozeroy",
            fillcolor=hex_to_rgba(
                team1_color,
                0.76
            ),
            connectgaps=False,
            name=team1,
            customdata=np.column_stack([
                momentum[
                    "period_label"
                ],
                momentum[
                    "team1_mentions"
                ]
            ]),
            hovertemplate=(
                f"<b>{team1}</b><br>"
                "%{customdata[0]}<br>"
                "%{customdata[1]:.0f} menciones"
                "<extra></extra>"
            )
        )
    )

    figure.add_trace(
        go.Scatter(
            x=momentum["minute"],
            y=momentum["team2_plot"],
            mode="lines",
            line={
                "color": team2_line,
                "width": 3,
                "shape": "spline",
                "smoothing": 1.10
            },
            fill="tozeroy",
            fillcolor=hex_to_rgba(
                team2_color,
                0.76
            ),
            connectgaps=False,
            name=team2,
            customdata=np.column_stack([
                momentum[
                    "period_label"
                ],
                momentum[
                    "team2_mentions"
                ]
            ]),
            hovertemplate=(
                f"<b>{team2}</b><br>"
                "%{customdata[0]}<br>"
                "%{customdata[1]:.0f} menciones"
                "<extra></extra>"
            )
        )
    )

    period_colors = {
        "halftime":
            "rgba(212,175,55,0.12)",

        "extra_time_transition":
            "rgba(29,78,158,0.17)",

        "extra_time_halftime":
            "rgba(212,175,55,0.12)",

        "shootout":
            "rgba(213,43,30,0.13)"
    }

    for period in metadata["periods"]:

        if period["type"] == "play":
            continue

        figure.add_vrect(
            x0=period["display_start"],
            x1=period["display_end"],
            fillcolor=period_colors.get(
                period["key"],
                "rgba(255,255,255,0.08)"
            ),
            line_width=0,
            layer="below"
        )

    for start, end in (
        get_missing_ranges(
            momentum
        )
    ):

        figure.add_vrect(
            x0=start,
            x1=end,
            fillcolor=(
                "rgba(0,0,0,0.17)"
            ),
            line_width=0,
            layer="below"
        )

        if end - start >= 20:

            figure.add_annotation(
                x=(start + end) / 2,
                y=0,
                text=(
                    "SIN COBERTURA "
                    "DEL DATASET"
                ),
                textangle=-90,
                showarrow=False,
                font={
                    "size": 10,
                    "color":
                        "rgba(255,255,255,0.30)"
                }
            )

    figure.add_hline(
        y=0,
        line_color="#F2F2F2",
        line_width=2
    )

    icons = {
        "goal": "⚽",
        "save": "🧤"
    }

    event_distance = (
        max_mentions * 0.18
    )

    for event_index, event in enumerate(
        metadata["events"]
    ):

        event_type = get_event_type(
            match_name,
            event
        )

        if (
            event_type == "shootout"
            and metadata["has_shootout"]
        ):
            continue

        event_x = football_minute_to_display(
            event["minute"],
            metadata["periods"]
        )

        if event_x is None:
            continue

        event_team = get_event_team(
            match_name,
            event_index,
            event
        )

        direction = (
            1
            if event_team == team1
            else -1
        )

        event_y = (
            direction
            * event_distance
            * (
                1
                + 0.16
                * (event_index % 2)
            )
        )

        figure.add_annotation(
            x=event_x,
            y=event_y,
            ax=event_x,
            ay=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#F2F2F2"
        )

        figure.add_trace(
            go.Scatter(
                x=[event_x],
                y=[event_y],
                mode="text",
                text=[
                    icons.get(
                        event_type,
                        "●"
                    )
                ],
                textfont={
                    "size": 17,
                    "color": "#FFFFFF"
                },
                showlegend=False,
                hovertemplate=(
                    f"<b>{int(event['minute'])}′</b><br>"
                    f"{event.get('event', '')}"
                    "<extra></extra>"
                )
            )
        )

    shootout = metadata.get(
        "shootout",
        []
    )

    penalty_distance = (
        max_mentions * 0.28
    )

    for penalty in shootout:

        penalty_x = (
            shootout_order_to_display(
                penalty["order"],
                metadata["periods"],
                shootout
            )
        )

        if penalty_x is None:
            continue

        penalty_y = (
            penalty_distance
            if penalty["team"] == team1
            else -penalty_distance
        )

        penalty_icon = (
            "⚽"
            if penalty["outcome"] == "scored"
            else "✕"
        )

        figure.add_trace(
            go.Scatter(
                x=[penalty_x],
                y=[penalty_y],
                mode="text",
                text=[penalty_icon],
                textfont={
                    "size": 19,
                    "color": "#FFFFFF"
                },
                showlegend=False,
                hovertemplate=(
                    f"<b>{penalty.get('player', '')}</b><br>"
                    f"{penalty.get('team', '')}"
                    "<extra></extra>"
                )
            )
        )

    (
        tick_values,
        tick_text,
        guide_values
    ) = build_final_axis(
        metadata
    )

    for guide_x in guide_values:

        figure.add_vline(
            x=guide_x,
            line_color=(
                "rgba(255,255,255,0.15)"
            ),
            line_width=1,
            line_dash="dot",
            layer="below"
        )

    figure.update_layout(
        title={
            "text": (
                "<b>"
                "PULSO DEL PARTIDO EN TWITTER"
                "</b>"
                "<br>"
                "<span style='font-size:15px;'>"
                "Menciones por equipo "
                "en intervalos de cinco minutos"
                "</span>"
            ),
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": 29,
                "color": "#FFFFFF"
            }
        },
        height=650,
        margin={
            "l": 125,
            "r": 45,
            "t": 145,
            "b": 105
        },
        paper_bgcolor="#050505",
        plot_bgcolor="#3B3F41",
        font={
            "color": "#FFFFFF"
        },
        showlegend=False,
        hovermode="x",
        xaxis={
            "range": [
                0,
                metadata["display_end"]
            ],
            "tickmode": "array",
            "tickvals": tick_values,
            "ticktext": tick_text,
            "tickfont": {
                "size": (
                    10
                    if metadata[
                        "has_extra_time"
                    ]
                    else 12
                ),
                "color": "#FFFFFF"
            },
            "showgrid": False,
            "showline": True,
            "linecolor": "#FFFFFF",
            "zeroline": False,
            "automargin": True
        },
        yaxis={
            "range": [
                -vertical_limit,
                vertical_limit
            ],
            "showticklabels": False,
            "showgrid": False,
            "showline": True,
            "linecolor": "#FFFFFF",
            "zeroline": False
        }
    )

    team1_flag = get_flag_uri(
        team1,
        banderas_img
    )

    team2_flag = get_flag_uri(
        team2,
        banderas_img
    )

    if team1_flag:

        figure.add_layout_image({
            "source": team1_flag,
            "xref": "paper",
            "yref": "paper",
            "x": -0.085,
            "y": 0.76,
            "sizex": 0.075,
            "sizey": 0.075,
            "xanchor": "center",
            "yanchor": "middle",
            "sizing": "contain",
            "layer": "above"
        })

    if team2_flag:

        figure.add_layout_image({
            "source": team2_flag,
            "xref": "paper",
            "yref": "paper",
            "x": -0.085,
            "y": 0.24,
            "sizex": 0.075,
            "sizey": 0.075,
            "xanchor": "center",
            "yanchor": "middle",
            "sizing": "contain",
            "layer": "above"
        })

    frame_left = -0.17
    frame_right = 1.06
    frame_bottom = -0.27
    frame_top = 1.38

    figure.add_shape(
        type="rect",
        x0=frame_left,
        x1=frame_right,
        y0=frame_bottom,
        y1=frame_top,
        line={
            "color": "#D4AF37",
            "width": 6
        },
        fillcolor="rgba(0,0,0,0)",
        xref="paper",
        yref="paper",
        layer="above"
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )
