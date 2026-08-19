# Sistema de recomendación de artistas para eventos musicales en Chile

## Descripción del proyecto

Este proyecto desarrolla un sistema de apoyo a la decisión para la selección de artistas en eventos musicales en Chile, utilizando datos de rankings diarios de Spotify.

El objetivo no es predecir directamente ventas de entradas, asistencia real ni capacidad de llenar recintos, sino identificar perfiles de artistas según su comportamiento digital local en Spotify Chile.

Para ello, se analizan variables relacionadas con:

- Apariciones en rankings.
- Canciones únicas.
- Ranking promedio.
- Popularidad promedio.
- Movimiento diario.
- Movimiento semanal.
- Permanencia en rankings.
- Puntaje de posición en Chile.

El proyecto combina técnicas de aprendizaje no supervisado, aprendizaje supervisado y Deep Learning:

- Análisis exploratorio y preparación de datos.
- Individualización de artistas y tratamiento de colaboraciones.
- Construcción de métricas agregadas por artista.
- Escalamiento de variables mediante `StandardScaler`.
- Reducción de dimensionalidad mediante PCA.
- Segmentación mediante K-Means.
- Comparación con DBSCAN.
- Construcción de una etiqueta técnica derivada de los clusters.
- Comparación de Logistic Regression, KNN y Random Forest.
- Comparación de tres arquitecturas MLP.
- Refinamiento de la arquitectura seleccionada.
- Comparación de estrategias de balanceo.
- Evaluación sobre datos no vistos.
- Explicabilidad mediante SHAP.
- Integración en una aplicación funcional desarrollada con Streamlit.

---

## Integrantes

**Grupo 2 - Aprendizaje de Máquina**

- Diego Mulatti Morales
- Alejandro Ortega Aranda
- Omar Sanhueza Becar

---

## Objetivo del proyecto

Construir un sistema de apoyo a la toma de decisiones para la selección de artistas en eventos musicales en Chile, utilizando señales de desempeño digital observadas en Spotify Chile.

El sistema busca caracterizar artistas mediante perfiles de comportamiento digital local obtenidos a partir de clustering.

De forma complementaria, se utiliza una etiqueta técnica binaria derivada de estos perfiles para evaluar y comparar modelos supervisados. Esta etiqueta no representa capacidad real de convocatoria.

---

## Alcance del modelo

El sistema permite analizar patrones de comportamiento digital de artistas en Spotify Chile, pero no mide convocatoria real de forma directa.

Por lo tanto, los resultados deben interpretarse como señales digitales complementarias y no como una predicción de:

- Venta de entradas.
- Asistencia a conciertos.
- Capacidad de llenar recintos.
- Éxito comercial real.
- Convocatoria efectiva en festivales u otros eventos.

Para estimar convocatoria real sería necesario incorporar fuentes externas como:

- Venta histórica de entradas.
- Asistencia a eventos.
- Capacidad de recintos.
- Costos de contratación.
- Redes sociales.
- YouTube.
- Apple Music.
- Tendencias de búsqueda.
- Historial de presentaciones.
- Características del público objetivo.

---

## Dataset utilizado

El dataset utilizado corresponde a:

**Top Spotify Songs in 73 Countries (Daily Updated)**

Fuente: Kaggle  
Archivo utilizado:

```text
universal_top_spotify_songs.csv
```

Por su tamaño, el archivo CSV original **no se incluye directamente en el repositorio**.

Para ejecutar desde cero el notebook, el archivo debe descargarse desde Kaggle y ubicarse en la misma carpeta del notebook.

### Datos utilizados para Chile

El filtrado inicial del mercado chileno produjo:

- **29.105 registros iniciales.**
- **599 canciones únicas identificadas mediante `spotify_id`.**
- **540 nombres distintos de canciones.**
- **408 valores originales en la columna `artists`.**
- **29.103 registros utilizados después de la depuración.**
- **597 canciones únicas identificadas mediante `spotify_id` después de la depuración.**
- **20.099 registros correspondientes a colaboraciones o combinaciones de artistas antes de la expansión.**
- **59.232 registros después de individualizar los participantes de las colaboraciones.**
- **351 entidades artísticas individualizadas como unidad final de análisis.**

