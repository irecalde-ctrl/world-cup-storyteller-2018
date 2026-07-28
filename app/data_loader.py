
import json
import os
from pathlib import Path
from functools import lru_cache


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DEFAULT_DATA_DIR = (
    PROJECT_ROOT
    / "data"
)


class MatchDataError(RuntimeError):
    """Error controlado al cargar los datos de los partidos."""


def get_data_dir():

    return os.environ.get(
        "WORLDCUP_DATA_DIR",
        str(DEFAULT_DATA_DIR)
    )


def read_json(file_path):

    if not os.path.exists(file_path):
        raise MatchDataError(
            f"No se encontró el archivo: {file_path}"
        )

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError as error:

        raise MatchDataError(
            f"JSON inválido en {file_path}: {error}"
        ) from error


@lru_cache(maxsize=1)
def load_match_index():

    index_path = os.path.join(
        get_data_dir(),
        "index.json"
    )

    index_data = read_json(
        index_path
    )

    matches = index_data.get(
        "matches",
        []
    )

    if len(matches) != 16:
        raise MatchDataError(
            "index.json debe contener exactamente "
            f"16 partidos y contiene {len(matches)}"
        )

    return index_data


@lru_cache(maxsize=32)
def load_match_package(slug):

    index_data = load_match_index()

    match_record = next(
        (
            match
            for match in index_data["matches"]
            if match["slug"] == slug
        ),
        None
    )

    if match_record is None:
        raise MatchDataError(
            f"No existe un partido con slug: {slug}"
        )

    relative_path = match_record[
        "file"
    ]

    package_path = os.path.join(
        get_data_dir(),
        relative_path
    )

    package = read_json(
        package_path
    )

    if package.get("slug") != slug:
        raise MatchDataError(
            f"El slug interno no coincide en {package_path}"
        )

    return package


def get_matches_by_stage(stage_key):

    index_data = load_match_index()

    return [
        match
        for match in index_data["matches"]
        if match["stage"]["key"] == stage_key
    ]


def clear_data_cache():

    load_match_index.cache_clear()
    load_match_package.cache_clear()
