import pandas as pd
import os
import time
import random
from pathlib import Path
from curl_cffi import requests
from bs4 import BeautifulSoup

class InventoryAutomation:
    def __init__(self, inventory_path, output_folder="Manuales_Equipos"):
        self.inventory_path = inventory_path
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # Cargar inventario
        if inventory_path.endswith('.xlsx'):
            self.df = pd.read_excel(inventory_path)
        else:
            self.df = pd.read_csv(inventory_path)
            
        print(f" Inventario cargado: {len(self.df)} equipos detectados.")

    def filtrar_unicos(self):
        """
        Optimización de Ingeniería: 
        Filtra equipos únicos por Marca y Modelo para no buscar 500 veces lo mismo.
        """
        self.unique_df = self.df.drop_duplicates(subset=['Marca', 'Modelo']).copy()
        print(f" Equipos únicos a buscar: {len(self.unique_df)} (ahorro de {len(self.df) - len(self.unique_df)} búsquedas).")
        return self.unique_df

    def buscar_links_manuales(self):
        """Scraping usando DuckDuckGo para evitar el fuerte bloqueo de Google."""
        self.unique_df['Link_Manual'] = "No encontrado"
        
        for index, row in self.unique_df.iterrows():
            marca = str(row['Marca']).strip()
            modelo = str(row['Modelo']).strip()
            query = f"{marca} {modelo} service manual pdf"
            
            # URL de búsqueda (DuckDuckGo versión HTML es más amigable para scraping)
            url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            try:
                # Impersonate Chrome 110 para evitar 403
                response = requests.get(url, impersonate="chrome110", timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Buscamos el primer resultado que contenga un link
                    resultado = soup.find('a', class_='result__a')
                    if resultado:
                        self.unique_df.at[index, 'Link_Manual'] = resultado['href']
                        print(f" Link encontrado para: {modelo}")
                
                # Jitter para salud mental del script y evitar ban de IP
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f" Error buscando {modelo}: {e}")
        
        # Merge de vuelta al DataFrame original para que todos los equipos tengan su link
        self.df = self.df.merge(
            self.unique_df[['Marca', 'Modelo', 'Link_Manual']], 
            on=['Marca', 'Modelo'], 
            how='left'
        )

    def descargar_y_organizar(self):
        """Descarga los archivos y los organiza en carpetas: Marca/Modelo/Manual.pdf"""
        for index, row in self.df.iterrows():
            link = row.get('Link_Manual')
            if not link or link == "No encontrado" or not str(link).startswith("http"):
                continue
            
            # Limpieza de nombres para sistema de archivos
            marca = str(row['Marca']).replace("/", "-").strip()
            modelo = str(row['Modelo']).replace("/", "-").strip()
            
            ruta_carpeta = self.output_folder / marca / modelo
            ruta_carpeta.mkdir(parents=True, exist_ok=True)
            
            ruta_archivo = ruta_carpeta / f"Manual_{modelo}.pdf"

            if ruta_archivo.exists():
                continue

            try:
                print(f" Descargando: {modelo}...")
                with requests.get(link, impersonate="chrome110", stream=True, timeout=15) as r:
                    r.raise_for_status()
                    
                    # Verificación básica de tipo de contenido
                    if 'application/pdf' in r.headers.get('Content-Type', '').lower() or link.endswith('.pdf'):
                        with open(ruta_archivo, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f" Guardado en: {ruta_archivo}")
                    else:
                        print(f" El link de {modelo} no parece ser un PDF directo.")
                
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f" Falló descarga de {modelo}: {e}")

    def guardar_progreso(self):
        output_path = "inventario_finalizado.xlsx"
        self.df.to_excel(output_path, index=False)
        print(f" Proceso terminado. Excel actualizado guardado como: {output_path}")

# --- Ejecución ---
if __name__ == "__main__":
    # Asegúrate de que el nombre del archivo coincida con el tuyo
    bot = InventoryAutomation("inventario_equipos.xlsx")
    
    # 1. Optimizar (Encontrar repetidos)
    bot.filtrar_unicos()
    
    # 2. Scraping (Solo equipos únicos)
    bot.buscar_links_manuales()
    
    # 3. Organización y descarga
    bot.descargar_y_organizar()
    
    # 4. Exportar resultados
    bot.guardar_progreso()