La diferencia entre los **540 nombres distintos de canciones** y los **599 identificadores únicos de Spotify** se debe a que el nombre visible de una canción no constituye por sí solo un identificador único. Para el análisis se utiliza `spotify_id` como criterio para identificar canciones únicas.

Después de la depuración se conservaron **597 `spotify_id` únicos**.

Las colaboraciones fueron separadas para representar individualmente a cada participante. Se utilizó un criterio de atribución completa de la información asociada a la aparición de cada canción.

La expansión de las colaboraciones incrementó el número de filas desde 29.103 registros depurados hasta 59.232 registros individualizados, debido a que una misma aparición puede generar una fila para cada artista participante.

---

## Variables del modelo

La base final utiliza ocho variables numéricas agregadas por artista:

- `apariciones_chile`
- `canciones_unicas_chile`
- `rank_promedio_chile`
- `popularidad_promedio`
- `movimiento_diario_promedio`
- `movimiento_semanal_promedio`
- `permanencia_dias`
- `puntaje_posicion_chile`

Estas variables representan dimensiones de presencia, repertorio, posicionamiento, popularidad, dinámica temporal y permanencia dentro de Spotify Chile.

Antes del modelamiento fueron estandarizadas mediante `StandardScaler`.

---

## Tecnologías utilizadas

El proyecto fue desarrollado en Python y utiliza principalmente:

- pandas
- numpy
- scikit-learn
- scipy
- matplotlib
- tensorflow
- shap
- streamlit
- tqdm
- ipywidgets

---

## Estructura del repositorio

La estructura principal del proyecto es:

```text
acif104_s9_equipo2/
│
├── app/
│   ├── app.py
│   └── backend.py
│
├── artifacts/
│   ├── artistas_modelo.csv
│   ├── importancia_shap.csv
│   ├── kmeans_final.pkl
│   ├── metadata_modelo.json
│   ├── metricas_modelo.json
│   ├── modelo_mlp_final.keras
│   ├── pca_final.pkl
│   ├── scaler_clustering.pkl
│   └── scaler_mlp.pkl
│
├── resultados_arquitecturas/
│
├── resultados_refinamiento/
│
├── spotify_artistas_chile_eda.ipynb
├── requirements.txt
└── README.md
```

El dataset original:

```text
universal_top_spotify_songs.csv
```

debe descargarse por separado para ejecutar desde cero el notebook de procesamiento y entrenamiento.

---

## Instalación del entorno

Para ejecutar el proyecto se recomienda crear un entorno virtual.

### 1. Crear entorno virtual

En Windows:

```bash
python -m venv venv
```

### 2. Activar entorno virtual

```bash
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución del notebook

Para reproducir el flujo completo de procesamiento y modelamiento, abrir:

```text
spotify_artistas_chile_eda.ipynb
```

Luego ejecutar las celdas en orden desde el inicio.

Para ejecutar desde cero es necesario que:

```text
universal_top_spotify_songs.csv
```

se encuentre en la ubicación esperada por el notebook.

El notebook realiza:

- Preparación y limpieza de datos.
- Tratamiento de colaboraciones.
- Construcción de la base individualizada por artista.
- Generación de variables agregadas.
- Estandarización.
- PCA.
- Clustering.
- Comparación de modelos clásicos.
- Entrenamiento y refinamiento de la MLP.
- Evaluación.
- Análisis SHAP.
- Exportación de artefactos para la aplicación.

---

## Ejecución de la aplicación

Una vez instaladas las dependencias y disponibles los artefactos necesarios, la aplicación puede iniciarse desde la raíz del repositorio mediante:

```bash
python -m streamlit run app/app.py
```

Streamlit iniciará la aplicación y permitirá acceder a ella desde el navegador local.

---

## Arquitectura de la solución

La aplicación utiliza una arquitectura modular:

```text
Notebook de procesamiento y modelamiento
                ↓
             artifacts/
                ↓
           app/backend.py
                ↓
             app/app.py
                ↓
        Aplicación Streamlit
                ↓
              Usuario
