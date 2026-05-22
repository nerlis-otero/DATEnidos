# Análisis de Colombianos Detenidos en el Exterior (2018–2025)

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=Plotly&logoColor=white)

Este repositorio contiene el ecosistema analítico interactivo desarrollado para explorar, limpiar, procesar y modelar estadísticamente las dinámicas demográficas, temporales y espaciales de los ciudadanos colombianos privados de la libertad en el extranjero.

Proyecto académico presentado en la **FERIA DE PROYECTOS DE CIENCIA DE DATOS** de la **Universidad Tecnológica de Bolívar (UTB)**.

---

## Objetivos del Proyecto

1.  **Identificación Geográfica y Criminal:** Descubrir los principales países de reclusión y las tipologías delictivas de mayor concentración.
2.  **Análisis Demográfico:** Evaluar si existen disparidades estadísticamente significativas en la situación jurídica de los internos según su género y rango etario.
3.  **Modelado Temporal:** Estudiar la evolución de capturas mensuales entre 2018 y 2025, aislando el impacto de fenómenos globales como la pandemia por COVID-19.

---

## Estructura del Repositorio

| Archivo / Carpeta | Descripción |
| :--- | :--- |
| `dashboard.py` | Código fuente principal de la aplicación interactiva desarrollada en **Streamlit**. |
| `Analisis_Colombianos_Detenidos_v2.ipynb` | Jupyter Notebook con la exploración inicial, pipeline de limpieza y contrastes estadísticos. |
| `datos_limpios.csv` | Dataset depurado (Data Sample) listo para alimentar los gráficos del sistema. |

---

## Pipeline de Procesamiento y Metodología

### 1. Limpieza y Calidad de Datos
El dataset bruto provisto por el Portal de Datos Abiertos de la Cancillería (`datos.gov.co`) presentaba un alto índice de ruido estructural. Se aplicaron los siguientes tratamientos en Python:
* **Deduplicación:** Identificación y remoción de **32,598 registros duplicados**.
* **Corrección de Encoding:** Reparación de cadenas de texto corruptas causadas por codificaciones UTF-8 defectuosas (*e.g.*, de `ESPAA` a `ESPAÑA`).
* **Homogeneización Categórica:** Unificación de etiquetas ambiguas o inconsistentes en las variables de género y estatus procesal.
* **Casteo de Tipos:** Conversión formal de datos temporales (fechas de publicación) y numéricos (coordenadas espaciales).

### 2. Análisis Estadístico y Modelado
* **Contraste de Hipótesis ($\chi^2$):** Se ejecutó una prueba de Chi-cuadrado de Independencia sobre tablas de contingencia cruzada. El resultado arrojó un **$p$-valor $\ll 0.05$ ($p = 2.14 \times 10^{-14}$)**, rechazando la hipótesis nula ($H_0$) y demostrando que la situación jurídica final está significativamente asociada al perfil demográfico (género y edad).
* **Suavizamiento de Series Temporales:** Se implementaron **Medias Móviles Centradas (MM3)** sobre la tasa de capturas mensuales para mitigar el ruido blanco y evidenciar el quiebre estructural generado por el cierre de fronteras durante la crisis del COVID-19 (2020–2021).

---

## Descubrimientos e Insights Principales

* **Concentración Geográfica:** Tres países monopolizan la mayor densidad de reclusos colombianos en el extranjero: **España, Estados Unidos y Ecuador**.
* **Predominancia Penal:** El **Narcotráfico** constituye el delito líder absoluto, abarcando aproximadamente el **42% de los casos globales**.
* **Brecha de Género:** Los hombres representan el **79% del volumen total de detenciones** y reflejan porcentajes de condena formal sustancialmente más estrictos en comparación con las mujeres.

---

## Guía de Reproducción Local

Sigue estas instrucciones paso a paso para clonar este repositorio y ejecutar la aplicación interactiva en tu entorno local:

### 1. Requisitos Previos
Es necesario contar con **Python 3.9 o una versión superior** instalado en el sistema operativo.

### 2. Clonar el Proyecto
Abre tu consola de comandos (Terminal o CMD) y escribe:
```bash
git clone [https://github.com/nerlis-otero/DATEnidos.git](https://github.com/nerlis-otero/DATEnidos.git)
cd cdatproyecto1