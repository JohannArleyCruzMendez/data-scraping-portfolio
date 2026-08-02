# Proyecto 2: Arquitectura Cloud, Interceptación de Tráfico y Operaciones CRUD NoSQL

Este proyecto es una demostración práctica de técnicas avanzadas de extracción de datos y su persistencia en bases de datos NoSQL basadas en la nube. Se enfoca en la ingesta de datos del sector automotriz superando las limitaciones del *web scraping* tradicional mediante el análisis de tráfico de red.

## 🚀 Objetivos del Proyecto
* Diseñar un flujo de ingesta de datos hacia un clúster de **MongoDB Atlas**.
* Aplicar técnicas de interceptación pasiva (XHR/Fetch) para consumir APIs internas no documentadas en entornos de producción (Ej. TuCarro/MercadoLibre).
* Gestionar grandes volúmenes de información mediante operaciones de inserción masiva.
* Ejecutar un ciclo completo de operaciones CRUD (Create, Read, Update, Delete) utilizando operadores nativos de MongoDB.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3
* **Base de Datos:** MongoDB Atlas (Cloud NoSQL)
* **Librerías Principales:** `pymongo`, `requests`
* **Herramientas de Análisis:** Browser Developer Tools (Network Inspector)

## 📂 Estructura y Fases del Proyecto

### Fase 1: Ingesta de APIs Públicas
Extracción de datos estructurados desde los endpoints públicos de la NHTSA (National Highway Traffic Safety Administration), implementando transformaciones ligeras antes de su persistencia en la nube.

### Fase 2: Interceptación Pasiva (Scraping Avanzado)
Análisis de tráfico de red en la plataforma TuCarro. En lugar de procesar HTML inestable, el script `scraper_tucarro.py` inyecta *headers* simulados (`User-Agent`) y consume directamente el *payload* JSON desde los microservicios internos de la plataforma, almacenando la carga útil mediante `insert_many()`.

### Fase 3: Operaciones CRUD Avanzadas
El script `crud_avanzado.py` demuestra la manipulación transaccional de los datos ingestados:
* **Read:** Uso de filtros con operadores de comparación (`$gt`) y optimización de red mediante **proyecciones**.
* **Update:** Enriquecimiento de documentos masivos (`update_many`) inyectando campos de auditoría con el operador `$set`.
* **Delete:** Limpieza estratégica de la base de datos eliminando registros fuera de rango (`$lt`).

## ⚙️ Cómo ejecutar este proyecto

1. Clona este repositorio.
2. Instala las dependencias necesarias:
   ```bash
   pip install requests pymongo