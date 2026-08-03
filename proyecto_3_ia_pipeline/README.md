# Pipeline de Enriquecimiento de Datos con IA (MongoDB + Google Gemini)

Este proyecto implementa una arquitectura cloud automatizada para la extracción, procesamiento y enriquecimiento de datos no estructurados. Utiliza Python para orquestar la comunicación entre una base de datos NoSQL (MongoDB Atlas) y un motor de Inteligencia Artificial Generativa (Google Gemini), estandarizando datos provenientes de web scraping.

## 🚀 Arquitectura y Flujo de Trabajo (ETL)

1. **Extracción (Extract):** Conexión segura al clúster de MongoDB Atlas para recuperar documentos crudos de vehículos obtenidos mediante scraping.
2. **Transformación (Transform):** Los datos crudos se inyectan dinámicamente en un prompt estructurado enviado a la API de Google Gemini (`gemini-flash-latest`). El motor de IA actúa como un orquestador de datos, limpiando y estandarizando la información para devolver un JSON estricto.
3. **Carga (Load):** Mediante el operador `$set` de MongoDB, se realiza una actualización atómica (`update_one`). El JSON devuelto por la IA se incrusta como un sub-documento (`ia_enriquecimiento`) dentro del registro original, aprovechando el esquema flexible de MongoDB sin alterar los datos crudos.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.x
* **Base de Datos:** MongoDB Atlas (Modelo de Documentos)
* **Motor de IA:** Google Generative AI (Gemini)
* **Dependencias Principales:** `pymongo`, `google-generativeai`, `python-dotenv`, `certifi`

## ⚙️ Configuración y Despliegue Local

1. Clonar el repositorio.
2. Crear y activar un entorno virtual (`venv`).
3. Instalar las dependencias:
   ```bash
   pip install google-generativeai python-dotenv pymongo[srv] certifi