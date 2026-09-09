

from lxml import html
from curl_cffi import requests

import config
from log import Log
from webdriver import get_driver



class Crawler:

    def __init__(self):
        self.logger=Log().get_logger(f'{config.NAME_CRAWLER}.log')


    def run(self):

        self.logger.info('Start Crawler')

        driver = get_driver(config.CHROMEDRIVER_PATH)

        try:
            driver.get("https://vea.com.ar")

            self.logger.info('Openning vea')


            self.logger.error('Soy un error')


            
            input("Press Enter to close the browser...")


        finally:
            driver.quit()

        self.logger.info('End Crawler')
        


if __name__ == "__main__":
    Crawler().run()



