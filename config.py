from dotenv import load_dotenv
import os

load_dotenv('.env')

NAME_CRAWLER = 'vea'


#CHROMEDRIVER_PATH = "C:/Users/Alumno/Desktop/proyectos/chromedriver-v-/chromedriver.exe"

#CHROMEDRIVER_PATH = "C:/Users/tata_/OneDrive/Documentos/Programacion/WebScrapping/chromedriver/152.0.7977.83/chromedriver.exe"

CHROMEDRIVER_PATH = "C:/Users/tata_/OneDrive/Documentos/WebScrapping/chromedriver/152.0.7977.82/chromedriver.exe"

HEADERS = {
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': 'https://www.vea.com.ar/jabon?_q=jabon&map=ft',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36'}


URL_BASE = "https://www.vea.com.ar/"
URL_API = 'https://www.vea.com.ar/_v/segment/graphql/v1'

EMAIL_ACCOUNT = os.environ.get('EMAIL')
PASSWORD_ACCOUNT = os.environ.get('PASSWORD')