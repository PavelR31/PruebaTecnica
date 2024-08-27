import sys
import requests
from bs4 import BeautifulSoup
from google.cloud import language_v1
import json
import os

# Configura las credenciales de Google Cloud
def configurar_credenciales():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credenciales_path = os.path.join(script_dir, 'credenciales.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credenciales_path

# Obtiene el contenido textual de una URL
def obtener_contenido_url(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        # Extrae el texto de la respuesta usando BeautifulSoup
        soup = BeautifulSoup(respuesta.content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except requests.RequestException as e:
        raise RuntimeError(f"Error al obtener contenido de la URL: {e}")

# Analiza entidades en el contenido textual
def analizar_entidades(contenido_texto, cliente):
    try:
        documento = language_v1.Document(content=contenido_texto, type=language_v1.Document.Type.PLAIN_TEXT)
        respuesta = cliente.analyze_entities(document=documento)
        entidades = respuesta.entities
        entidades_ordenadas = sorted(entidades, key=lambda e: e.salience, reverse=True)
        
        return [
            {
                'nombre': entidad.name,
                'tipo': language_v1.Entity.Type(entidad.type_).name,
                'relevancia': entidad.salience
            }
            for entidad in entidades_ordenadas[:5]
        ]
    except Exception as e:
        raise RuntimeError(f"Error al analizar entidades: {e}")

def main():
    configurar_credenciales()
    
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Se debe proporcionar una URL como argumento."}, ensure_ascii=False))
        return
    
    url = sys.argv[1]
    
    try:
        contenido = obtener_contenido_url(url)
        cliente = language_v1.LanguageServiceClient()
        resultados = analizar_entidades(contenido, cliente)
        print(json.dumps(resultados, indent=4, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
