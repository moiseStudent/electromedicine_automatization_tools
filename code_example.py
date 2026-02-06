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
        
        # Carga flexible (Excel o CSV)
        if inventory_path.endswith('.xlsx'):
            self.df = pd.read_excel(inventory_path)
        else:
            self.df = pd.read_csv(inventory_path)
            
        print(f" Inventario cargado: {len(self.df)} equipos.")

    def filtrar_unicos(self):
        """Optimización: Buscar solo modelos distintos."""
        self.unique_df = self.df.drop_duplicates(subset=['Marca', 'Modelo']).copy()
        return self.unique_df

    def buscar_links_manuales(self):
        """Búsqueda de links."""
        self.unique_df['Link_Manual'] = "No encontrado"
        
        for index, row in self.unique_df.iterrows():
            query = f"{row['Marca']} {row['Modelo']} service manual filetype:pdf"
            url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            try:
                # Impersonate imita un navegador real (Chrome 110)
                response = requests.get(url, impersonate="chrome110", timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    resultado = soup.find('a', class_='result__a')
                    if resultado:
                        link = resultado['href']
                        self.unique_df.at[index, 'Link_Manual'] = link
                        print(f" Enlace hallado para {row['Modelo']}")
                
                time.sleep(random.uniform(2, 4))
            except Exception as e:
                print(f" Error en búsqueda de {row['Modelo']}: {e}")
        
        # Unir links al dataframe principal
        self.df = self.df.merge(
            self.unique_df[['Marca', 'Modelo', 'Link_Manual']], 
            on=['Marca', 'Modelo'], 
            how='left'
        )

    def descargar_y_organizar(self):
        """Función mejorada para forzar la descarga de archivos."""
        for index, row in self.df.iterrows():
            link = row.get('Link_Manual')
            
            # Validar que tengamos un link real
            if not link or "http" not in str(link) or link == "No encontrado":
                continue
            
            marca = str(row['Marca']).replace("/", "-").strip()
            modelo = str(row['Modelo']).replace("/", "-").strip()
            
            ruta_carpeta = self.output_folder / marca / modelo
            ruta_carpeta.mkdir(parents=True, exist_ok=True)
            
            # Nombre del archivo final
            ruta_archivo = ruta_carpeta / f"Manual_{modelo}.pdf"

            try:
                print(f" Intentando descargar: {modelo} desde {link[:50]}...")
                
                # Headers de navegación real para evitar carpetas vacías por bloqueo
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0 Safari/537.36",
                    "Accept": "application/pdf, */*"
                }

                # Realizar la petición de descarga
                with requests.get(link, impersonate="chrome110", headers=headers, stream=True, timeout=20) as r:
                    r.raise_for_status()
                    
                    # Escribir el archivo en el disco
                    with open(ruta_archivo, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024 * 64): # 64KB chunks
                            if chunk:
                                f.write(chunk)
                
                # Verificación de éxito: si el archivo pesa 0 bytes, algo salió mal
                if ruta_archivo.exists() and ruta_archivo.stat().st_size > 1000:
                    print(f" Descarga exitosa: {ruta_archivo.name} ({ruta_archivo.stat().st_size // 1024} KB)")
                else:
                    print(f" Archivo descargado vacío o muy pequeño para ser un PDF en {modelo}")
                    if ruta_archivo.exists(): ruta_archivo.unlink() # Borrar si falló

                time.sleep(random.uniform(1, 2))

            except Exception as e:
                print(f" Fallo crítico al descargar {modelo}: {e}")

    def finalizar(self):
        self.df.to_excel("inventario_con_links.xlsx", index=False)
        print("\n Proceso completado. Revisa la carpeta 'Manuales_Equipos'.")

# Ejecución
if __name__ == "__main__":
    # Cambia esto por el nombre real de tu archivo
    bot = InventoryAutomation("inventario_equipos.xlsx")
    bot.filtrar_unicos()
    bot.buscar_links_manuales()
    bot.descargar_y_organizar()
    bot.finalizar()