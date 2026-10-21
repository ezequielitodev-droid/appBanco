#Flujo principal de ejecucion con el CLI:

#Imports:

import time
import logging
from decimal import Decimal

from datos.persistencia import cargar_datos, guardar_datos
from utils.vistas import (
    limpiar_pantalla, 
    mostrar_bienvenida, 
    mostrar_menu_principal, 
    mostrar_menu_gestionar_cliente, 
    mostrar_menu_operaciones_cliente, 
    mostrar_menu_crear_cuenta
)
from core.core_cli import (
    flujo_dar_alta_cliente, 
    flujo_resumen_de_banco, 
    flujo_salida_guardado_programa, 
    flujo_gestion_clientes_cli
)

#Global Variables:

logger = logging.getLogger(__name__)

#Funcion principal:

def flujo_cli_app() -> None:

    #Creacion o carga del banco...
    banco = cargar_datos()
    logger.info(f"Sistema CLI iniciado correctamente. Banco cargado: {banco.get_nombre()}")

    mostrar_bienvenida(banco)

    flag_program = True

    while flag_program:

        option = mostrar_menu_principal(banco)

        match option:

            case "1":

                flujo_dar_alta_cliente(banco) 

            case "2":

                flujo_gestion_clientes_cli(banco)

            case "3":

                flujo_resumen_de_banco(banco)

            case "4":

                flujo_salida_guardado_programa(banco)
                flag_program = False

            case _:

                print("\n Opción inválida. Por favor, elija una opción del 1 al 4.")
                time.sleep(1.5)