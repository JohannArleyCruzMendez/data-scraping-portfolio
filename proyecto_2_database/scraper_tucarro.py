import requests
from pymongo import MongoClient

# 1. Tu cadena de conexión (reemplaza <db_password> por tu contraseña real)
MONGO_URI = "mongodb+srv://johann:@cluster-portafolio.1xdogjg.mongodb.net/?appName=Cluster-Portafolio"

def interceptar_y_guardar():
    print("Estableciendo conexión con MongoDB Atlas...")
    cliente = MongoClient(MONGO_URI)
    db = cliente['portafolio_scraping']
    # Creamos una nueva colección para separar estos datos de los de NHTSA
    coleccion = db['tucarro_modelos'] 
    
    # 2. Pega aquí la Request URL completa que copiaste de la pestaña Headers
   # 2. Pega aquí la Request URL completa
    url_interceptada = "https://www.tucarro.com.co/faceted-search/MCO/MOT/searchbox/BRAND/MODEL?MODEL=&category=MCO1744&BRAND=66811"
    
    # 3. Simulamos ser un navegador real usando el header User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Ejecutando petición a la API interna de TuCarro...")
    respuesta = requests.get(url_interceptada, headers=headers)
    
    if respuesta.status_code == 200:
        # Extraemos el JSON
        datos = respuesta.json()
        
        # Dependiendo de la estructura del JSON de MercadoLibre, la lista puede estar 
        # directamente en la raíz o bajo una clave (ej. a veces es una lista pura)
        # Asumiremos que es una lista de diccionarios para la iteración.
        if isinstance(datos, list) and len(datos) > 0:
            print(f"Se interceptaron {len(datos)} registros. Iniciando persistencia...")
            
            coleccion.delete_many({}) # Limpieza previa opcional
            coleccion.insert_many(datos)
            print("¡Operación exitosa! Tráfico interceptado y guardado en la nube.")
        elif isinstance(datos, dict):
            # Si el JSON es un solo objeto con listas anidadas, lo guardamos completo
            coleccion.insert_one(datos)
            print("¡Operación exitosa! Objeto JSON guardado en la nube.")
        else:
            print("La estructura del JSON está vacía o no es la esperada.")
            print("Estructura recibida:", datos)
            
    else:
        print(f"La petición fue bloqueada o falló. Código: {respuesta.status_code}")

if __name__ == "__main__":
    interceptar_y_guardar()