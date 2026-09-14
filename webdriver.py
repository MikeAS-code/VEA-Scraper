# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_driver(driver_path: str):
    """
    Crea una instancia local de Chrome utilizando una ruta explícita
    al ejecutable de ChromeDriver.
    """

    # Configuración del navegador Chrome
    options = Options()

    options.set_capability(
        "goog:loggingPrefs",
        {"performance": "ALL"}
    )

    # Abre Chrome maximizado
    options.add_argument("--start-maximized")

    # Evita algunos mensajes de automatización en Chrome
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Desactiva extensiones instaladas
    options.add_argument("--disable-extensions")

    # Desactiva notificaciones del navegador
    options.add_argument("--disable-notifications")

    # Evita problemas de permisos en algunos entornos
    options.add_argument("--no-sandbox")

    # Mejora compatibilidad en entornos con pocos recursos
    options.add_argument("--disable-dev-shm-usage")

    # Desactiva la GPU. Útil en servidores o máquinas virtuales
    options.add_argument("--disable-gpu")

    # Ejecuta Chrome sin interfaz gráfica
    # Útil para servidores, pero para aprender conviene dejarlo comentado
    # options.add_argument("--headless=new")

    # Define el tamaño de ventana si no usas start-maximized
    # options.add_argument("--window-size=1366,768")

    # Cambia el User-Agent del navegador
    # Útil cuando una web responde distinto según navegador/dispositivo
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #     "AppleWebKit/537.36 (KHTML, like Gecko) "
    #     "Chrome/120.0.0.0 Safari/537.36"
    # )

    # Oculta parcialmente que Chrome fue abierto por Selenium
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Desactiva la extensión interna de automatización de Chrome
    options.add_experimental_option("useAutomationExtension", False)

    # Preferencias del perfil de Chrome
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    })

    service = Service(executable_path=driver_path)

    return webdriver.Chrome(
        service=service,
        options=options
    )

