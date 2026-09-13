import config
from logger import Log
import time
from web_driver import get_driver

from curl_cffi import requests
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

class Discovery:
    def __init__(self):
        self._logger = Log.get_logger(config.LOG_PATH)
        self._records = set()
    
    def _signin_and_select_region(self, province):
        try:
            self._logger.info(f"Starting signin process for {province}")

            driver = get_driver(config.DRIVER_PATH)
            driver.get(config.BASE_URL)

            wait = WebDriverWait(driver, 10)

            # After landing on the site, first button to press
            my_account_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'vtex-login')]//button[contains(@class, 'vtex-button')]")
                ),
                message = "my_account_button was not found"
            )
            my_account_button.click()
            self._logger.info("my_account_button found and clicked")

            # After previous button, a popup window spawns where we need to select an auth option
            auth_options_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'emailPasswordOptionBtn')]//button[contains(@class, 'vtex-button')]")
                ),
                message = "auth_options_button was not found"
            )
            auth_options_button.click()
            self._logger.info("auth_options_button found and clicked")

            # After that we shoulds have the signin form available

            # Email input
            email_input = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inputContainerEmail')]//input")
                ),
                message = "email_input was not found or is not visible"
            )
            email_input.clear()
            email_input.send_keys(config.ACCOUNT_EMAIL)
            self._logger.info("email_input found and filled")

            # Password input
            password_input = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inputContainerPassword')]//input")
                ),
                message = "password_input was not found or is not visible"
            )
            password_input.clear()
            password_input.send_keys(config.ACCOUNT_PASSWORD)
            self._logger.info("password_input found and filled")

            # Signin form submit button
            submit_button = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'sendButton')]//button[contains(@class, 'vtex-button')]")
                ),
                message = "submit_button was not found"
            )
            submit_button.click()
            self._logger.info("submit_button found and clicked")
            
            # After signin, we need to select the delivery method
            method_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'veaargentina-delivery-modal-1-x-containerTrigger')]/parent::div"),
                ),
                message = "method_button was not found"
            )
            method_button.click()
            self._logger.info("method_button found and clicked")

            # From the popup window we select the pickup delivery option
            pickup_option = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'veaargentina-delivery-modal-1-x-pickUpSelectionContainer')]//button[contains(@class, 'vtex-button')]")
                ),
                message = "pickup_option was not found"
            )
            pickup_option.click()
            self._logger("pickup_option was clicked")

            # From the popup window we select the region we want to scrape from
            region_option = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//div[contains(@class, 'veaargentina-delivery-modal-1-x-StoresDropDownContainer')]//select)[1]")
                ),
                message = "region_option was not found"
            )
            region_dropdown = Select(region_option)
            region_dropdown.select_by_visible_text(province)
            self._logger.info(f"region_option found and {province} selected")

            # From the popup window we select the first possible store option
            store_option = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//div[contains(@class, 'veaargentina-delivery-modal-1-x-StoresDropDownContainer')]//select)[2]")
                ),
                message = "store_option was not found"
            )
            store_dropdown = Select(store_option)
            store_dropdown.select_by_index(1)
            self._logger.info("store_option found and first option selected")


            # From the popup window we submit the form
            confirm_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'veaargentina-delivery-modal-1-x-buttonsContainer')]//button[contains(@class, 'vtex-button')]")
                ),
                message = "confirm_button was not found"
            )
            confirm_button.click()
            self._logger.info("confirm_button found and clicked")
            
            # We wait for 5 seconds for the cookies to be set

            cookies = {
                c["name"]: c["value"] 
                for c in driver.get_cookies()
            }
            self._logger.info("Cookies set successfully")

            self._logger.info("Signin and region selection process completed successfully")

            return cookies

        except Exception as e:
            self._logger.error(f"There was an error signing in. Error: {e}")
        finally:
            driver.quit()
    
    def _get_producs(self):
        pass
    
    def run(self):
        try:
            provinces = config.PROVINCES
            for index, p in enumerate(provinces):
                province_cookies = self._signin_and_select_region(p.strip().casefold())
                print(province_cookies)

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