import config
from logger import Log
import time
from web_driver import get_driver

from curl_cffi import requests
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Discovery:
    def __init__(self):
        self._logger = Log.get_logger(config.LOG_PATH)
        self._driver = get_driver(config.DRIVER_PATH)
        self._wait = WebDriverWait(self._driver, 10)
    
    def _signin(self):
        try:
            self._logger.info("Starting signin process")

            self._driver.get(config.BASE_URL)

            # After landing on the site, first button to press
            land_button = self._wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'vtex-login')]//button[contains(@class, 'vtex-button')]")
                ),
                message="land_button not found or not clickable"
            )
            land_button.click()
            self._logger.info("land_button clicked")

            # After previous button, a popup window spawns where we need to select an option
            options_button = self._wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'emailPasswordOptionBtn')]//button[contains(@class, 'vtex-button')]")
                ),
                message="options_button not found or not clickable"
            )
            options_button.click()
            self._logger.info("options_button clicked")

            # After that we shoulds have the signin form available

            # Email input
            email_input = self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inputContainerEmail')]//input")
                ),
                message="email_input not found or not visible"
            )
            email_input.clear()
            email_input.send_keys(config.ACCOUNT_EMAIL)
            self._logger.info("email_input filled")

            # Password input
            password_input = self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inputContainerPassword')]//input")
                ),
                message="password_input not found or not visible"
            )
            password_input.clear()
            password_input.send_keys(config.ACCOUNT_PASSWORD)
            self._logger.info("password_input filled")

            # Submit button
            submit_button = self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'sendButton')]//button[contains(@class, 'vtex-button')]")
                ),
                message="submit_button not found or not clickable"
            )
            submit_button.click()
            self._logger.info("submit_button clicked")

            # Wait until form unmounts
            self._wait.until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inputContainerEmail')]")
                ),
                message="form not unmounting"
            )

            # Wait for the cookies
            self._wait.until(
                lambda d: d.get_cookie("VtexIdclientAutCookie_veaargentina"),
                message = "Cookie was not set"
            )

            cookies = {
                c["name"]: c["value"] 
                for c in self._driver.get_cookies()
                if c["name"].startswith("VtexIdclientAutCookie_")
            }

            self._logger.info("Signin process completed successfully")

            return cookies

        except Exception as e:
            self._logger.error(f"There was an error signing in. Error: {e}")
        finally:
            self._driver.quit()
    
    def _load_cookies(self, cookies):
        try:
            self._logger.info("Starting cookies loading process")

            for name, value in cookies.items():
                self._driver.add_cookie({"name": name, "value": value})
            
            self._driver.refresh()

            self._logger.info("Cookies loaded successfully")

        except Exception as e:
            self._logger.error(f"There was an error loading the cookies. Error: {e}")

    def _select_region(self, cookies):
        try:
            self._logger.info("Starting region selection process")

            self._driver.get(config.BASE_URL)

            self._load_cookies(cookies)
        except Exception as e:
            print(f"There was an error selecting the region. Error: {e}")
        finally:
            self._driver.quit()

    def run(self):
        try:
           cookies = self._signin()
           print(cookies)

        except Exception as e:
            print(f"There was an error in the discovery process. Error: {e}")
        

class PDP:
    def __init__(self):
        pass

    def run(self):
        pass
    
if __name__ == "__main__":
    print("Webcrawler started")

    Discovery().run()