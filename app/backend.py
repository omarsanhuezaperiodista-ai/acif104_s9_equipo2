from pathlib import Path
import json

import joblib
import pandas as pd
import tensorflow as tf


# ============================================================
# Rutas generales del proyecto
# ============================================================

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
ARTIFACTS_DIR = ROOT_DIR / "artifacts"


# ============================================================
# Rutas de artefactos
# ============================================================

RUTA_ARTISTAS = ARTIFACTS_DIR / "artistas_modelo.csv"
RUTA_METRICAS = ARTIFACTS_DIR / "metricas_modelo.json"
RUTA_METADATA = ARTIFACTS_DIR / "metadata_modelo.json"
RUTA_SHAP = ARTIFACTS_DIR / "importancia_shap.csv"

RUTA_MODELO = ARTIFACTS_DIR / "modelo_mlp_final.keras"
RUTA_SCALER_MLP = ARTIFACTS_DIR / "scaler_mlp.pkl"
RUTA_SCALER_CLUSTERING = ARTIFACTS_DIR / "scaler_clustering.pkl"
RUTA_PCA = ARTIFACTS_DIR / "pca_final.pkl"
RUTA_KMEANS = ARTIFACTS_DIR / "kmeans_final.pkl"


# ============================================================
# Verificación de archivos
# ============================================================

def verificar_artefactos():
    """
    Verifica que los archivos necesarios para ejecutar el sistema
    se encuentren disponibles.
    """

    archivos = [
        RUTA_ARTISTAS,
        RUTA_METRICAS,
        RUTA_METADATA,
        RUTA_SHAP,
        RUTA_MODELO,
        RUTA_SCALER_MLP,
        RUTA_SCALER_CLUSTERING,
        RUTA_PCA,
        RUTA_KMEANS,
    ]

    faltantes = [
        str(archivo)
        for archivo in archivos
        if not archivo.exists()
    ]

    if faltantes:
        raise FileNotFoundError(
            "Faltan los siguientes artefactos:\n"
            + "\n".join(faltantes)
        )

    return True


# ============================================================
# Carga de datos y metadatos
# ============================================================

def cargar_artistas():
    """
    Carga la base consolidada de artistas utilizada por
    el frontend.
    """

    return pd.read_csv(RUTA_ARTISTAS)


def cargar_metricas():
    """
    Carga las métricas finales obtenidas sobre el conjunto Test.
    """

    with open(
        RUTA_METRICAS,
        "r",
        encoding="utf-8"
    ) as archivo:
        return json.load(archivo)


def cargar_metadata():
    """
    Carga información descriptiva del modelo seleccionado.
    """

    with open(
        RUTA_METADATA,
        "r",
        encoding="utf-8"
    ) as archivo:
        return json.load(archivo)


def cargar_importancia_shap():
    """
    Carga la importancia global de variables obtenida con SHAP.
    """

    return pd.read_csv(RUTA_SHAP)


# ============================================================
# Carga de modelos y objetos de preprocesamiento
# ============================================================

def cargar_modelo():
    """
    Carga el modelo MLP final refinado.
    """

    return tf.keras.models.load_model(
        RUTA_MODELO
    )


def cargar_scaler_mlp():
    """
    Carga el StandardScaler ajustado exclusivamente
    con el conjunto de entrenamiento.
    """

    return joblib.load(
        RUTA_SCALER_MLP
    )


def cargar_scaler_clustering():
    """
    Carga el escalador utilizado antes de PCA/K-Means.
    """

    return joblib.load(
        RUTA_SCALER_CLUSTERING
    )


def cargar_pca():
    """
    Carga el PCA de cuatro componentes.
    """

    return joblib.load(
        RUTA_PCA
    )


def cargar_kmeans():
    """
    Carga el modelo K-Means final de cuatro clusters.
    """

    return joblib.load(
        RUTA_KMEANS
    )


# ============================================================
# Funciones para el dashboard
# ============================================================

