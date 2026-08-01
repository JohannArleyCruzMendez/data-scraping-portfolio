# Proyecto 1: Web Scraper Multi-página de Libros 📚

Este proyecto forma parte de mi portafolio como **Data & Scraping Specialist**. Consiste en un script desarrollado en Python para la extracción automatizada de datos desde una plataforma web de catálogo de libros.

## 🚀 Características
- **Conexión HTTP robusta:** Uso de la librería `requests` para validar el estado de las páginas web.
- **Parseo de HTML:** Interpretación y navegación de la estructura web utilizando `BeautifulSoup`.
- **Paginación automatizada:** Recorrido dinámico a través de múltiples páginas del sitio web para recolectar un volumen mayor de datos.
- **Exportación de datos:** Almacenamiento estructurado de la información extraída (Títulos y Precios) en un archivo `.csv` dentro de la carpeta `outputs/`.

## 🛠️ Tecnologías Utilizadas
- **Python 3.x**
- **Requests**
- **BeautifulSoup4**

## 📂 Estructura del Proyecto
```text
proyecto_1_scraping/
│
├── outputs/
│   └── libros.csv      # Archivo generado con los datos extraídos
├── scraper.py          # Script principal con la lógica de scraping y paginación
└── README.md           # Documentación del proyecto