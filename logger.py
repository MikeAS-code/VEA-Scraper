"""
Configuración de Logging — NIVEL BÁSICO
Complejidad: Baja (2/10)

¿Para qué sirve?
----------------
Esta configuración está pensada para proyectos pequeños o crawlers simples
donde solo necesitamos:

- Mostrar los logs en la consola.
- Guardar los logs de la ejecución en un archivo local.
- Trabajar con nivel INFO o superior.

Características principales
---------------------------
- Usa logging.FileHandler para escribir en un archivo.
- Usa logging.StreamHandler para mostrar los mismos mensajes en consola.
- El archivo se abre con mode="w", por lo que se sobrescribe en cada ejecución.
- No mantiene historial entre ejecuciones.
- No tiene rotación de archivos.
- No necesita servicios externos.

¿Cuándo usarla?
---------------
- Scrapers pequeños.
- Scripts que se ejecutan manualmente.
- Proyectos de aprendizaje.
- Procesos donde solo interesa conservar el log de la ejecución actual.

Ejemplo de arquitectura:

    Crawler
       ├── Consola
       └── Archivo .log
"""

import os
import logging


class Log:
    @staticmethod
    def get_logger(log_path):
        try:
            log_path_str = str(log_path)
            split_path = log_path_str.split("/")

            if len(split_path) > 1:
                logger = logging.getLogger(split_path[1])
            else:
                logger = logging.getLogger(split_path[0])

            if not logger.hasHandlers():
                formatter = logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(message)s"
                )

                # mode="w" sobrescribe el archivo en cada nueva ejecución.
                file_handler = logging.FileHandler(
                    os.path.join(log_path),
                    mode="a" # "a" para append
                )
                file_handler.setFormatter(formatter)

                # Muestra los mismos mensajes también en la consola.
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(formatter)

                # INFO registra INFO, WARNING, ERROR y CRITICAL.
                logger.setLevel(logging.INFO)

                logger.addHandler(file_handler)
                logger.addHandler(stream_handler)

            return logger

        except Exception as e:
            print(e)
            raise