def obtener_resumen_dashboard():
    """
    Construye los principales indicadores que serán mostrados
    en el dashboard del frontend.
    """

    artistas = cargar_artistas()
    metricas = cargar_metricas()
    metadata = cargar_metadata()

    resumen = {
        "cantidad_artistas": len(artistas),
        "cantidad_variables": metricas["n_variables"],
        "cantidad_clusters": metadata["numero_clusters"],
        "modelo": metricas["modelo"],
        "accuracy": metricas["accuracy"],
        "precision": metricas["precision"],
        "recall": metricas["recall"],
        "f1_score": metricas["f1_score"],
        "auc": metricas["auc"],
    }

    return resumen


def obtener_distribucion_clusters():
    """
    Devuelve la cantidad de artistas pertenecientes a
    cada cluster.
    """

    artistas = cargar_artistas()

    return (
        artistas["perfil_cluster"]
        .value_counts()
        .rename_axis("perfil")
        .reset_index(name="cantidad")
    )


def obtener_distribucion_senal():
    """
    Devuelve la distribución de la señal digital predicha.
    """

    artistas = cargar_artistas()

    return (
        artistas["senal_predicha"]
        .value_counts()
        .rename_axis("senal")
        .reset_index(name="cantidad")
    )


# ============================================================
# Explorador de artistas
# ============================================================

def filtrar_artistas(
    texto="",
    cluster=None,
    senal=None
):
    """
    Permite filtrar artistas por nombre, cluster y señal digital.
    """

    datos = cargar_artistas().copy()

    if texto:
        datos = datos[
            datos["artists"]
            .str.contains(
                texto,
                case=False,
                na=False
            )
        ]

    if cluster is not None:
        datos = datos[
            datos["cluster"] == cluster
        ]

    if senal is not None:
        datos = datos[
            datos["senal_predicha"] == senal
        ]

    return datos


def obtener_artista(nombre_artista):
    """
    Recupera la información completa de un artista.
    """

    datos = cargar_artistas()

    coincidencia = datos[
        datos["artists"]
        .str.lower()
        .eq(nombre_artista.lower())
    ]

    if coincidencia.empty:
        return None

    return coincidencia.iloc[0].to_dict()


# ============================================================
# Predicción mediante el modelo final
# ============================================================

def predecir_desde_metricas(datos_artista):
    """
    Recibe las ocho variables del modelo y devuelve la
    probabilidad estimada de alta señal digital local.

    Esta predicción representa la etiqueta técnica construida
    a partir de Spotify Chile y no convocatoria real.
    """

    metadata = cargar_metadata()
    metricas = cargar_metricas()

    variables = metadata[
        "variables_modelo"
    ]

    entrada = pd.DataFrame(
        [datos_artista],
        columns=variables
    )

    scaler = cargar_scaler_mlp()
    modelo = cargar_modelo()

    entrada_escalada = scaler.transform(
        entrada
    )

    probabilidad = float(
        modelo.predict(
            entrada_escalada,
            verbose=0
        ).ravel()[0]
    )

    umbral = metricas[
        "umbral_clasificacion"
    ]

    clase = int(
        probabilidad >= umbral
    )

    if clase == 1:
        señal = "Alta señal digital local"
    else:
        señal = "Menor señal digital local"

    return {
        "probabilidad": probabilidad,
        "clase": clase,
        "senal": señal,
        "advertencia": (
            "La predicción corresponde a una etiqueta técnica "
            "basada en señales de Spotify Chile y no representa "
            "convocatoria real, venta de entradas ni asistencia."
        )
    }


# ============================================================
# Prueba básica del backend
# ============================================================

if __name__ == "__main__":

    print("Verificando backend...")
    print()

    verificar_artefactos()

    print("Artefactos disponibles: OK")
    print()

    resumen = obtener_resumen_dashboard()

    print("Resumen del sistema:")
    for clave, valor in resumen.items():
        print(f"- {clave}: {valor}")

    print()

    artistas = cargar_artistas()

    print(
        "Primer artista disponible:",
        artistas.iloc[0]["artists"]
    )

    print()
    print("Backend cargado correctamente.")