from lxml import html
from curl_cffi import requests
from log import Log
from webdriver import get_driver
import config

class Crawler:

    def __init__(self):
        self.logger = Log().get_logger(f'{config.NAME_CRAWLER}.log')

    def run(self):
        self.logger.info('Start Crawler')
        driver = get_driver(config.CHROMEDRIVER_PATH)
        
        try:
            driver.get(config.URL_BASE)

            input("Press Enter to close the browser...")

        finally:
            driver.quit()

        self.logger.info('End Crawler')
    

if __name__ == "__main__":

    crawler = Crawler()
    crawler.run()
    
    