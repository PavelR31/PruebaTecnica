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

def obtener_contenido_completo_url(url):
    try:
        # Configura las opciones del navegador
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")

        # Inicia el driver de Chrome
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        # Abre la URL
        driver.get(url)

      
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[self::p or self::div or self::article or self::span or self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]"))
        )
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        sleep(2)

        elementos_texto = driver.find_elements(By.XPATH, "//*[self::p or self::div or self::article or self::span or self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]")
        
        # Extrae el texto de los elementos encontrados
        contenido_texto = " ".join([element.text for element in elementos_texto])

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
