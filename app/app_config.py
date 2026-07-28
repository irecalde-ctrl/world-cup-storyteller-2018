
# =========================================================
# NOMBRES VISIBLES DE LOS EQUIPOS
# =========================================================

TEAM_NAMES_ES = {
    "France": "Francia",
    "Argentina": "Argentina",
    "Uruguay": "Uruguay",
    "Portugal": "Portugal",
    "Spain": "España",
    "Russia": "Rusia",
    "Croatia": "Croacia",
    "Denmark": "Dinamarca",
    "Brazil": "Brasil",
    "Mexico": "México",
    "Belgium": "Bélgica",
    "Japan": "Japón",
    "Sweden": "Suecia",
    "Switzerland": "Suiza",
    "Colombia": "Colombia",
    "England": "Inglaterra"
}


# =========================================================
# ORDEN Y PRESENTACIÓN DE LAS FASES
# =========================================================

STAGE_CONFIG = {
    "octavos": {
        "stage_key": "round_of_16",
        "nombre": "Octavos de final",
        "cantidad": "8 partidos"
    },
    "cuartos": {
        "stage_key": "quarterfinals",
        "nombre": "Cuartos de final",
        "cantidad": "4 partidos"
    },
    "semifinales": {
        "stage_key": "semifinals",
        "nombre": "Semifinales",
        "cantidad": "2 partidos"
    },
    "tercer-puesto": {
        "stage_key": "third_place",
        "nombre": "Tercer puesto",
        "cantidad": "1 partido"
    },
    "final": {
        "stage_key": "final",
        "nombre": "Final",
        "cantidad": "1 partido"
    }
}


def get_team_name_es(team_name):

    return TEAM_NAMES_ES.get(
        team_name,
        team_name
    )
