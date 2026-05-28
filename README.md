# ⚙️ Pipeline de Preprocesamiento de Datos CLI

Una herramienta interactiva de línea de comandos diseñada para facilitar el proceso de ETL (Extracción, Transformación y Carga) y Análisis Exploratorio de Datos (EDA). Permite cargar datasets, aplicar técnicas de limpieza y transformación matemática, visualizar los resultados y exportar el dataset final listo para modelos de Machine Learning.

## 🏛️ Arquitectura del Proyecto

El proyecto está diseñado bajo una **arquitectura modular** siguiendo el Principio de Responsabilidad Única (SRP), lo que garantiza un código limpio, mantenible y escalable:

* **`main.py`**: Controlador central (Orquestador). Gestiona la máquina de estados, la Interfaz de Usuario (UI) en consola y el manejo robusto de excepciones.
* **`data_io.py`**: Capa de Entrada/Salida. Aísla exclusivamente la lectura y exportación de archivos (CSV, Excel, SQLite).
* **`transformer.py`**: Motor lógico y matemático. Contiene algoritmos puros de Pandas para la imputación de nulos, codificación categórica, escalado y limpieza de valores atípicos (Outliers).
* **`visualizer.py`**: Motor gráfico. Encargado de renderizar histogramas, diagramas de dispersión comparativos y mapas de calor utilizando Matplotlib y Seaborn.
* **`test_*.py`**: Batería de pruebas unitarias para garantizar la calidad del software.

## 🛡️ Características Destacadas

* **Validación de Estados:** El sistema bloquea inteligentemente las opciones avanzadas del menú hasta que el usuario completa los pasos de preprocesamiento requeridos.
* **Manejo Robusto de Errores:** Incluye captura específica de excepciones (como `FileNotFoundError`, `sqlite3.Error`, `PermissionError` y `ValueError`) para evitar que la aplicación se cierre abruptamente ante inputs inválidos o archivos bloqueados.
* **Código Documentado:** Todos los módulos incluyen *Docstrings* detallados explicando los parámetros y retornos de cada función.

---

## 🛠️ Requisitos e Instalación

Asegúrate de tener instalado **Python 3.7 o superior**. 

1. **Clona o descarga este repositorio** en tu máquina local.
2. Abre una terminal y navega hasta la carpeta del proyecto.
3. Instala las dependencias necesarias ejecutando el siguiente comando:

```bash
pip install pandas openpyxl matplotlib seaborn



## Ejemplo de Uso (Flujo Típico)
El menú te guiará paso a paso:

1. Cargar Datos
Selecciona 1. Elige el formato de tu archivo (CSV, Excel o SQLite) y proporciona la ruta. El sistema mostrará la cantidad de filas, columnas y una vista previa segura.

2. Preprocesado de Datos
Selecciona 2 o navega por los submenús:

[2.1] Selección de columnas: Elige tus variables predictoras (features) y tu variable objetivo (target).

[2.2] Manejo de faltantes: Trata los valores NaN (eliminar fila, media, mediana, moda o constante).

[2.3] Transformación Categórica: Convierte texto a números usando One-Hot Encoding o Label Encoding.

[2.4] Normalización: Escala tus variables numéricas mediante Min-Max o Z-Score.

[2.5] Valores Atípicos: Detecta y limpia outliers utilizando el algoritmo de Rango Intercuartílico (IQR).

3. Visualización (Antes y Después)
Una vez completado el paso 2, selecciona 3 para acceder al panel gráfico:

Resumen estadístico tabular.

Histogramas de distribución.

Mapas de calor de correlaciones (Pearson).

Gráficos de dispersión comparativos: Muestra lado a lado los datos originales vs. los datos limpios y normalizados.

4. Exportar
Selecciona 4 para guardar tu dataset procesado en formato .csv o .xlsx (sin índices basura), dejándolo listo para entrenar modelos predictivos.

