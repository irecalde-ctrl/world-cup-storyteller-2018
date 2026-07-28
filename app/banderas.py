
import base64
import os
import unicodedata
from pathlib import Path


def normalizar_nombre(nombre):

    nombre = unicodedata.normalize("NFD", nombre)

    nombre = "".join(
        caracter
        for caracter in nombre
        if unicodedata.category(caracter) != "Mn"
    )

    return nombre.lower().strip()


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

FLAGS_DIR = (
    PROJECT_ROOT
    / "assets"
    / "flags"
)


def cargar_banderas():

    banderas_encontradas = {}

    if not FLAGS_DIR.exists():
        return banderas_encontradas

    for ruta in sorted(
        FLAGS_DIR.iterdir()
    ):

        if not ruta.is_file():
            continue

        extension = (
            ruta.suffix
            .lower()
            .lstrip(".")
        )

        if extension == "jpg":
            extension = "jpeg"

        if extension not in [
            "png",
            "jpeg",
            "webp"
        ]:
            continue

        with ruta.open(
            "rb"
        ) as archivo:

            imagen_base64 = (
                base64
                .b64encode(
                    archivo.read()
                )
                .decode()
            )

        clave = normalizar_nombre(
            ruta.stem
        )

        banderas_encontradas[clave] = (
            f"data:image/{extension};"
            f"base64,{imagen_base64}"
        )

    return banderas_encontradas


def obtener_bandera_html(
    nombre_pais,
    banderas_img,
    css_class="bandera-partido"
):

    clave = normalizar_nombre(nombre_pais)
    imagen = banderas_img.get(clave, "")

    if not imagen:
        return ""

    return (
        f'<img '
        f'src="{imagen}" '
        f'class="{css_class}" '
        f'alt="Bandera de {nombre_pais}">'
    )