```

El notebook concentra el procesamiento, entrenamiento, evaluación y explicabilidad.

Los resultados necesarios para la aplicación se exportan como artefactos reutilizables.

`app/backend.py` centraliza la lógica de acceso a estos recursos y `app/app.py` implementa la interfaz de usuario.

Esta separación evita volver a entrenar los modelos durante cada consulta.

---

## Flujo metodológico

### 1. Carga y revisión inicial del dataset

Se carga el dataset original y se revisan dimensiones, columnas, valores nulos, duplicados y características generales.

### 2. Filtrado de Spotify Chile

Se seleccionan los registros correspondientes a:

```text
country = CL
```

para concentrar el análisis en el mercado chileno.

El subconjunto inicial contiene:

```text
29.105 registros
599 spotify_id únicos
540 nombres distintos de canciones
408 valores originales de artists
```

Después de la depuración se obtienen:

```text
29.103 registros
597 spotify_id únicos
408 valores originales de artists
```

### 3. Tratamiento de artistas y colaboraciones

La columna `artists` puede contener un artista individual, un grupo o una combinación de artistas.

Las colaboraciones fueron separadas por participante y posteriormente expandidas para construir una unidad de análisis individualizada por artista.

La expansión genera:

```text
59.232 registros individualizados
```

que posteriormente son agregados para obtener:

```text
351 entidades artísticas
```

### 4. Construcción de variables

Se generan ocho variables agregadas por artista:

- Apariciones.
- Canciones únicas.
- Ranking promedio.
- Popularidad promedio.
- Movimiento diario promedio.
- Movimiento semanal promedio.
- Permanencia en días.
- Puntaje de posición en Chile.

Las canciones únicas son identificadas utilizando `spotify_id`.

### 5. Estandarización

Las ocho variables son estandarizadas mediante:

```text
StandardScaler
```

para reducir el efecto de las diferencias de escala.

### 6. Reducción dimensional mediante PCA

Se aplica Análisis de Componentes Principales.

Los primeros cuatro componentes permiten conservar aproximadamente:

```text
94,07 % de la varianza acumulada
```

La representación mediante PCA se utiliza para apoyar el análisis de estructura y clustering.

### 7. Clustering

Se comparan K-Means y DBSCAN.

#### K-Means

Con:

```text
k = 4
```

se obtiene un Silhouette Score aproximado de:

```text
0,4112
```

Los 351 artistas quedan distribuidos en cuatro clusters:

```text
Cluster 0: 157 artistas
Cluster 1: 47 artistas
Cluster 2:   8 artistas
Cluster 3: 139 artistas
```

Estos grupos fueron interpretados como:

- **Cluster 0:** Presencia sostenida.
- **Cluster 1:** Aparición puntual o emergente.
- **Cluster 2:** Consolidado de alto desempeño local.
- **Cluster 3:** Baja presencia o menor posicionamiento local.

#### DBSCAN

DBSCAN obtuvo un Silhouette Score superior:

```text
0,7503
```

pero concentró:

```text
343 artistas en un cluster
3 artistas en otro cluster
5 observaciones como ruido
```

Por esta razón, su segmentación resultó poco útil para generar perfiles diferenciados y se seleccionó K-Means.

---

## Construcción de la etiqueta técnica supervisada

Los perfiles de K-Means se reagruparon para construir una etiqueta técnica binaria.

```text
Clase 0: clusters 1 y 3 → 186 artistas
Clase 1: clusters 0 y 2 → 165 artistas
```

Interpretación:

- **Clase 0:** menor señal digital local.
- **Clase 1:** mayor señal digital local.

Esta etiqueta se utiliza exclusivamente para evaluar y comparar modelos supervisados.

**No constituye una medición externa de convocatoria, ventas ni asistencia a eventos.**

---

## Comparación de modelos supervisados clásicos

Se evaluaron tres modelos clásicos:

| Modelo | F1-score |
|---|---:|
| Logistic Regression | 0,9846 |
| KNN | 0,9697 |
| Random Forest | 0,9538 |

Logistic Regression obtuvo el mayor F1-score entre los modelos clásicos.

Random Forest fue conservado como referencia no lineal frente al modelo MLP.

---

## Comparación de arquitecturas MLP

Se evaluaron tres arquitecturas:

- `MLP_1_capa`
- `MLP_16_8`
- `MLP_32_16`

La selección se realizó utilizando exclusivamente el conjunto de validación.

El conjunto de prueba no participó en la selección de arquitectura.

La arquitectura seleccionada fue:

```text
MLP_16_8
```

con:

```text
Capas ocultas: [16, 8]
Activación: ReLU
Salida: Sigmoid
Optimizador: Adam
Learning rate: 0.001
Dropout: 0.30
Parámetros: 289
```

---

## Refinamiento de la arquitectura

Sobre `MLP_16_8` se compararon tres niveles de Dropout:

```text
D025 → Dropout 0.25
D030 → Dropout 0.30
D035 → Dropout 0.35
```

D035 obtuvo una pérdida de validación ligeramente menor que D030, pero la diferencia quedó dentro del umbral metodológico de equivalencia definido.

Se mantuvo:

```text
MLP_16_8_D030
```

por presentar la menor brecha absoluta entre pérdida de entrenamiento y validación y un equilibrio adecuado entre desempeño y estabilidad.

---

## Partición de los datos

La base supervisada contiene 351 artistas y fue dividida aproximadamente en proporción 60/20/20:

```text
Entrenamiento: 210
Validación:      70
Prueba:          71
```

El conjunto de prueba permaneció aislado durante la selección y refinamiento.

---

## Estrategias de balanceo

Se compararon cuatro escenarios:

- Sin balanceo.
- Ponderación de clases.
- Sobremuestreo.
- Submuestreo.

Distribución inicial del entrenamiento:

```text
Clase 0: 111
Clase 1:  99
```

Con sobremuestreo:

```text
Clase 0: 111
Clase 1: 111
```

Las métricas de clasificación fueron prácticamente equivalentes entre las estrategias.

El sobremuestreo fue seleccionado porque:

- Obtuvo la menor pérdida de validación.
- Equilibró las clases.
- Conservó todas las observaciones originales.

---

## Resultados principales

El modelo final fue evaluado sobre los:

```text
71 artistas
```

del conjunto de prueba.

### Métricas finales

```text
Accuracy:  0.9859
Precision: 1.0000
Recall:    0.9697
F1-score:  0.9846
AUC:       0.9992
```

### Matriz de confusión

```text
[[38, 0],
 [ 1, 32]]
