# Sistema de recomendación de artistas para eventos musicales en Chile

## Descripción del proyecto

Este proyecto desarrolla un sistema de análisis y recomendación de artistas con potencial de selección para eventos musicales en Chile, utilizando datos de rankings diarios de Spotify.

El objetivo no es predecir directamente ventas de entradas, asistencia real ni capacidad de llenar recintos, sino identificar perfiles de artistas según su señal digital local en Spotify Chile. Para ello, se analizan variables como apariciones en rankings, permanencia, ranking promedio, popularidad, movimientos diarios y semanales, y puntaje de posición.

El proyecto combina técnicas de aprendizaje no supervisado y supervisado:

- Análisis exploratorio de datos.
- Agregación de métricas por artista.
- Escalamiento de variables.
- Reducción de dimensionalidad con PCA.
- Segmentación mediante K-Means.
- Construcción de una etiqueta técnica derivada de clusters.
- Entrenamiento de una red neuronal MLP.
- Comparación de estrategias de balanceo.
- Evaluación con métricas de clasificación.
- Explicabilidad del modelo mediante SHAP.
- Propuesta conceptual de frontend y backend.

## Integrantes

Grupo 2 - Aprendizaje de Máquina

- Diego Mulatti Morales
- Alejandro Ortega Aranda
- Omar Sanhueza Becar

## Dataset utilizado

El dataset utilizado corresponde a:

**Top Spotify Songs in 73 Countries (Daily Updated)**  
Fuente: Kaggle  
Archivo utilizado: `universal_top_spotify_songs.csv`

Por su tamaño, el archivo CSV original **no se incluye directamente en el repositorio**. Para ejecutar el notebook, el archivo debe descargarse desde Kaggle y ubicarse en la misma carpeta del notebook.

La estructura esperada es:

    omarunab/
    │
    ├── spotify_artistas_chile_eda.ipynb
    ├── requirements.txt
    ├── README.md
    ├── resultados_arquitecturas/
    │   ├── comparacion_arquitecturas.json
    │   ├── resumen_arquitecturas.md
    │   ├── MLP_16_8_perdida.png
    │   ├── MLP_16_8_exactitud.png
    │   ├── MLP_32_16_perdida.png
    │   ├── MLP_32_16_exactitud.png
    │   ├── MLP_1_capa_perdida.png
    │   └── MLP_1_capa_exactitud.png
    └── universal_top_spotify_songs.csv

## Objetivo del proyecto

Construir un sistema de apoyo a la toma de decisiones para la selección de artistas en eventos musicales en Chile, utilizando datos de desempeño digital en Spotify Chile.

El sistema busca clasificar artistas según una etiqueta técnica de mayor o menor señal digital local, construida a partir de perfiles obtenidos mediante clustering.

## Alcance del modelo

El modelo desarrollado permite analizar patrones de desempeño en Spotify Chile, pero no mide convocatoria real de forma directa.

Por lo tanto, los resultados deben interpretarse como una clasificación técnica basada en señales digitales disponibles en el dataset, y no como una predicción de:

- Venta de entradas.
- Asistencia a conciertos.
- Capacidad de llenar recintos.
- Éxito comercial real.
- Convocatoria en festivales, casinos, eventos comunales o espacios específicos.

Para estimar convocatoria real sería necesario incorporar otras fuentes de datos, como venta histórica de tickets, redes sociales, YouTube, Apple Music, rankings radiales, Billboard, TikTok, ciudad, tipo de recinto, precio de entradas y características del público objetivo.

## Tecnologías utilizadas

El proyecto fue desarrollado en Python, utilizando principalmente las siguientes librerías:

- pandas
- numpy
- scikit-learn
- scipy
- matplotlib
- tensorflow
- shap
- tqdm
- ipywidgets

## Instalación del entorno

Para ejecutar el proyecto, se recomienda crear un entorno virtual.

### 1. Crear entorno virtual

En Windows:

    python -m venv venv

### 2. Activar entorno virtual

    venv\Scripts\activate

### 3. Instalar dependencias

    pip install -r requirements.txt

