### Test

"""

 def diagnostico_de_tablas(ruta):
     doc = Document(ruta)
     print(f"Total de tablas encontradas: {len(doc.tables)}") #

     for i, tabla in enumerate(doc.tables):
         print(f"\satoN--- Analizando Tabla {i} ---")
         for j, fila in enumerate(tabla.rows):
             # Extraemos el texto de cada celda para ver qué ve Python
             contenido = [celda.text.strip() for celda in fila.cells]
             print(f"Fila {j}: {contenido}") #

 diagnostico_de_tablas("20260105_01_INFORME_MA_DRAGER_FABIUS_0039.docx")


"""

"""
import os
import shutil

def organizar_archivos(directorio_origen, carpeta_destino, patron_nombre):
    """
   # Identifica y desplaza archivos que contienen un patrón específico.
    """
    # Verificación de existencia de directorios (Input Validation)
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Iteración sobre el set de datos
    for archivo in os.listdir(directorio_origen):
        # Lógica de filtrado (Case-insensitive)
        if patron_nombre.lower() in archivo.lower():
            ruta_inicial = os.path.join(directorio_origen, archivo)
            ruta_final = os.path.join(carpeta_destino, archivo)
            
            try:
                shutil.move(ruta_inicial, ruta_final)
                print(f"Desplazado: {archivo} -> {carpeta_destino}")
            except Exception as e:
                print(f"Error al mover {archivo}: {e}")

# Ejemplo de ejecución
# origen = "/home/usuario/documentos"
# destino = "/home/usuario/manuales_tecnicos"
# organizar_archivos(origen, destino, "Manual")
"""