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
            self._driver.get(config.BASE_URL)

            # After landing on the site, first button to press
            land_button = self._wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'vtex-login')]//button[contains(@class, 'vtex-button')]")
                ),
                message="land_button not found or not clickable"
            )
            land_button.click()

            # After previous button, a popup window spawns where we need to select an option
            options_button = self._wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'emailPasswordOptionBtn')]//button[contains(@class, 'vtex-button')]")
                ),
                message="options_button not found or not clickable"
            )
            options_button.click()

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

            # Password input
            password_input = self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inputContainerPassword')]//input")
                ),
                message="password_input not found or not visible"
            )
            password_input.clear()
            password_input.send_keys(config.ACCOUNT_PASSWORD)

            # Submit button
            submit_button = self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'sendButton')]//button[contains(@class, 'vtex-button')]")
                ),
                message="submit_button not found or not clickable"
            )
            submit_button.click()

            # Check of an user only component to be rendered to confirm authentication
            check_button = self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'vtex-login')]//button[contains(@class, 'vtex-button')]")
                ),
                message="check_button not found or not clickable"
            )
            check_button.click()

            self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'accountOptions')]")
                ),
                message="account_options not found or not visible"
            )

            cookies = {
                c["name"]: c["value"] for c in self._driver.get_cookies()
            }

            self._driver.quit()

            return cookies

        except Exception as e:
            self._logger.error(f"There was an error signing in. Error: {e}")
        finally:
            time.sleep(5)
            self._driver.quit()

    def _get_session_cookie(self, driver):
        try:
            options_button = self._wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'veaargentina-delivery-modal-1-x-containerTrigger')]/..")
                )
            )
            print(driver.title)
            input("Press Enter to close the browser...")
        except Exception as e:
            print(f"There was an error getting the session cookie. Error {e}")
        finally:
            driver.quit()

    def run(self):
        try:
           signin_cookies = self._signin()
           print(signin_cookies)

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