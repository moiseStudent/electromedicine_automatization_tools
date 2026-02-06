import pandas as pd
import os
import time
import random
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from curl_cffi import requests
from bs4 import BeautifulSoup

class ElectromedicinaAutomation:
    def __init__(self, file_path, output_folder="Inventario_Manuales"):
        self.file_path = file_path
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # Carga de datos
        if file_path.endswith('.xlsx'):
            self.df = pd.read_excel(file_path)
        else:
            self.df = pd.read_csv(file_path)
        
        # Limpieza básica de nombres de columnas para evitar errores de acceso
        self.df.columns = [c.strip() for c in self.df.columns]
        print(f" Inventario cargado con {len(self.df)} registros.")

    def _limpiar_nombre(self, texto):
        """Elimina caracteres no permitidos en nombres de carpetas/archivos."""
        return re.sub(r'[\\/*?:"<>|]', "", str(texto)).strip()

    def procesar_inventario(self):
        """
        Paso 1: Filtrar equipos únicos por Marca y Modelo.
        Esto evita hacer 500 búsquedas si muchos equipos se repiten.
        """
        print("🔍 Identificando modelos únicos para optimizar tiempo...")
        # Suponiendo que tus columnas se llaman 'Marca' y 'Modelo'
        df_unicos = self.df.drop_duplicates(subset=['Marca', 'Modelo']).copy()
        df_unicos['Link_Manual'] = None
        
        total_unicos = len(df_unicos)
        print(f" De 500 registros, solo hay {total_unicos} modelos distintos. Iniciando scraping...")

        # Paso 2: Scraping de links
        for index, row in df_unicos.iterrows():
            marca = row['Marca']
            modelo = row['Modelo']
            query = f"{marca} {modelo} service manual pdf"
            
            # Buscador DuckDuckGo (menos agresivo con bloqueos que Google)
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            try:
                response = requests.get(search_url, impersonate="chrome110", timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Extraer el primer link de resultado
                    resultado = soup.find('a', class_='result__a')
                    if resultado:
                        raw_link = resultado['href']
                        
                        # DuckDuckGo a veces envuelve el link, intentamos extraer el real
                        if "uddg=" in raw_link:
                            actual_link = parse_qs(urlparse(raw_link).query).get('uddg', [None])[0]
                            df_unicos.at[index, 'Link_Manual'] = actual_link
                        else:
                            df_unicos.at[index, 'Link_Manual'] = raw_link
                            
                        print(f" Encontrado: {modelo} -> {df_unicos.at[index, 'Link_Manual'][:50]}...")
                
                # Jitter de ingeniería: pausa aleatoria para no ser baneado
                time.sleep(random.uniform(2.5, 5.0))
                
            except Exception as e:
                print(f" Error buscando {modelo}: {e}")

        # Paso 3: Re-mapear los links al DataFrame original (los 500 equipos)
        self.df = self.df.merge(df_unicos[['Marca', 'Modelo', 'Link_Manual']], on=['Marca', 'Modelo'], how='left')

    def descargar_y_organizar(self):
        """Paso 4: Descarga física y organización en carpetas."""
        print("\n Iniciando fase de descarga y organización...")
        
        for index, row in self.df.iterrows():
            link = row.get('Link_Manual_y') if 'Link_Manual_y' in self.df.columns else row.get('Link_Manual')
            
            # --- VALIDACIÓN DE INGENIERÍA ---
            if not link or pd.isna(link) or str(link).strip() == "":
                continue

            parsed_url = urlparse(str(link))
            if not parsed_url.netloc:
                print(f" Host inválido para {row['Modelo']}: {link}")
                continue
            # -------------------------------

            marca_folder = self._limpiar_nombre(row['Marca'])
            modelo_folder = self._limpiar_nombre(row['Modelo'])
            
            # Crear estructura: Inventario_Manuales/Marca/Modelo/
            ruta_destino = self.output_folder / marca_folder / modelo_folder
            ruta_destino.mkdir(parents=True, exist_ok=True)
            
            nombre_archivo = f"Manual_{modelo_folder}.pdf"
            ruta_completa = ruta_destino / nombre_archivo

            # Evitar descargar dos veces el mismo archivo
            if ruta_completa.exists() and ruta_completa.stat().st_size > 0:
                continue

            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0"}
                with requests.get(link, impersonate="chrome110", headers=headers, stream=True, timeout=20) as r:
                    r.raise_for_status()
                    
                    with open(ruta_completa, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024 * 128): # Chunks de 128KB
                            f.write(chunk)
                
                # Validación post-descarga
                if ruta_completa.stat().st_size < 1000: # Menos de 1KB es probablemente un error o HTML
                    print(f" Archivo corrupto o inválido para {row['Modelo']}. Eliminando...")
                    ruta_completa.unlink()
                else:
                    print(f" Descargado: {marca_folder} - {modelo_folder}")

            except Exception as e:
                print(f" Error descargando {row['Modelo']} desde {parsed_url.netloc}: {e}")

    def exportar_excel_final(self):
        output_path = "Inventario_Finalizado_Con_Links.xlsx"
        self.df.to_excel(output_path, index=False)
        print(f"\n Proceso terminado. Excel final: {output_path}")

# --- Ejecución del Programa ---
if __name__ == "__main__":
    # Sustituye por tu archivo real
    procesador = ElectromedicinaAutomation("inventario_equipos.xlsx")
    
    # Ejecución de flujo
    procesador.procesar_inventario()
    procesador.descargar_y_organizar()
    procesador.exportar_excel_final()