## Ejecución del notebook

Una vez instalado el entorno y descargado el dataset, abrir el archivo:

    spotify_artistas_chile_eda.ipynb

Luego ejecutar las celdas en orden desde el inicio.

Es importante que el archivo:

    universal_top_spotify_songs.csv

esté ubicado en la misma carpeta que el notebook.

## Reproducibilidad

`requirements.txt` fija las versiones de las librerías utilizadas y los resultados publicados se generaron con Python 3.11.9. Las métricas exactas de entrenamiento pueden variar levemente al usar otra versión de Python o un procesador diferente. Debido a que las diferencias entre las arquitecturas son pequeñas, tanto las métricas como el orden del ranking podrían variar ligeramente entre entornos; por ello, no se presupone que la arquitectura seleccionada sea necesariamente la misma en todas las ejecuciones.

## Flujo metodológico

El desarrollo del proyecto se organiza en las siguientes etapas:

### 1. Carga y revisión inicial del dataset

Se carga el dataset original de Spotify y se revisan dimensiones, columnas, valores nulos, duplicados y estadísticas generales.

### 2. Filtrado de datos de Chile

Se filtran los registros correspondientes a Chile para enfocar el análisis en el mercado local.

### 3. Construcción de base agregada por artista

Se agrupan los datos por artista, generando variables como:

- Apariciones en rankings de Chile.
- Canciones únicas.
- Ranking promedio.
- Popularidad promedio.
- Movimiento diario promedio.
- Movimiento semanal promedio.
- Permanencia en días.
- Puntaje de posición en Chile.

### 4. Análisis no supervisado

Se aplican técnicas de reducción de dimensionalidad y clustering:

- PCA para representar la información en componentes principales.
- K-Means para segmentar artistas en perfiles de desempeño.

### 5. Construcción de etiqueta técnica

A partir de los clusters obtenidos, se construye una variable objetivo binaria que representa mayor o menor señal digital local en Spotify Chile.

Esta etiqueta no corresponde a convocatoria real, sino a una clasificación técnica derivada del comportamiento observado en el dataset.

### 6. Entrenamiento de red neuronal MLP

Se entrena una red neuronal de tipo Perceptrón Multicapa para clasificar artistas según la etiqueta técnica construida.

El modelo utiliza:

- Capas densas.
- Función de activación ReLU.
- Dropout.
- Salida sigmoide.
- Optimizador Adam.
- Función de pérdida binary crossentropy.

### 7. Comparación de estrategias de balanceo

Se comparan cuatro escenarios:

- Modelo sin balanceo.
- Modelo con ponderación de clases.
- Modelo con sobremuestreo.
- Modelo con submuestreo.

La comparación se realiza con métricas como:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- AUC.

### 8. Comparación experimental de tres arquitecturas MLP

Se comparan las arquitecturas `MLP_16_8`, `MLP_32_16` y `MLP_1_capa` usando el mismo conjunto de entrenamiento sobremuestreado y el mismo conjunto de validación. El modelo final se selecciona únicamente con validación, priorizando menor pérdida de validación, mayor F1 y mayor AUC. El conjunto de prueba no participa en esta selección y se reserva para la evaluación final.

### 9. Evaluación final

Luego de comparar las arquitecturas, se adopta el modelo seleccionado exclusivamente a partir del conjunto de validación.

El modelo final se evalúa sobre el conjunto de prueba, utilizando métricas de clasificación y matriz de confusión.

### 10. Explicabilidad con SHAP

Se utiliza SHAP para interpretar qué variables influyen más en las predicciones del modelo.

Esto permite observar la importancia de variables como:

- Ranking promedio en Chile.
- Puntaje de posición.
- Permanencia en rankings.
- Apariciones en Chile.
- Movimiento semanal promedio.

### 11. Revisión de casos particulares

Se revisan artistas específicos del conjunto de prueba para analizar si las predicciones son coherentes con sus métricas de desempeño digital en Spotify Chile.

### 12. Limitaciones y mejoras futuras

