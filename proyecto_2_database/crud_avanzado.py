from pymongo import MongoClient

# 1. Conexión a tu clúster cloud
MONGO_URI = "mongodb+srv://johann:@cluster-portafolio.1xdogjg.mongodb.net/?appName=Cluster-Portafolio"

def operaciones_crud():
    print("Conectando a la arquitectura cloud de MongoDB Atlas...")
    cliente = MongoClient(MONGO_URI)
    db = cliente['portafolio_scraping']
    coleccion = db['tucarro_modelos']
    
    # ==========================================
    # 1. READ (Consultas Avanzadas)
    # ==========================================
    print("\n--- EJECUTANDO CONSULTA (READ) ---")
    # Filtraremos los vehículos cuyo campo 'weight' sea mayor a 100
    # Usamos el operador $gt (greater than)
    filtro_peso = {"weight": {"$gt": 100}}
    
    # projection nos permite traer solo los campos que nos interesan (0 oculta, 1 muestra)
    proyeccion = {"_id": 0, "label": 1, "weight": 1}
    
    resultados_lectura = coleccion.find(filtro_peso, proyeccion)
    
    print("Modelos de Mazda con 'weight' superior a 100:")
    modelos_pesados = list(resultados_lectura)
    for doc in modelos_pesados:
        print(f" - Modelo: {doc.get('label')} | Weight: {doc.get('weight')}")

    # ==========================================
    # 2. UPDATE (Actualización de Documentos)
    # ==========================================
    print("\n--- EJECUTANDO ACTUALIZACIÓN (UPDATE) ---")
    # Vamos a añadir un nuevo campo llamado 'revisado' a todos los documentos que filtramos antes
    # Usamos el operador $set para modificar o agregar un campo sin sobreescribir todo el documento
    resultado_update = coleccion.update_many(
        filtro_peso, 
        {"$set": {"auditado_por": "Pipeline Cloud", "estado": "Activo"}}
    )
    print(f"Documentos actualizados exitosamente: {resultado_update.modified_count}")

    # ==========================================
    # 3. DELETE (Borrado Estratégico)
    # ==========================================
    print("\n--- EJECUTANDO BORRADO (DELETE) ---")
    # Supongamos que queremos limpiar la base de datos eliminando modelos con weight muy bajo (menor a 25)
    # Usamos el operador $lt (less than)
    filtro_borrado = {"weight": {"$lt": 25}}
    
    resultado_delete = coleccion.delete_many(filtro_borrado)
    print(f"Documentos eliminados (weight < 25): {resultado_delete.deleted_count}")

    print("\n¡Ciclo CRUD completado con éxito!")

if __name__ == "__main__":
    operaciones_crud()