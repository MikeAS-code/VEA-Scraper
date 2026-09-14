from dotenv import load_dotenv
import os

load_dotenv('.env')

NAME_CRAWLER = 'vea'


## CHROMEDRIVER_PATH = "C:/Users/Alumno/Desktop/proyectos/chromedriver-v-/chromedriver.exe"

CHROMEDRIVER_PATH = "C:/Users/tata_/OneDrive/Documentos/Programacion/WebScrapping/chromedriver/152.0.7977.83/chromedriver.exe"


URL_BASE = "https://www.vea.com.ar/"

EMAIL_ACCOUNT = os.environ.get('EMAIL')
PASSWORD_ACCOUNT = os.environ.get('PASSWORD')