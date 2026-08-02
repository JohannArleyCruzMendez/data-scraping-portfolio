import requests
from pymongo import MongoClient

# 1. Cadena de conexión (recuerda poner tu contraseña real)
MONGO_URI = "mongodb+srv://johann:@cluster-portafolio.1xdogjg.mongodb.net/?appName=Cluster-Portafolio"

def obtener_y_guardar_vehiculos():
    print("Conectando a MongoDB Atlas...")
    cliente = MongoClient(MONGO_URI)
    db = cliente['portafolio_scraping']
    coleccion = db['vehiculos']
    
    # 2. Definimos el endpoint de la API
    # Usaremos Honda como ejemplo, pero puedes cambiarlo por Toyota, Ford, etc.
    marca = "honda"
    url_api = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{marca}?format=json"
    
    print(f"Consultando la API de NHTSA para la marca: {marca.upper()}...")
    respuesta = requests.get(url_api)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        resultados = datos.get('Results', [])
        
        print(f"Se encontraron {len(resultados)} modelos. Iniciando ingesta en MongoDB...")
        
        if resultados:
            # 3. Limpiamos la colección antes de insertar para evitar duplicados en cada prueba
            coleccion.delete_many({})
            
            # 4. Inserción masiva (bulk insert)
            coleccion.insert_many(resultados)
            print("¡Ingesta exitosa! Los documentos ya están persistidos en la nube.")
        else:
            print("La API no devolvió resultados.")
    else:
        print(f"Error en la API. Código de estado: {respuesta.status_code}")

if __name__ == "__main__":
    obtener_y_guardar_vehiculos()