import pandas as pd
import os
import time
import random
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from curl_cffi import requests
from bs4 import BeautifulSoup

class InventoryAutomation:
    def __init__(self, file_path, output_folder="Manuales_Descargados"):
        self.file_path = file_path
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # Lista negra de dominios (pago o registro)
        self.blacklist = [
            'scribd.com', 'manualslib.com', 'issuu.com', 
            'pudn.com', 'buy-manual.com', 'service-manual.net'
        ]
        
        try:
            self.df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            self.df.columns = [c.strip() for c in self.df.columns]
            print(f"📦 Inventario cargado: {len(self.df)} registros.")
        except Exception as e:
            print(f"❌ Error crítico al cargar el archivo: {e}")
            sys.exit()

    def _es_link_valido(self, url):
        """Verifica si el link no está en la blacklist y tiene host."""
        if not url: return False
        parsed = urlparse(str(url))
        if not parsed.netloc: return False
        return not any(domain in parsed.netloc for domain in self.blacklist)

    def _mostrar_progreso(self, actual, total, prefijo='Progreso:', sufijo='Completado'):
        """Barra de progreso estilo terminal de ingeniería."""
        percent = ("{0:.1f}").format(100 * (actual / float(total)))
        filled_length = int(50 * actual // total)
        bar = '█' * filled_length + '-' * (50 - filled_length)
        sys.stdout.write(f'\r{prefijo} |{bar}| {percent}% {sufijo}')
        sys.stdout.flush()

    def procesar(self):
        # 1. Optimización de modelos únicos
        df_unicos = self.df.drop_duplicates(subset=['Marca', 'Modelo']).copy()
        df_unicos['Link_Manual'] = None
        total = len(df_unicos)
        
        print(f"🔍 Buscando manuales para {total} modelos únicos...")

        for i, (index, row) in enumerate(df_unicos.iterrows()):
            self._mostrar_progreso(i + 1, total)
            
            marca = str(row['Marca'])
            modelo = str(row['Modelo'])
            query = f"{marca} {modelo} service manual pdf"
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            try:
                # Impersonate Chrome para evitar 403
                resp = requests.get(search_url, impersonate="chrome110", timeout=15)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    links = soup.find_all('a', class_='result__a')
                    
                    for l in links:
                        raw_url = l['href']
                        # Limpiar redirección de DuckDuckGo
                        if "uddg=" in raw_url:
                            raw_url = parse_qs(urlparse(raw_url).query).get('uddg', [None])[0]
                        
                        # Validar contra blacklist y host
                        if self._es_link_valido(raw_url):
                            df_unicos.at[index, 'Link_Manual'] = raw_url
                            break # Tomar el primero que pase el filtro
                
                time.sleep(random.uniform(2, 4)) # Respeto al servidor
            except Exception:
                continue

        # 2. Unir links y descargar
        self.df = self.df.merge(df_unicos[['Marca', 'Modelo', 'Link_Manual']], on=['Marca', 'Modelo'], how='left')
        print("\n\n📂 Iniciando descargas...")
        self.descargar_archivos()

    def descargar_archivos(self):
        total_descargas = len(self.df)
        for i, (index, row) in enumerate(self.df.iterrows()):
            link = row.get('Link_Manual_y', row.get('Link_Manual'))
            
            if not self._es_link_valido(link):
                continue

            # Crear estructura de carpetas
            marca = re.sub(r'\W+', '', str(row['Marca']))
            modelo = re.sub(r'\W+', '', str(row['Modelo']))
            ruta_dir = self.output_folder / marca / modelo
            ruta_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = ruta_dir / f"Manual_{modelo}.pdf"
            
            if file_path.exists(): continue

            try:
                with requests.get(link, impersonate="chrome110", stream=True, timeout=20) as r:
                    if r.status_code == 200:
                        with open(file_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=65536):
                                f.write(chunk)
                
                # Si el archivo es muy pequeño (<2KB), suele ser un error HTML, borrarlo.
                if file_path.stat().st_size < 2048:
                    file_path.unlink()
            except Exception:
                pass
            
            self._mostrar_progreso(i + 1, total_descargas, prefijo='Descarga:')

    def finalizar(self):
        self.df.to_excel("Resultado_Inventario.xlsx", index=False)
        print("\n\n✅ Proceso completado con éxito.")

if __name__ == "__main__":
    bot = InventoryAutomation("inventario_equipos.xlsx")
    bot.procesar()
    bot.finalizar()