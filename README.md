# ⚽ World Cup Storyteller 2018

## 🚀 Aplicación en vivo

[Explorar World Cup Storyteller 2018](https://world-cup-storyteller-2018.streamlit.app/)

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
