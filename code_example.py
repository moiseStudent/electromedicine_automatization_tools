import pandas as pd
from googlesearch import search
import time

# 1. Cargar el inventario
file_path = 'inventario_equipos.xlsx'
df = pd.read_excel(file_path)

# Asumiendo que tus columnas se llaman 'Equipo' y 'Marca'
def buscar_manual(row):
    query = f"manual de usuario pdf {row['Equipo']} {row['Marca']} filetype:pdf"
    print(f"Buscando: {query}")
    
    try:
        # Buscamos el primer link que devuelva Google
        for j in search(query, tld="com", num=1, stop=1, pause=2):
            return j
    except Exception as e:
        return "Error en búsqueda"

# 2. Aplicar la búsqueda (limitado a los primeros 5 para probar)
# Nota: La salud mental de tu script depende de no ser bloqueado por Google; usa pausas.
df['Link_Manual'] = df.head(5).apply(buscar_manual, axis=1)

# 3. Guardar progreso
df.to_excel('inventario_con_manuales.xlsx', index=False)
print("Proceso completado.")



## Made for the main 


import pandas as pd
from pathlib import Path

class ElectromedicinaManager:
    def __init__(self, inventory_path):
        self.df = pd.read_csv(inventory_path)
        self.base_path = Path("Inventario_Equipos")

    def create_folder_structure(self):
        """Crea una carpeta por equipo basada en Modelo y Serial."""
        for _, row in self.df.iterrows():
            # Limpiamos nombres para evitar errores de sistema de archivos
            folder_name = f"{row['Marca']}_{row['Modelo']}_{row['Serial']}".replace("/", "-")
            path = self.base_path / folder_name
            path.mkdir(parents=True, exist_ok=True)
            print(f"Directorio verificado: {path}")

    def scrape_manuals(self):
        """
        Lógica de scraping (Placeholder). 
        Sugerencia: Google Search API o búsqueda directa en sitios de fabricantes.
        """
        for _, row in self.df.iterrows():
            query = f"Manual de servicio {row['Marca']} {row['Modelo']} filetype:pdf"
            # Aquí integrarías Selenium o requests
            print(f"Buscando manual para: {row['Modelo']}...")

    def generate_report(self):
        """Fase 2: Generación de reportes en PDF o Excel."""
        pass

# Ejecución
if __name__ == "__main__":
    manager = ElectromedicinaManager("inventario.csv")
    manager.create_folder_structure()




### This is for the block in the scraping search
import requests

url = "https://ejemplo.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://www.google.com/"
}

response = requests.get(url, headers=headers)
print(response.status_code)

session = requests.Session()
session.headers.update(headers)
response = session.get(url)




### Dictionary 

dic = {
    "equipo":[1,2,3],
    "marca":[1,2,3],
    "modelo":[1,2,3]
}



import pandas as pd

class ElectromedicineManager:
    def __init__(self, inventory_path):
        self.inventory_path = inventory_path
        # Leemos el archivo una sola vez
        self.inventory = pd.read_excel(self.inventory_path)
        
        # Usamos la variable ya cargada en memoria
        print("Inventario cargado exitosamente:")
        print(self.inventory.head()) # .head() para no saturar la consola




        import pandas as pd

class ElectromedicineManager:
    def __init__(self, inventory_path):
        self.inventory_path = inventory_path
        self.inventory_df = pd.read_excel(self.inventory_path)
        self.data_dict = [] # Aquí guardaremos la lista de diccionarios

    def estructurar_datos(self):
        """
        Convierte el DataFrame (o datos de scraping) en una lista 
        de diccionarios optimizada.
        """
        # .to_dict(orient='records') es el truco de ingeniería clave aquí
        self.data_dict = self.inventory_df.to_dict(orient='records')
        return self.data_dict

    def agregar_equipo_scraped(self, nombre, modelo, precio):
        """
        Si haces scraping, puedes añadir elementos individualmente 
        manteniendo la consistencia.
        """
        nuevo_item = {
            "nombre": nombre,
            "modelo": modelo,
            "precio": precio,
            "fuente": "Web Scraping"
        }
        self.data_dict.append(nuevo_item)


        import pandas as pd

