# ⚽ World Cup Storyteller 2018

> Reconstrucción de los partidos eliminatorios del Mundial de Rusia 2018 a través de la conversación registrada en Twitter.

## Descripción

World Cup Storyteller 2018 es una aplicación interactiva de periodismo de datos que permite revivir los 16 partidos de la fase eliminatoria del Mundial de Rusia 2018.

El proyecto combina:

- análisis de redes sociales;
- procesamiento de lenguaje natural;
- eventos futbolísticos históricos;
- visualizaciones interactivas;
- storytelling deportivo.

El objetivo no es solamente mostrar qué ocurrió en cada partido, sino reconstruir cómo fue vivido socialmente mientras estaba sucediendo.

## Experiencia de cada partido

Cada partido incluye:

1. Hero con resultado e información general.
2. Historia narrativa.
3. Pulso del partido en Twitter.
4. Share of Voice.
5. Clima emocional.
6. Ranking de protagonistas.
7. Tweets destacados.
8. Radiografía final.

## Arquitectura

```text
Dataset de Twitter
        ↓
Notebook de análisis
        ↓
16 paquetes JSON
        ↓
Aplicación Streamlit
```

El análisis pesado se ejecuta previamente. La aplicación consume archivos JSON procesados, por lo que no necesita descargar el dataset ni ejecutar modelos de NLP cada vez que un usuario entra.

## Calidad de los datos

El dataset no posee la misma cobertura temporal para todos los partidos.

La aplicación distingue entre:

- cobertura temporal parcial;
- análisis social sin línea temporal;
- muestra social limitada;
- partidos sin datos sociales.

Cuando no existe cobertura suficiente, la aplicación lo informa explícitamente y evita fabricar métricas o curvas temporales.

## Dataset

Dataset principal:

[World Cup 2018 Tweets — Kaggle](https://www.kaggle.com/datasets/rgupta09/world-cup-2018-tweets)

Contiene aproximadamente 530.000 tweets con fecha, texto, likes, retweets, hashtags y usuario.

El dataset original no está incluido en este repositorio.


## Fuentes y metodología de la V2

### Conversación social

La conversación social se reconstruye a partir del dataset
[World Cup 2018 Tweets — Kaggle](https://www.kaggle.com/datasets/rgupta09/world-cup-2018-tweets).

Este dataset contiene publicaciones asociadas con la fase eliminatoria del Mundial de Rusia 2018. Por ese motivo, el alcance del proyecto se mantiene en los 16 partidos comprendidos entre los octavos de final y la final. No se incorporan encuentros de la fase de grupos porque no existe una cobertura equivalente en la fuente utilizada.

La cobertura no es homogénea para todos los partidos. Algunos encuentros poseen registros parciales y otros no contienen tuits disponibles. La aplicación no completa ni infiere observaciones inexistentes: cuando la muestra no es suficiente, informa la limitación de manera explícita.

### Eventos deportivos

Los resultados, goles, tiempos suplementarios y tandas de penales se reconstruyen con
[StatsBomb Open Data](https://github.com/statsbomb/open-data).

La integración fue validada para los 16 partidos eliminatorios:

- 16 partidos relacionados y validados;
- 51 eventos principales;
- 5 partidos con tiempo suplementario;
- 4 tandas de penales;
- 39 ejecuciones registradas en tandas.

Los eventos deportivos se procesan durante la etapa de análisis y se exportan en los paquetes JSON consumidos por la aplicación.

### Análisis de contenido

El análisis temático se realiza por separado para cada selección mediante:

1. limpieza y normalización de los tuits;
2. construcción de representaciones TF-IDF;
3. extracción de dos temas mediante NMF;
4. cálculo del peso relativo de cada tema;
5. selección de términos y de un tuit representativo.

Se exige un mínimo de 200 tuits asociados con cada selección para publicar el resultado. Con este criterio, el análisis temático se encuentra disponible en 8 de los 16 partidos. En los demás encuentros, la interfaz comunica que la muestra es insuficiente.

Los modelos se ejecutan sobre los textos originales en inglés. Para la presentación se utiliza traducción automática al español con `Helsinki-NLP/opus-mt-en-es` (MarianMT), complementada con un glosario futbolístico y una normalización editorial de las etiquetas visibles. Los términos y tuits originales se conservan dentro de los paquetes para permitir su auditoría.

### Arquitectura de publicación

El procesamiento de StatsBomb, el análisis NLP y las traducciones se realizan fuera de Streamlit. El resultado se guarda en 16 paquetes JSON con versión de esquema `2.1`.

La aplicación web consume estos archivos preprocesados, por lo que no necesita descargar modelos de lenguaje ni consultar servicios externos durante su ejecución. Esta decisión reduce el tiempo de carga y mejora la reproducibilidad del proyecto.


## Estructura

```text
WorldCupStoryteller_RELEASE/
│
├── app/
│   ├── app.py
│   ├── app_config.py
│   ├── banderas.py
│   ├── chart_config.py
│   ├── data_loader.py
│   ├── match_charts.py
│   └── match_components.py
│
├── assets/
│   ├── flags/
│   ├── portada.webp
│   └── estadio.jpg
│
├── data/
│   ├── index.json
│   └── matches/
│
├── notebooks/
│   ├── Mundial2018_FINAL.ipynb
│   └── Mundial2018_App_FINAL.ipynb
│
├── requirements.txt
└── README.md
```

## Ejecución local

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
streamlit run app/app.py
```

## Tecnologías

- Python
- Streamlit
- Plotly
- Pandas
- NumPy
- Google Colab
- Kaggle

## Principio de diseño

Este proyecto no busca responder solamente:

> ¿Qué pasó?

Busca responder:

> ¿Cómo reaccionó la gente mientras estaba ocurriendo?

La narrativa es tan importante como los datos.
