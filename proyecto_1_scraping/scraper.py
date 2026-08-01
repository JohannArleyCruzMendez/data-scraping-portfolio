import csv
import requests
from bs4 import BeautifulSoup

# Definimos la ruta de salida de nuestro CSV
nombre_archivo = "proyecto_1_scraping/outputs/libros.csv"

# Abrimos el archivo CSV una sola vez para guardar todo el recorrido
with open(nombre_archivo, mode='w', encoding='utf-8') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(['Titulo', 'Precio']) # Cabecera
    
    # Bucle para recorrer múltiples páginas (ejemplo: de la 1 a la 3)
    for numero_pagina in range(1, 4):
        # Construimos la URL dinámica para cada página
        url = f"http://books.toscrape.com/catalogue/page-{numero_pagina}.html"
        print(f"Scrapeando la página {numero_pagina}: {url}")
        
        respuesta = requests.get(url)
        
        # Si la página existe (código 200), procesamos los datos
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            libros = soup.find_all('article', class_='product_pod')
            
            for libro in libros:
                titulo = libro.h3.a['title']
                precio = libro.find('p', class_='price_color').text
                escritor.writerow([titulo, precio])
        else:
            print(f"La página {numero_pagina} no existe o dio un error.")
            break

print("¡Proceso de paginación terminado con éxito!")

