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