```

Esto corresponde a:

- 38 verdaderos negativos.
- 0 falsos positivos.
- 1 falso negativo.
- 32 verdaderos positivos.

El modelo obtuvo 70 clasificaciones correctas sobre 71 observaciones.

Estos resultados muestran una alta consistencia con la etiqueta técnica derivada del clustering.

Sin embargo, **no representan validación externa de convocatoria real**, debido a que la etiqueta supervisada fue construida a partir de las mismas dimensiones utilizadas posteriormente como variables predictoras.

---

## Explicabilidad mediante SHAP

Se utiliza SHAP para analizar la contribución de las variables a la clasificación del modelo.

La importancia global media obtenida fue:

| Variable | Importancia SHAP media |
|---|---:|
| `puntaje_posicion_chile` | 0,189680 |
| `rank_promedio_chile` | 0,129339 |
| `movimiento_semanal_promedio` | 0,070992 |
| `permanencia_dias` | 0,065620 |
| `popularidad_promedio` | 0,037012 |
| `movimiento_diario_promedio` | 0,026034 |
| `apariciones_chile` | 0,020372 |
| `canciones_unicas_chile` | 0,007254 |

Los resultados indican que el modelo otorga mayor influencia al posicionamiento y a la estabilidad temporal que al volumen bruto de apariciones o canciones únicas.

---

## Aplicación frontend/backend

Los resultados fueron integrados en una aplicación funcional desarrollada mediante Streamlit.

La aplicación contiene cuatro vistas principales.

### Inicio

Presenta:

- Propósito de la herramienta.
- Alcance.
- Limitaciones.
- Cuatro perfiles de comportamiento digital local.

### Resumen general

Presenta una visión global de:

- 351 artistas.
- 4 perfiles.
- 8 variables.
- Distribución de artistas entre los perfiles.

### Explorar artistas

Permite:

- Buscar artistas por nombre.
- Filtrar por perfil.
- Consultar resultados.
- Seleccionar un artista.
- Revisar su información individual.

### Monitoreo técnico

Presenta:

- Métricas finales del modelo.
- Matriz de confusión.
- Configuración técnica.
- Información de explicabilidad.
- Estado de los artefactos utilizados.

La clasificación binaria empleada durante el entrenamiento se mantiene como información técnica interna.

Para usuarios finales se priorizan los cuatro perfiles de comportamiento digital local obtenidos mediante clustering.

---

## Reproducibilidad

`requirements.txt` documenta las dependencias utilizadas.

Los resultados publicados fueron generados con:

```text
Python 3.11.9
```

Se utiliza:

```text
Semilla = 42
```

en las etapas experimentales para favorecer la reproducibilidad.

Las principales condiciones utilizadas incluyen:

```text
Batch size: 32
Máximo de épocas: 150
EarlyStopping sobre val_loss
patience = 10
min_delta = 0.0001
restore_best_weights = True
Umbral de clasificación = 0.5
```

Las técnicas de balanceo se aplican exclusivamente al conjunto de entrenamiento.

El conjunto de validación se utiliza para seleccionar arquitectura e hiperparámetros.

El conjunto de prueba permanece aislado hasta la evaluación final.

Algunas métricas pueden presentar pequeñas variaciones entre entornos computacionales. En las ejecuciones verificadas se mantiene la selección de la arquitectura:

```text
MLP 16-8 con Dropout 0.30
```

---

## Archivos principales del repositorio

```text
spotify_artistas_chile_eda.ipynb
    Notebook principal de preparación, modelamiento y evaluación.

