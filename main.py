from lxml import html
from curl_cffi import requests
from log import Log
from webdriver import get_driver
import config
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

    def cargamos_provincia(self, driver, provincia):

        boton_retiro = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[.//p[normalize-space()='Retirar en una tienda']]"
            ))
        )

        boton_retiro.click()

        time.sleep(3)

        select_provincia = Select(
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//select[option[@value='' and normalize-space()='Seleccionar Provincia']]"
                ))
            )
        )

        select_provincia.select_by_visible_text(provincia)

        time.sleep(3)

        select_tienda = WebDriverWait(driver, 20).until(
            lambda driver: (
                Select(driver.find_element(
                    By.XPATH,
                    "//select[option[@value='' and normalize-space()='Seleccionar tienda']]"
                ))
                if len(Select(driver.find_element(
                    By.XPATH,
                    "//select[option[@value='' and normalize-space()='Seleccionar tienda']]"
                )).options) > 1
                else False
            )
        )

        select_tienda.select_by_index(1)

        time.sleep(3)

        boton_confirmar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[.//div[normalize-space()='Confirmar']]"
            ))
        )

        boton_confirmar.click()

    def run(self):
        self.logger.info('Start Crawler')
        driver = get_driver(config.CHROMEDRIVER_PATH)
        keywords = self.get_keywords()

        try:
            driver.get(config.URL_BASE)
            self.login(driver)
            time.sleep(10)

            for provincia, lista_keywords in keywords.items():

                self.logger.info(
                    f'Cargamos provincia: {provincia}'
                )

                self.cargamos_provincia(driver, provincia)

                for keyword in lista_keywords:

                    self.logger.info(
                        f'Procesando keyword: {keyword}'
                    )

                    # Acá hacés el scraping de esa keyword
                    # self.scrapear(driver, keyword)

            input("Press Enter to close the browser...")

        finally:
            driver.quit()

        self.logger.info('End Crawler')
    

if __name__ == "__main__":

    crawler = Crawler()
    crawler.run()
    
    