from lxml import html
from curl_cffi import requests
from log import Log
from webdriver import get_driver
import config
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import base64

class Crawler:

    def __init__(self):
        self.logger = Log().get_logger(f'{config.NAME_CRAWLER}.log')

    def get_keywords(self):

        df = pd.read_csv('input/keywords.csv')

        keywords = {}

        for _, fila in df.iterrows():

            provincia = fila['provincia']
            keyword = fila['keyword']

            if provincia not in keywords:
                keywords[provincia] = []

            if keyword not in keywords[provincia]:
                keywords[provincia].append(keyword)

        return keywords

    def login(self, driver):
     
        button_entrega = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                    By.XPATH,
                    "//a[normalize-space()='Seleccioná el método de entrega']"
                ))
        )
        button_entrega.click()

        button_email_password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[.//span[normalize-space()='Email y contraseña']]"
                ))
        )

        button_email_password.click()

        driver.find_element(By.XPATH,"//input[@placeholder='Email']").send_keys(config.EMAIL_ACCOUNT)
        driver.find_element(By.XPATH,"//input[@placeholder='Contraseña']").send_keys(config.PASSWORD_ACCOUNT)

        button_ingresar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@type='submit' and .//span[normalize-space()='Entrar']]"
                ))
            )
        button_ingresar.click()
        time.sleep(2)

        self.logger.info('Sesion Iniciada')

    def cargar_provincia(self, driver, provincia):

        boton_retiro = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[.//p[normalize-space()='Retirar en una tienda']]"
            ))
        )

        boton_retiro.click()

        time.sleep(3)

        select_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//select[option[contains(normalize-space(), 'Seleccionar Provincia')]]"
            ))
        )

        provincia = provincia.upper().strip()

        print(f"Seleccionando provincia: {provincia}")

        driver.execute_script("""
            const select = arguments[0];
            const value = arguments[1];

            select.value = value;
            select.dispatchEvent(new Event('change', { bubbles: true }));
        """, select_element, provincia)

        print("Value:", select_element.get_attribute("value"))
        time.sleep(3)

        select_tienda = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//select[option[contains(normalize-space(), 'Seleccionar tienda')]]"
            ))
        )

        driver.execute_script("""
            const select = arguments[0];

            // La primera opción disponible después de la opción deshabilitada
            const option = Array.from(select.options)
                .find(option => !option.disabled && option.value !== '');

            if (option) {
                select.value = option.value;

                select.dispatchEvent(
                    new Event('input', { bubbles: true })
                );

                select.dispatchEvent(
                    new Event('change', { bubbles: true })
                );
            }
        """, select_tienda)

        time.sleep(3)

        boton_confirmar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[.//div[normalize-space()='Confirmar']]"
            ))
        )

        boton_confirmar.click()

    def generar_params(self,keyword, desde=0, cantidad=20):
        hasta = desde + cantidad - 1

        variables = {
            "skusFilter": "ALL",
            "simulationBehavior": "default",
            "installmentCriteria": "MAX_WITHOUT_INTEREST",
            "productOriginVtex": False,
            "map": "ft",
            "query": keyword,
            "orderBy": "OrderByScoreDESC",
            "from": desde,
            "to": hasta,
            "selectedFacets": [
                {
                    "key": "ft",
                    "value": keyword
                }
            ],
            "fullText": keyword,
            "operator": "and",
            "fuzzy": "0",
            "searchState": None,
            "hideUnavailableItems": True,
            "facetsBehavior": "Static",
            "categoryTreeBehavior": "default",
            "withFacets": False
        }

        variables_base64 = base64.b64encode(
            json.dumps(
                variables,
                separators=(",", ":"),
                ensure_ascii=False
            ).encode("utf-8")
        ).decode("utf-8")

        extensions = {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "b398fc0a2fd04ea5d4f7a94c732c10fb1bf64f8f9a2b31c92aee6a5e796457c9",
                "sender": "vtex.store-resources@0.x",
                "provider": "vtex.search-graphql@0.x"
            },
            "variables": variables_base64
        }

        return {
            "workspace": "master",
            "maxAge": "short",
            "appsEtag": "remove",
            "domain": "store",
            "locale": "es-AR",
            "__bindingId": "6890cd39-87c6-4689-ad4f-3b913f3c0b19",
            "operationName": "productSearchV3",
            "variables": "{}",
            "extensions": json.dumps(
                extensions,
                separators=(",", ":")
            )
        }

    def run(self):
        self.logger.info('Start Crawler')

        driver = get_driver(config.CHROMEDRIVER_PATH)
        keywords = self.get_keywords()

        try:
            driver.get(config.URL_BASE)
            self.login(driver)
            time.sleep(5)

            for provincia, lista_keywords in keywords.items():

                self.logger.info(
                    f'Cargamos provincia: {provincia}'
                )

                self.cargar_provincia(driver, provincia)

                cookies = driver.get_cookies()
                cookies = {
                    cookie["name"]: cookie["value"]
                    for cookie in driver.get_cookies()
                }

                for keyword in lista_keywords:

                    self.logger.info(
                        f'Procesando keyword: {keyword}'
                    )

                    desde = 0
                    cantidad = 20
                    todos_productos = []

                    while True:

                        self.logger.info(
                            f'Buscando productos {desde} - {desde + cantidad - 1}'
                        )

                        params = self.generar_params(
                            keyword,
                            desde,
                            cantidad
                        )

                        while True:
                            response = requests.get(
                                config.URL_API,
                                params=params,
                                cookies=cookies,
                                headers=config.HEADERS
                            )

                            if response.status_code == 200:
                                break

                            self.logger.warning(
                                f'Error HTTP {response.status_code}. Reintentando...'
                            )

                            time.sleep(1)

                        data = response.json()

                        # Acá tenemos que sacar los productos
                        productos = data["data"]["productSearch"]["products"]

                        cantidad_productos = len(productos)

                        self.logger.info(
                            f'Productos encontrados: {cantidad_productos}'
                        )

                        if not productos:
                            break

                        todos_productos.extend(productos)

                        # Si devuelve menos de 20,
                        # significa que llegamos al final
                        if cantidad_productos < cantidad:
                            break

                        desde += cantidad

                    self.logger.info(
                        f'Total productos para "{keyword}": '
                        f'{len(todos_productos)}'
                    )

                    print(todos_productos)

            input("Press Enter to close the browser...")


        finally:
            driver.quit()

        self.logger.info('End Crawler')
    

if __name__ == "__main__":

    crawler = Crawler()
    crawler.run()
    
    