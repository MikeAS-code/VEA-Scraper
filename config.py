import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.vea.com.ar"

PROXIES = {
    "http": os.getenv("PROXY"),
    "https": os.getenv("PROXY") 
}

LOG_PATH = "./out/crawler.log"

# You could use the tempmail to get the email and password
ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

DRIVER_PATH = "./drivers/chromedriver"

# PROVINCES = ["Chubut", "Buenos Aires", "Santiago del Estero", "Cordoba", "Rio Negro", "Buenos Aires", "San Luis", "La Rioja", "Misiones", "Cordoba", "Tierra del Fuego"]
PROVINCES = ["Buenos Aires"]
KEYWORDS = ["Shampoo", "Cerveza", "Crema", "Carne", "Verdura", "Vino", "Electrodomesticos", "Tecnologia", "Carne", "Pollo"]