#Imports:

import logging

#Modulo instrumental:

def configurar_logging() -> None:

    """
    Configura el logging de la aplicación. Se llama una sola vez, desde main.py.
    """

    #Definicion de parlantes:

    handler_app = logging.FileHandler("app.log", encoding="utf-8")

    #Configuración del parlante:

    handler_app.setLevel(logging.INFO)
    formato = logging.Formatter("%(asctime)s: [%(levelname)s] --- %(name)s ---> [%(message)s]")
    handler_app.setFormatter(formato)

    #Configuracion de la consola:

    raiz = logging.getLogger()
    raiz.setLevel(logging.INFO)
    raiz.addHandler(handler_app)