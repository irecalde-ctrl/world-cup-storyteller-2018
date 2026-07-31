FINAL_CONTENT_EDITORIAL = {
    ("France vs Argentina", "France", 2): (
        ["Di María", "Mercado", "Pavard"],
        "Final del partido: goles de Griezmann, Pavard, Mbappé, Di María, Mercado y Agüero.",
    ),
    ("France vs Argentina", "France", 1): (
        ["Kylian Mbappé", "doblete", "Pelé"],
        "Kylian Mbappé es el primer adolescente que marca al menos dos goles en un partido de un Mundial desde Pelé ante Suecia.",
    ),
    ("France vs Argentina", "Argentina", 1): (
        ["Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappé"],
        "Clasificación a cuartos de final y eliminación de Lionel Messi.",
    ),
    ("France vs Argentina", "Argentina", 2): (
        ["eliminación", "GOAT", "hinchas"],
        "Messi: «Todavía soy el GOAT». Siri: «¿Quién eres?».",
    ),
    ("Uruguay vs Portugal", "Uruguay", 2): (
        ["Cristiano Ronaldo", "Luis Suárez"],
        "Cristiano Ronaldo se enfrenta por primera vez a Uruguay en su carrera.",
    ),
    ("Uruguay vs Portugal", "Uruguay", 1): (
        ["pronósticos", "Ronaldo", "Pepe"],
        "Portugal–Uruguay: ¿marcará Ronaldo esta noche?",
    ),
    ("Uruguay vs Portugal", "Portugal", 1): (
        ["Lionel Messi", "Cristiano Ronaldo", "goles"],
        "Lionel Messi y Cristiano Ronaldo, protagonistas de las próximas noches.",
    ),
    ("Uruguay vs Portugal", "Portugal", 2): (
        ["eliminación", "figuras"],
        "Portugal es el siguiente: hoy dos grandes figuras se vuelven a casa.",
    ),
    ("Spain vs Russia", "Spain", 2): (
        ["tanda de penales", "cuartos de final", "victoria rusa"],
        "Rusia alcanza los cuartos de final tras vencer a España en la tanda de penales.",
    ),
    ("Spain vs Russia", "Spain", 1): (
        ["Alemania", "Argentina", "Portugal", "eliminación"],
        "Alemania, España, Argentina y Portugal quedaron eliminadas del Mundial.",
    ),
    ("Spain vs Russia", "Russia", 2): (
        ["tanda de penales", "cuartos de final", "victoria"],
        "Rusia venció a España por penales y avanzó a los cuartos de final del Mundial.",
    ),
    ("Spain vs Russia", "Russia", 1): (
        ["tanda de penales", "anfitrión", "clasificación"],
        "El anfitrión Rusia alcanza los cuartos de final tras superar a España por penales.",
    ),
    ("Croatia vs Denmark", "Croatia", 1): (
        ["tanda de penales", "clasificación", "drama"],
        "Croacia avanza tras imponerse en la tanda de penales.",
    ),
    ("Croatia vs Denmark", "Croatia", 2): (
        ["penales", "clasificación", "celebración"],
        "Croacia lo logró después de la tanda de penales.",
    ),
    ("Croatia vs Denmark", "Denmark", 1): (
        ["tanda de penales", "Schmeichel", "mala suerte"],
        "Qué mala suerte para Dinamarca. Qué tanda de penales.",
    ),
    ("Croatia vs Denmark", "Denmark", 2): (
        ["eliminación", "penales", "Mundial"],
        "Dinamarca quedó eliminada del Mundial por penales.",
    ),
    ("Colombia vs England", "Colombia", 2): (
        ["tanda de penales", "Inglaterra", "hinchas"],
        "Inglaterra ganó la tanda de penales ante Colombia.",
    ),
    ("Colombia vs England", "Colombia", 1): (
        ["penales", "cuartos de final", "clasificación"],
        "Inglaterra venció a Colombia por penales y avanzó a los cuartos de final.",
    ),
    ("Colombia vs England", "England", 2): (
        ["el fútbol vuelve a casa", "victoria", "Inglaterra"],
        "¡Inglaterra! El fútbol vuelve a casa.",
    ),
    ("Colombia vs England", "England", 1): (
        ["tanda de penales", "victoria", "Inglaterra"],
        "Inglaterra ganó la tanda de penales ante Colombia.",
    ),
    ("France vs Belgium", "France", 2): (
        ["semifinal", "Francia", "Bélgica"],
        "Mañana: semifinal entre Francia y Bélgica.",
    ),
    ("France vs Belgium", "France", 1): (
        ["transmisión en vivo", "Francia", "Bélgica"],
        "Mirá ahora la transmisión en vivo de Francia vs. Bélgica.",
    ),
    ("France vs Belgium", "Belgium", 2): (
        ["semifinal", "Francia", "Bélgica"],
        "Mañana: semifinal entre Francia y Bélgica.",
    ),
    ("France vs Belgium", "Belgium", 1): (
        ["transmisión en vivo", "Francia", "Bélgica"],
        "Mirá ahora la transmisión en vivo de Francia vs. Bélgica.",
    ),
    ("Croatia vs England", "Croatia", 2): (
        ["Ivan Perišić", "gol", "empate"],
        "¡Gol de Ivan Perišić! Inglaterra–Croacia.",
    ),
    ("Croatia vs England", "Croatia", 1): (
        ["el fútbol vuelve a casa", "tiempo extra", "Croacia"],
        "Inglaterra: «El fútbol vuelve a casa». Croacia: «Esta vez no».",
    ),
    ("Croatia vs England", "England", 2): (
        ["el fútbol vuelve a casa", "eliminación", "Croacia"],
        "El «Coming Home» queda para Inglaterra. Bien hecho, Croacia.",
    ),
    ("Croatia vs England", "England", 1): (
        ["Inglaterra", "final", "aliento"],
        "¡Vamos, Inglaterra! A buscar la final.",
    ),
    ("France vs Croatia", "France", 2): (
        ["diseño ganador", "Francia", "felicitaciones"],
        "Mi diseño ganador para celebrar a Francia. ¡Felicitaciones!",
    ),
    ("France vs Croatia", "France", 1): (
        ["campeones", "Francia", "felicitaciones"],
        "Francia gana el Mundial. ¡Felicitaciones a los campeones!",
    ),
    ("France vs Croatia", "Croatia", 1): (
        ["Luka Modrić", "Balón de Oro", "premio"],
        "Luka Modrić se queda con el Balón de Oro.",
    ),
    ("France vs Croatia", "Croatia", 2): (
        ["presidenta croata", "apoyo", "afecto", "abrazos"],
        "Lo que Nita Ambani representa para la IPL, la presidenta croata lo representa para este Mundial.",
    ),
}

applied_changes = 0
missing_changes = set(FINAL_CONTENT_EDITORIAL)

for match_name, content in MATCH_CONTENT_ANALYSIS.items():
    if not content.get("available", False):
        continue

    for team_key in ["team1", "team2"]:
        team_data = content[team_key]
        team_name = team_data["team"]

        for topic in team_data.get("topics", []):
            topic_number = topic.get(
                "topic",
                topic.get("topic_id", topic.get("id")),
            )
            editorial_key = (match_name, team_name, topic_number)

            if editorial_key not in FINAL_CONTENT_EDITORIAL:
                continue

            terms, translated_tweet = FINAL_CONTENT_EDITORIAL[editorial_key]
            topic["terms_display_es"] = terms
            topic["representative_tweet_es"] = translated_tweet

            applied_changes += 1
            missing_changes.discard(editorial_key)

print("✅ Correcciones aplicadas:", applied_changes)
print("✅ Correcciones faltantes:", len(missing_changes))

if missing_changes:
    print("Claves no encontradas:")
    for key in sorted(missing_changes):
        print("-", key)