Se documentan las principales limitaciones del modelo y se proponen mejoras, como integrar datos de otras plataformas, redes sociales, ventas de entradas y características reales de eventos.

## Resultados principales

Modelo seleccionado: MLP_16_8

Resultados sobre los 71 artistas del conjunto de prueba:

    Accuracy:  0.9859
    Precision: 1.0000
    Recall:    0.9697
    F1-score:  0.9846
    AUC:       0.9992

Matriz de confusión:

    [[38, 0],
     [1, 32]]

Estos resultados corresponden a los 71 artistas del conjunto de prueba y a la ejecución incluida en el repositorio. Indican que el modelo logra reproducir adecuadamente la etiqueta técnica construida a partir de los clusters. Sin embargo, no deben interpretarse como una medición directa de convocatoria real.

## Explicabilidad del modelo

El análisis SHAP permite identificar las variables que más influyen en la clasificación del modelo.

Entre las variables más relevantes se encuentran:

- `rank_promedio_chile`
- `puntaje_posicion_chile`
- `movimiento_semanal_promedio`
- `permanencia_dias`
- `apariciones_chile`

Esto muestra que el modelo basa sus predicciones principalmente en variables asociadas al posicionamiento, permanencia y presencia en rankings diarios de Spotify Chile.

## Propuesta frontend/backend

Además del notebook de modelamiento, el proyecto considera una propuesta conceptual de sistema compuesta por frontend y backend.

### Backend

El backend corresponde al flujo de procesamiento y modelamiento desarrollado en Python:

    Carga de datos → Limpieza → Agregación por artista → PCA/K-Means → Modelo MLP → Métricas → SHAP → Resultados

Este componente sería responsable de procesar los datos, generar predicciones, calcular métricas y entregar resultados explicables.

### Frontend

El frontend corresponde a un mockup de interfaz no funcional, pensado para usuarios como productoras, equipos de marketing u organizadores de eventos.

La interfaz propuesta permitiría:

- Cargar o seleccionar datos.
- Revisar un dashboard general.
- Filtrar artistas.
- Consultar rankings recomendados.
- Revisar el detalle de cada artista.
- Visualizar explicaciones del modelo mediante métricas y SHAP.

## Limitaciones

El modelo presenta limitaciones importantes:

- Solo utiliza datos de Spotify.
- No incorpora Apple Music, YouTube, TikTok, Billboard, rankings radiales ni redes sociales.
- No incluye ventas reales de entradas.
- No considera asistencia histórica a eventos.
- No incorpora ciudad, recinto, género del evento, precio de entrada ni público objetivo.
- La variable objetivo es técnica y deriva de clusters, no de datos reales de convocatoria.

Por esta razón, los resultados deben entenderse como señales de apoyo para la toma de decisiones, no como una predicción definitiva de éxito comercial.

## Mejoras futuras

Como mejoras futuras se propone:

- Incorporar datos de venta de entradas y asistencia real.
- Integrar fuentes externas como YouTube, Apple Music, TikTok, Instagram, Billboard y rankings radiales.
- Mejorar la desambiguación de nombres artísticos y la identificación de colaboraciones con reglas más robustas que una separación por comas.
- Aplicar validación cruzada.
- Comparar con otros modelos como Random Forest, Gradient Boosting o regresión logística.
- Desarrollar una aplicación funcional con backend y frontend conectados.
- Actualizar periódicamente el modelo con nuevos rankings diarios.

## Archivos del repositorio

    spotify_artistas_chile_eda.ipynb   Notebook principal del proyecto
    requirements.txt                   Dependencias necesarias
    README.md                          Documentación del proyecto

El archivo `universal_top_spotify_songs.csv` debe descargarse por separado desde Kaggle y ubicarse localmente en la carpeta del proyecto.

## Consideraciones finales

Este proyecto demuestra cómo las técnicas de aprendizaje automático pueden apoyar la selección de artistas para eventos musicales a partir de señales digitales observables.

El sistema no reemplaza el criterio experto de productores u organizadores, pero puede servir como herramienta complementaria para analizar tendencias, comparar artistas y justificar decisiones con datos.
