import requests
import warnings
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_water_news():
    url = "https://news.google.com/rss/search?q=tratamiento+de+aguas+industria&hl=es-419&gl=MX&ceid=MX:es-419"
    noticias = []
    warnings.filterwarnings("ignore")
    
    # Headers para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
        'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, timeout=10, verify=False, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'xml')  # Usar 'xml' en lugar de 'html.parser' para RSS
        
        articulos = soup.find_all('item', limit=4)
        
        for articulo in articulos:
            # 1. Extraemos las etiquetas
            titulo_tag = articulo.find('title')
            link_tag = articulo.find('link')
            pubdate_tag = articulo.find('pubDate')  # Nota: es 'pubDate' con 'D' mayúscula en RSS
            source_tag = articulo.find('source')
            
            # 2. Convertimos TODO a texto puro de Python con str() y limpiamos espacios con strip()
            titulo = str(titulo_tag.text).strip() if titulo_tag else "Sin título"
            
            # En RSS el link está directamente en el texto del tag
            enlace = str(link_tag.text).strip() if link_tag else "#"
            
            fecha_cruda = str(pubdate_tag.text).strip() if pubdate_tag else ""
            fecha = fecha_cruda[5:16] if len(fecha_cruda) > 16 else "Reciente"
            
            fuente = str(source_tag.text).strip() if source_tag else "Industry News"
            
            # 3. Guardamos en la lista 
            noticias.append({
                "title": titulo,
                "summary": f"📰 Fuente: {fuente} | 📅 Fecha: {fecha}",
                "link": enlace,
                "img": "https://images.unsplash.com/photo-1530053969600-caed2596d242?q=80&w=1074&auto=format&fit=crop" 
            })
            
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP {e.response.status_code}: Google News bloqueó la solicitud")
        return []
    except Exception as e:
        print(f"Error obteniendo el feed de noticias: {str(e)}")
        return []
        
    return noticias