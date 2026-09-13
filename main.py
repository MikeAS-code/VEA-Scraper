import config
from logger import Log
import time
from web_driver import get_driver
import unicodedata
import re
from typing import Any

from curl_cffi import requests
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Discovery:
    def __init__(self):
        self._logger = Log.get_logger(config.LOG_PATH)
        self._records = set()

    def _normalize_province(self, text: str) -> str:
        decomposed = unicodedata.normalize("NFKD", text.strip().casefold())
        return "".join(c for c in decomposed if not unicodedata.combining(c))


    def _validate_province(self, province: Any) -> str:
        _PROVINCE_RE = re.compile(r"^[a-z]+(?:[ '-][a-z]+)*$")

        if not isinstance(province, str):
            raise ValueError(f"Province must be a string, got {type(province).__name__}")
        
        province = province.strip()

        if not province:
            raise ValueError("Province is empty")

        if len(province) > 80:
            raise ValueError(f"Province is too long: {province!r}")
        
        normalized = self._normalize_province(province)
    
        if not _PROVINCE_RE.fullmatch(normalized):
            raise ValueError(f"Province has invalid characters: {province!r}")

        return normalized
    
    def _click(self, wait, xpath, name):
        try:
            element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpath)
                ),
                message = f"{name} was not found"
            )
            element.click()
            self._logger.info(f"{name} found and clicked")
        
        except TimeoutException:
            self._logger.error(f"Timeout while clicking '{name}'. XPATH = '{xpath}'")
            raise
        
        except Exception as e:
            self._logger.error(f"Failed clicking '{name}': {e}. XPATH= '{xpath}'")
            raise

    def _fill(self, wait, xpath, value, name):
        try:
            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpath)
                ),
                message = f"{name} was not found or is not visible"
            )
            element.clear()
            element.send_keys(value)
            self._logger.info(f"{name} found and filled")
        
        except TimeoutException:
            self._logger.error(f"Timeout while filling '{name}'. XPATH = '{xpath}'")
            raise
        
        except Exception as e:
            self._logger.error(f"Failed filling '{name}': {e}. XPATH = '{xpath}'")
            raise

    
    def _get_dropdown(self, wait, xpath, name):
        try:
            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath)),
                message=f"{name} was not found",
            )
            self._logger.info(f"{name} found")
            return Select(element)

        except TimeoutException:
            self._logger.error(f"Timeout while finding dropdown '{name}'. XPATH = '{xpath}'")
            raise

        except Exception as e:
            self._logger.error(f"Failed finding dropdown '{name}': {e}. XPATH = '{xpath}'")
            raise
    
    def _select_dropdown_option(self, dropdown, wanted, name):
        match = None

        for option in dropdown.options:
            option_text = option.text.strip()
            if option_text == "":
                continue
            if self._normalize_province(option_text) == wanted:
                match = option.text
                break

        if match is None:
            available = []
            for option in dropdown.options:
                option_text = option.text.strip()
                if option_text != "":
                    available.append(option_text)

            self._logger.error(
                f"Option '{wanted}' not found in '{name}'. Available: {available}"
            )

            raise ValueError(
                f"Option '{wanted}' not found in '{name}'. Available: {available}"
            )

        dropdown.select_by_visible_text(match)

        self._logger.info(f"{name} selected '{match}'")
                
    
    def _signin(self, wait):
        # Button labeled "Mi cuenta" is the first thing to click
        self._click(
            wait,
            "//div[contains(@class, 'vtex-login')]//button[contains(@class, 'vtex-button')]",
            "my_account_button",
        )

        # A popup window should appear, we must press the "Email y Contraseña" button
        self._click(
            wait,
            "//div[contains(@class, 'emailPasswordOptionBtn')]//button[contains(@class, 'vtex-button')]",
            "auth_options_button",
        )

        # We fill the Email field from the form
        self._fill(
            wait,
            "//div[contains(@class, 'inputContainerEmail')]//input",
            config.ACCOUNT_EMAIL,
            "email_input",
        )

        # We fill the Password field from the form
        self._fill(
            wait,
            "//div[contains(@class, 'inputContainerPassword')]//input",
            config.ACCOUNT_PASSWORD,
            "password_input",
        )

        # We press the Submit button from the form
        self._click(
            wait,
            "//div[contains(@class, 'sendButton')]//button[contains(@class, 'vtex-button')]",
            "submit_button",
        )

    def _select_first_store(self, wait, dropdown, name):
        def stores_are_ready(driver):
            count = 0
            for option in dropdown.options:
                if option.text.strip() != "":
                    count = count + 1
            return count > 1

        try:
            wait.until(
                stores_are_ready,
                message=f"{name} did not load any stores",
            )

            dropdown.select_by_index(1)

            selected = dropdown.first_selected_option.text

            self._logger.info(f"{name} selected '{selected}'")

        except TimeoutException:
            self._logger.error(f"Timeout waiting for stores in '{name}'")
            raise

        except Exception as e:
            self._logger.error(f"Failed selecting first store in '{name}': {e}")
            raise
    
    def _select_pickup_region(self, wait, province, province_key):
        # Element labeled "Selecciona el metodo de entrega" is the first thing to click
        self._click(
            wait,
            "//div[contains(@class, 'veaargentina-delivery-modal-1-x-containerTrigger')]/parent::div",
            "method_button",
        )

        # A popup window should appear, we must press the "Retirar en una tienda" button
        self._click(
            wait,
            "//div[contains(@class, 'veaargentina-delivery-modal-1-x-pickUpSelectionContainer')]//button[contains(@class, 'vtex-button')]",
            "pickup_option",
        )

        # We need to grab reference from the Provincias select element
        region_dropdown = self._get_dropdown(
            wait,
            "(//div[contains(@class, 'veaargentina-delivery-modal-1-x-StoresDropDownContainer')]//select)[1]",
            "region_option",
        )
        
        # We select the province we need
        self._select_dropdown_option(region_dropdown, province_key, "region_option")
        
        # We need to grab reference from the Tienda select element
        store_dropdown = self._get_dropdown(
            wait,
            "(//div[contains(@class, 'veaargentina-delivery-modal-1-x-StoresDropDownContainer')]//select)[2]",
            "store_option",
        )

        # We select the first available option
        self._select_first_store(wait, store_dropdown, "store_options")

        # We submit our form
        self._click(
            wait,
            "//div[contains(@class, 'veaargentina-delivery-modal-1-x-buttonsContainer')]//button[contains(@class, 'vtex-button')]",
            "confirm_button",
        )

    def _signin_and_select_region(self, province):
        driver = None
        province_key = self._validate_province(province)

        try:
            self._logger.info(f"Starting signin process for {province_key}")

            driver = get_driver(config.DRIVER_PATH)
            driver.get(config.BASE_URL)

            wait = WebDriverWait(driver, 10)

            self._signin(wait)
            self._select_pickup_region(wait, province, province_key)

            cookies = {}
            for c in driver.get_cookies():
                cookies[c["name"]] = c["value"]
            
            self._logger.info("Cookies set successfully")
            self._logger.info("Signin and region selection process completed")

            return cookies

        except Exception:
            self._logger.error(f"Signin and region selection aborted for: {province_key}")

        finally:
            if driver is not None:
                driver.quit()
    
    def _get_producs(self):
        pass
    
    def run(self):
        try:
            provinces = config.PROVINCES
            for index, p in enumerate(provinces):
                province_cookies = self._signin_and_select_region(p)
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