class ElectromedicineManager:
    def __init__(self, inventory_path):
        self.inventory_path = inventory_path
        self.inventory_df = pd.read_excel(self.inventory_path)
        self.data_dict = [] # Aquí guardaremos la lista de diccionarios

    def estructurar_datos(self):
        """
        Convierte el DataFrame (o datos de scraping) en una lista 
        de diccionarios optimizada.
        """
        # .to_dict(orient='records') es el truco de ingeniería clave aquí
        self.data_dict = self.inventory_df.to_dict(orient='records')
        return self.data_dict

    def agregar_equipo_scraped(self, nombre, modelo, precio):
        """
        Si haces scraping, puedes añadir elementos individualmente 
        manteniendo la consistencia.
        """
        nuevo_item = {
            "nombre": nombre,
            "modelo": modelo,
            "precio": precio,
            "fuente": "Web Scraping"
        }
        self.data_dict.append(nuevo_item)




#### Human Scraping
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0"
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Referer": "https://www.google.com/",
    "DNT": "1", # Do Not Track
}

### Coldown and human behavior
import time
import random

# Delay aleatorio entre 2 y 7 segundos
time.sleep(random.uniform(2, 7))

### Traffic throughout proxy

ip = input("What do you want to search for: ")

for url in search(ip, timeout=5):
    print(url)

    search()




#### Busqueda de manuales 
def generar_query(fila):
    # Formato ideal: "Marca Modelo Tipo de Equipo service manual filetype:pdf"
    query = f"{fila['Marca']} {fila['Modelo']} {fila['Nombre_Equipo']} manual PDF"
    return query.replace(" ", "+") # Formato para URL


### Micode
import time
import random
from curl_cffi import requests
from bs4 import BeautifulSoup

class ElectromedicineManager:
    

    def buscar_manuales(self):
        self.inventory['Link_Manual'] = "No encontrado"
        
        for index, row in self.inventory.iterrows():
            query = f"{row['Marca']}+{row['Modelo']}+service+manual+pdf"
            url = f"https://html.duckduckgo.com/html/?q={query}"
            
            try:
                # Usamos impersonate para evitar el error 403
                response = requests.get(url, impersonate="chrome110")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Buscamos el primer link de resultado que parezca útil
                    resultado = soup.find('a', class_='result__a')
                    if resultado:
                        self.inventory.at[index, 'Link_Manual'] = resultado['href']
                
                print(f"Procesado: {row['Modelo']}")
                # Jitter para no ser bloqueado (salud del script)
                time.sleep(random.uniform(2, 5)) 
                
            except Exception as e:
                print(f"Error en {row['Modelo']}: {e}")


### Marca - modelo - manual



### Organizacion con Os sytem

import os
import time
import random
from curl_cffi import requests # Mejor para evitar bloqueos 403

class ElectromedicineManager:
    def __init__(self, inventory_path, base_folder="Manuales_Equipos"):
        self.inventory_path = inventory_path
        # ... (carga de pandas ya realizada)
        self.base_folder = base_folder
        
        # Crear la carpeta raíz si no existe
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

    def descargar_y_organizar(self):
        for index, row in self.inventory.iterrows():
            # 1. Definir rutas (Limpieza de strings para evitar caracteres ilegales en Windows/Linux)
            marca = str(row['Marca']).strip().replace("/", "-")
            modelo = str(row['Modelo']).strip().replace("/", "-")
            
            ruta_carpeta = os.path.join(self.base_folder, marca, modelo)
            os.makedirs(ruta_carpeta, exist_ok=True)
            
            # 2. Obtener el link (asumiendo que ya tienes el link del paso anterior)
            url_manual = row.get('Link_Manual')
            if not url_manual or url_manual == "No encontrado":
                continue

            # 3. Descarga con streaming (eficiente para archivos grandes/PDFs)
            nombre_archivo = f"Manual_{modelo}.pdf"
            ruta_final = os.path.join(ruta_carpeta, nombre_archivo)

            try:
                # Usamos impersonate para saltar el error 403 del servidor de archivos
                with requests.get(url_manual, impersonate="chrome110", stream=True) as r:
                    r.raise_for_status()
                    with open(ruta_final, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                print(f"✅ Guardado: {marca} - {modelo}")
                
                # Gestión de tiempo para no saturar el ancho de banda del servidor
                time.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"❌ Error descargando {modelo}: {e}")

### Verificar que los archivos sean pdfs



# Cambia tu importación así:
from curl_cffi import requests

# Ahora 'session' sí tendrá el método necesario
session = requests.Session()
response = session.get(url, impersonate="chrome110")