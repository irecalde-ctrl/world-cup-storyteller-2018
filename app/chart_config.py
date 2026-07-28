
# =========================================================
# COLORES DE LAS SELECCIONES
# =========================================================

TEAM_COLORS = {
    "France": "#2457D6",
    "Argentina": "#75AADB",
    "Uruguay": "#55BDE6",
    "Portugal": "#C92535",
    "Brazil": "#F7D117",
    "Mexico": "#168B52",
    "Belgium": "#E12C3D",
    "Japan": "#1D4E9E",
    "Spain": "#AA151B",
    "Russia": "#F4F4F4",
    "Croatia": "#F4F4F4",
    "Denmark": "#C8102E",
    "Sweden": "#1769AA",
    "Switzerland": "#D52B1E",
    "Colombia": "#FCD116",
    "England": "#F4F4F4"
}


MATCH_COLOR_OVERRIDES = {
    "Russia vs Croatia": {
        "Russia": "#F4F4F4",
        "Croatia": "#171717"
    },
    "Croatia vs England": {
        "Croatia": "#171717",
        "England": "#F4F4F4"
    }
}


# =========================================================
# EQUIPO DE CADA EVENTO HISTÓRICO
# =========================================================

EVENT_TEAM_ORDER = {
    "France vs Argentina": [
        "France",
        "Argentina",
        "Argentina",
        "France",
        "France",
        "France",
        "Argentina"
    ],
    "Uruguay vs Portugal": [
        "Uruguay",
        "Portugal",
        "Uruguay"
    ],
    "Spain vs Russia": [
        "Spain",
        "Russia",
        "Russia"
    ],
    "Croatia vs Denmark": [
        "Denmark",
        "Croatia",
        "Denmark",
        "Croatia"
    ],
    "Brazil vs Mexico": [
        "Brazil",
        "Brazil"
    ],
    "Belgium vs Japan": [
        "Japan",
        "Japan",
        "Belgium",
        "Belgium",
        "Belgium"
    ],
    "Sweden vs Switzerland": [
        "Sweden"
    ],
    "Colombia vs England": [
        "England",
        "Colombia",
        "England"
    ],
    "Uruguay vs France": [
        "France",
        "France"
    ],
    "Brazil vs Belgium": [
        "Belgium",
        "Belgium",
        "Brazil"
    ],
    "Russia vs Croatia": [
        "Russia",
        "Croatia",
        "Croatia",
        "Russia",
        "Croatia"
    ],
    "Sweden vs England": [
        "England",
        "England"
    ],
    "France vs Belgium": [
        "France"
    ],
    "Croatia vs England": [
        "England",
        "Croatia",
        "Croatia"
    ],
    "Belgium vs England (3rd Place)": [
        "Belgium",
        "Belgium"
    ],
    "France vs Croatia": [
        "France",
        "Croatia",
        "France",
        "France",
        "France",
        "Croatia"
    ]
}


EVENT_TYPE_OVERRIDES = {
    ("Spain vs Russia", 120): "shootout",
    ("Croatia vs Denmark", 116): "save",
    ("Croatia vs Denmark", 120): "shootout",
    ("Colombia vs England", 120): "shootout",
    ("Russia vs Croatia", 120): "shootout"
}


def hex_to_rgba(
    hex_color,
    opacity
):

    color = hex_color.lstrip("#")

    red = int(color[0:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)

    return (
        f"rgba("
        f"{red}, {green}, {blue}, {opacity}"
        f")"
    )


def get_visible_line_color(color):

    if color.upper() == "#171717":
        return "#A3A3A3"

    if color.upper() == "#F4F4F4":
        return "#FFFFFF"

    return color


def get_match_colors(
    match_name,
    team1,
    team2
):

    colors = TEAM_COLORS.copy()

    colors.update(
        MATCH_COLOR_OVERRIDES.get(
            match_name,
            {}
        )
    )

    return (
        colors.get(team1, "#2457D6"),
        colors.get(team2, "#75AADB")
    )


def get_event_team(
    match_name,
    event_index,
    event
):

    if event.get("team"):
        return event["team"]

    teams = EVENT_TEAM_ORDER.get(
        match_name,
        []
    )

    if event_index < len(teams):
        return teams[event_index]

    return None


def get_event_type(
    match_name,
    event
):

    if event.get("type"):
        return event["type"]

    event_key = (
        match_name,
        int(event["minute"])
    )

    if event_key in EVENT_TYPE_OVERRIDES:
        return EVENT_TYPE_OVERRIDES[
            event_key
        ]

    event_text = (
        event.get("event", "")
        .lower()
    )

    if "ataja" in event_text:
        return "save"

    if (
        "penales" in event_text
        or "tanda" in event_text
        or "clasifica" in event_text
    ):
        return "shootout"

    return "goal"
