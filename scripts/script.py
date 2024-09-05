import sys
import json
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from google.cloud import language_v1

def configurar_credenciales():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credenciales_path = os.path.join(script_dir, 'credenciales.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credenciales_path

from selenium.common.exceptions import StaleElementReferenceException

def obtener_contenido_completo_url(url):
    try:
        
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")

      #incia chrome
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        # Abre la URL
        driver.get(url)

        # Carga de contenido dinamico
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[self::p or self::div or self::article or self::span or self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]"))
        )

        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)  

      
        def obtener_texto():
            try:
                # Encuentra todos los elementos de texto relevantes en la página
                elementos_texto = driver.find_elements(By.XPATH, "//*[self::p or self::div or self::article or self::span or self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]")
                return " ".join([element.text for element in elementos_texto])
            except StaleElementReferenceException:
                # Si se produce una excepción, intenta de nuevo
                return obtener_texto()

        contenido_texto = obtener_texto()

        driver.quit()

        return contenido_texto
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        raise RuntimeError(f"Error al obtener contenido de la URL con Selenium: {e}")


def analizar_entidades(contenido_texto, cliente):
    try:
        documento = language_v1.Document(content=contenido_texto, type_=language_v1.Document.Type.PLAIN_TEXT)
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
        contenido_texto = obtener_contenido_completo_url(url)
        cliente = language_v1.LanguageServiceClient()
        resultados = analizar_entidades(contenido_texto, cliente)
        print(json.dumps(resultados, indent=4, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
