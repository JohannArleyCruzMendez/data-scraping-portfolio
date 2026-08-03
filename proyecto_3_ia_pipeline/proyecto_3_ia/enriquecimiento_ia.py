import os
import json
import certifi
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi


""" def listar_modelos_disponibles():
    print("Iniciando diagnóstico de la API...")
    
    # 1. Cargar credenciales
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # 2. Consultar al servidor los modelos disponibles
    print("\n--- MODELOS SOPORTADOS PARA GENERACIÓN DE TEXTO ---")
    for modelo in genai.list_models():
        if 'generateContent' in modelo.supported_generation_methods:
            print(f"- {modelo.name}")
    print("---------------------------------------------------")
    

if __name__ == "__main__":
    listar_modelos_disponibles() """
    
       
def inicializar_ia():
    """Configura y devuelve el modelo de Google Gemini."""
    print("Iniciando pipeline de automatización con IA...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Error CRÍTICO: No se encontró la API KEY.")
        
    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel('models/gemini-flash-latest')
    print("Motor de IA configurado correctamente.")
    return modelo


def conectar_mongodb():
    """Establece y verifica la conexión con MongoDB Atlas."""
    print("Conectando al clúster de MongoDB Atlas...")
    
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("Error CRÍTICO: No se encontró la MONGO_URI.")
        
    cliente = MongoClient(
        mongo_uri, 
        server_api=ServerApi('1'), 
        tlsCAFile=certifi.where()
    )
    
    try:
        cliente.admin.command('ping')
        print("¡Conexión exitosa a MongoDB Atlas confirmada!")
        return cliente
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


def enriquecer_datos(cliente, modelo):
    """Extrae un documento de la BD y lo procesa con la IA."""
    # 1. Apuntamos a la base de datos y colección exactas
    db = cliente['portafolio_scraping']
    coleccion = db['vehiculos']
    
    # 2. Extraemos un solo documento de prueba
    print("\nExtrayendo un vehículo de prueba de la base de datos...")
    vehiculo = coleccion.find_one()
    
    if not vehiculo:
        print("La colección está vacía. No hay datos para procesar.")
        return

    print(f"Vehículo encontrado (ID: {vehiculo.get('_id')}). Procesando...")
    
    # Excluimos el _id de Mongo porque no es relevante para la IA
    datos_crudos = {k: v for k, v in vehiculo.items() if k != '_id'}
    
    # 3. Diseñamos el Prompt para estructurar la información
    prompt = (
        
        "Eres un orquestador de datos. Analiza esta información "
        "cruda extraída mediante scraping de un vehículo:\n\n"
        f"{json.dumps(datos_crudos, ensure_ascii=False)}\n\n"
        "Extrae la información y devuélvela en formato JSON estricto "
        "con las siguientes claves: 'marca', 'modelo', 'precio' "
        "(si aplica), y una lista de 'caracteristicas_destacadas'. "
        "No incluyas texto adicional ni formato markdown."
    )
    
    # 4. Solicitamos la generación a Gemini
    respuesta = modelo.generate_content(prompt)
    
    print("\n--- DATOS ESTRUCTURADOS POR LA IA ---")
    print(respuesta.text)
    print("-------------------------------------")
    
    # 5. Guardar los datos enriquecidos de vuelta en MongoDB
    print("\nGuardando resultados en la base de datos...")
    try:
        # Limpiamos posibles caracteres 
        # de markdown que la IA suele añadir (```json)
        
        texto_limpio = respuesta.text.replace('```json', '').replace('```', '').strip()
        
        # Convertimos el string de la IA en un diccionario real de Python
        datos_estructurados = json.loads(texto_limpio)
        
        # Actualizamos el documento original usando su _id
        coleccion.update_one(
            {'_id': vehiculo['_id']},
            {'$set': {'ia_enriquecimiento': datos_estructurados}}
        )
        mensajeok = ("¡Éxito! Documento actualizado en MongoDB" 
                     "Atlas con los datos estructurados.")
        print(mensajeok)
    except json.JSONDecodeError:
        print("Error: La IA no devolvió un formato JSON válido.")
    except Exception as e:
        print(f"Error crítico al actualizar la base de datos: {e}")
        

if __name__ == "__main__":
    # Cargamos las variables del archivo .env
    load_dotenv()
    
    # 1. Inicializamos los motores
    modelo_ia = inicializar_ia()
    cliente_db = conectar_mongodb()
    
    # 2. Si ambas conexiones son exitosas, ejecutamos el pipeline
    if cliente_db and modelo_ia:
        enriquecer_datos(cliente_db, modelo_ia)