app/app.py
    Interfaz frontend desarrollada mediante Streamlit.

app/backend.py
    Capa lógica de acceso a datos, métricas y artefactos.

artifacts/
    Modelos, transformadores, métricas y datos procesados utilizados por la aplicación.

resultados_arquitecturas/
    Resultados y curvas de comparación de las tres arquitecturas MLP.

resultados_refinamiento/
    Resultados del refinamiento de la arquitectura MLP 16-8.

requirements.txt
    Dependencias necesarias para reproducir el proyecto.

README.md
    Documentación general, metodología y ejecución del sistema.
```

### Artefactos principales

La carpeta `artifacts/` contiene, entre otros:

```text
artistas_modelo.csv
importancia_shap.csv
kmeans_final.pkl
metadata_modelo.json
metricas_modelo.json
modelo_mlp_final.keras
pca_final.pkl
scaler_clustering.pkl
scaler_mlp.pkl
```

---

## Limitaciones

El proyecto presenta limitaciones importantes:

- Utiliza principalmente señales provenientes de Spotify.
- No incorpora ventas reales de entradas.
- No incluye asistencia histórica a eventos.
- No incorpora capacidad de recintos ni costos de contratación.
- No considera directamente ciudad, tipo de recinto, precio de entrada o características del público.
- Las colaboraciones utilizan un criterio de atribución completa para cada participante.
- La aplicación utiliza artefactos previamente generados y no incorpora automáticamente nuevos rankings.
- La variable objetivo supervisada deriva de los perfiles generados mediante clustering y no de datos externos de convocatoria.

Por estas razones, los resultados deben interpretarse como **señales de apoyo para la toma de decisiones**, no como una predicción definitiva de éxito comercial o asistencia.

---

## Mejoras futuras

Como líneas de evolución del proyecto se propone:

- Incorporar datos reales de venta de entradas y asistencia.
- Incorporar capacidad de recintos y costos de contratación.
- Integrar fuentes externas como redes sociales, YouTube, Apple Music y tendencias de búsqueda.
- Incorporar ubicación de audiencias e historial de presentaciones.
- Mejorar el tratamiento de colaboraciones mediante mecanismos más robustos de identificación y atribución.
- Automatizar la incorporación periódica de nuevos rankings.
- Implementar monitoreo de `data drift` y `concept drift`.
- Definir criterios de reentrenamiento.
- Evaluar el sistema frente a resultados reales de eventos.
- Construir en el futuro una variable objetivo externa que permita validar la relación entre señales digitales y asistencia presencial.

---

## Consideraciones finales

El proyecto demuestra cómo las técnicas de aprendizaje automático pueden transformar rankings diarios de Spotify en información agregada e interpretable para apoyar decisiones relacionadas con programación musical.

La principal contribución del sistema es la construcción de perfiles de comportamiento digital local por artista y su integración en una aplicación funcional de consulta.

El sistema no reemplaza el criterio experto de productores, organizadores o equipos de programación, pero puede complementar ese proceso mediante información objetiva derivada del comportamiento observado en Spotify Chile.