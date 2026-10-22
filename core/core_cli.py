#Archivo donde estaran las logicas principales del flujo del CLI...

#Imports:

import decimal
import logging
import random
import string
import time
from decimal import Decimal

from datos.persistencia import cargar_datos, guardar_datos
from models.objects_models import (
    Banco, 
    Cliente, 
    CuentaAhorro, 
    CuentaCorriente
)
from utils.vistas import (
    limpiar_pantalla, 
    mostrar_menu_crear_cuenta, 
    mostrar_menu_gestionar_cliente, 
    mostrar_menu_operaciones_cliente, 
)


#Constants:

#Global Variables:

logger = logging.getLogger(__name__)

#Moduls:

def flujo_dar_alta_cliente(banco: Banco) -> None:

    """
        Gestiona el flujo interactivo por consola para dar de alta a un nuevo cliente en el banco.

        Solicita al usuario el nombre y el DNI, procesa el registro a través de la instancia
        del banco y captura posibles errores de validación o duplicidad de DNI.

        Args:
            banco (Banco): Instancia del objeto Banco donde se registrará el cliente.

        Returns:
            None

        Raises:
            ValueError: Capturado internamente si el DNI ya está registrado o los datos son inválidos.

        Examples:
            >>> # flujo_dar_alta_cliente(banco_instancia)
    """

    limpiar_pantalla()

    print("--- ALTA DE NUEVO CLIENTE ---\n")

    #Datos necesarios para el alta del cliente...
    nombre_cliente = input("Ingrese el nombre del cliente: ").strip()
    dni_cliente_normalizado = input("Ingrese el DNI del cliente: ").strip().replace(".", "")

    try:

        banco.alta_cliente(nombre_cliente, dni_cliente_normalizado)
        print("\n!Cliente dado de alta con exito!")
        logger.info(f"Alta de cliente procesada desde CLI con éxito: DNI {dni_cliente_normalizado}")
    
    except ValueError as e:

        print(f"\n Error al dar de alta: {e}")
        logger.error(f"Fallo en alta de cliente desde CLI [ValueError]: {e}")

    except Exception as e:

        print(f"\n Ocurrió un error inesperado: {e}")
        logger.error(f"Error inesperado en alta de cliente desde CLI: {e}")

    input("\n\n\nPresione Enter para continuar...")

def flujo_resumen_de_banco(banco: Banco) -> None:

    """
        Ejecuta el flujo para mostrar un resumen general del estado del banco.

        Limpia la pantalla e invoca el método de resumen institucional de la clase Banco,
        registrando la acción en el sistema de logs.

        Args:
            banco (Banco): Instancia del banco del cual se generará el resumen.

        Returns:
            None

        Examples:
            >>> # flujo_resumen_de_banco(banco_instancia)
    """

    limpiar_pantalla()

    print(f"--- RESUMEN DEL BANCO {banco.get_nombre()} ---\n")

    banco.resumen()

    logger.info("Resumen general del banco consultado desde CLI.")

    input("\nPresione Enter para continuar...")

def flujo_salida_guardado_programa(banco) -> None:

    """
        Gestiona el cierre seguro de la aplicación mediante la persistencia de los datos.

        Limpia la pantalla, invoca la función de guardado en archivo JSON y realiza
        una pausa antes de finalizar la ejecución del CLI.

        Args:
            banco (Banco): Instancia del banco cuyos datos serán persistidos.

        Returns:
            None

        Examples:
            >>> # flujo_salida_guardado_programa(banco_instancia)
    """

    limpiar_pantalla()
    print("\n\nGuardando datos y saliendo del sistema... ¡Hasta luego!")
    logger.info("Procediendo a guardar datos y cerrar el sistema CLI...")
    guardar_datos(banco)
    time.sleep(1.5)

def flujo_crear_cuenta_ahorro_cli(banco: Banco, cliente: Cliente) -> None:

    """
        Ejecuta el flujo interactivo para crear y asociar una cuenta de ahorro a un cliente.

        Genera de forma aleatoria un número de cuenta válido de 22 dígitos, instancia
        una CuentaAhorro y la añade a la cartera del cliente seleccionado.

        Args:
            banco (Banco): Instancia del banco al que pertenece el cliente.
            cliente (Cliente): Instancia del cliente titular de la nueva cuenta.

        Returns:
            None

        Examples:
            >>> # flujo_crear_cuenta_ahorro_cli(banco_instancia, cliente_instancia)
    """

    limpiar_pantalla()
    print("--- CREAR CUENTA DE AHORRO ---\n")

    num_cuenta = ''.join(random.choices(string.digits, k=22))

    try:

        nueva_cuenta = CuentaAhorro(num_cuenta)
        cliente.agregar_cuenta(nueva_cuenta)

        print("\n ¡Cuenta de Ahorro creada con éxito!")
        logger.info(
        f"Cuenta de Ahorro agregada exitosamente desde CLI: "
        f"Cuenta {num_cuenta} para Cliente DNI {cliente.get_dni()}"
        )

    except ValueError as e:

        print(f"\n Error al crear la cuenta: {e}")
        logger.error(f"Error en creación de Cuenta de Ahorro desde CLI [ValueError]: {e}")

    except Exception as e:

        print(f"\n Ocurrió un error inesperado: {e}")
        logger.error(f"Error inesperado en creación de Cuenta de Ahorro desde CLI: {e}")

    input("\nPresione Enter para continuar...")
        
def flujo_crear_cuenta_corriente_cli(banco: Banco, cliente: Cliente) -> None:

    """
        Ejecuta el flujo interactivo para crear y asociar una cuenta corriente a un cliente.

        Genera un número de cuenta aleatorio de 22 dígitos, solicita opcionalmente el límite
        de descubierto (utilizando uno por defecto si no se ingresa valor) y añade la cuenta al cliente.

        Args:
            banco (Banco): Instancia del banco al que pertenece el cliente.
            cliente (Cliente): Instancia del cliente titular de la cuenta corriente.

        Returns:
            None

        Examples:
            >>> # flujo_crear_cuenta_corriente_cli(banco_instancia, cliente_instancia)
    """

    limpiar_pantalla()
    print("--- CREAR CUENTA CORRIENTE ---\n")

    num_cuenta = ''.join(random.choices(string.digits, k=22))
    descubierto_input = input("Ingrese el descubierto (Enter para usar $500.00 por defecto): ").strip()

    try:

        monto_descubierto = Decimal(descubierto_input) if descubierto_input else None

        nueva_cuenta = CuentaCorriente(num_cuenta, descubierto=monto_descubierto)
        cliente.agregar_cuenta(nueva_cuenta)
        print("\n ¡Cuenta Corriente creada con éxito!")
        logger.info(
            f"Cuenta Corriente agregada exitosamente desde CLI: "
            f"Cuenta {num_cuenta} para Cliente DNI {cliente.get_dni()}"
        )
    except ValueError as e:
        
        print(f"\n Error al crear la cuenta: {e}")
        logger.error(f"Error en creación de Cuenta Corriente desde CLI [ValueError]: {e}")
    
    except Exception as e:
        
        print(f"\n Ocurrió un error inesperado: {e}")
        logger.error(f"Error inesperado en creación de Cuenta Corriente desde CLI: {e}")
                                                        
    input("\nPresione Enter para continuar...")

def flujo_depositar_cli(banco: Banco, cliente: Cliente) -> None:

    """
        Gestiona el flujo interactivo por consola para realizar un depósito de dinero
        en una cuenta específica asociada al cliente.

        Verifica si el cliente posee cuentas; de ser así, lista las opciones disponibles,
        solicita el número de cuenta y el monto a depositar, procesando la operación y
        registrando tanto el éxito como los posibles errores en los logs.

        Args:
            banco (Banco): Instancia del banco actual.
            cliente (Cliente): Instancia del cliente titular de las cuentas.

        Returns:
            None

        Examples:
            >>> # flujo_depositar_cli(banco, cliente)
    """

    limpiar_pantalla()
    print(f"--- DEPOSITAR PARA {cliente.get_nombre()} ---\n")
    
    if not cliente.cuentas:

        print(" El cliente no posee cuentas asociadas para depositar.")
        logger.warning(f"Intento de depósito fallido en CLI: Cliente {cliente.get_dni()} sin cuentas asociadas.")
        
    else:

        print("Cuentas disponibles:")

        for idx, c in enumerate(cliente.cuentas, 1):
            print(f"{idx}. {c}")
        
        num_cuenta = input("\nIngrese el número de cuenta: ").strip()
        
        try:

            monto_str = input("Ingrese el monto a depositar: ").strip()
            monto = Decimal(monto_str)
            
            cliente.depositar_en_cuenta(num_cuenta, monto)
            print("\n¡Depósito realizado con éxito!")
            logger.info(f"Depósito en CLI exitoso: Cuenta {num_cuenta}, Monto ${monto}")
            
        except (ValueError, decimal.InvalidOperation) as e:

            print(f"\nError: Monto inválido o problema en el depósito ({e})")
            logger.error(f"Error de depósito en CLI [Monto/Valor]: {e}")
            
    input("\nPresione Enter para continuar...")

def flujo_extraer_cli(banco: Banco, cliente: Cliente) -> None:

    """
        Gestiona el flujo interactivo por consola para realizar una extracción de fondos
        de una cuenta específica del cliente.

        Comprueba la existencia de cuentas, muestra el listado al usuario, captura
        el número de cuenta y el monto a retirar, aplicando las reglas de validación
        de saldo o descubierto según corresponda.

        Args:
            banco (Banco): Instancia del banco actual.
            cliente (Cliente): Instancia del cliente titular de la cuenta.

        Returns:
            None

        Examples:
            >>> # flujo_extraer_cli(banco, cliente)
    """

    limpiar_pantalla()
    print(f"--- EXTRAER PARA {cliente.get_nombre()} ---\n")
    
    if not cliente.cuentas:

        print("El cliente no posee cuentas asociadas para extraer.")
        logger.warning(f"Intento de extracción fallido en CLI: Cliente {cliente.get_dni()} sin cuentas asociadas.")
        
    else:

        print("Cuentas disponibles:")
        
        for c in cliente.cuentas:
            print(f" - {c}")
        
        num_cuenta = input("\nIngrese el número de cuenta: ").strip()
        
        try:

            monto_str = input("Ingrese el monto a extraer: ").strip()
            monto = Decimal(monto_str)
            
            cliente.extraer_de_cuenta(num_cuenta, monto)
            print("\n¡Extracción realizada con éxito!")
            logger.info(f"Extracción en CLI exitosa: Cuenta {num_cuenta}, Monto ${monto}")
            
        except (ValueError, decimal.InvalidOperation) as e:

            print(f"\nError: Monto inválido o problema en la extracción ({e})")
            logger.error(f"Error de extracción en CLI [Monto/Valor]: {e}")
            
    input("\nPresione Enter para continuar...")

def flujo_crear_cuenta_cli(banco: Banco, cliente: Cliente) -> None: #pragma: no cover

    """
        Controla el submenú interactivo para la creación de cuentas asociadas a un cliente.

        Mantiene un bucle que permite elegir entre crear una cuenta de ahorro,
        una cuenta corriente o regresar al menú anterior.

        Args:
            banco (Banco): Instancia del banco.
            cliente (Cliente): Instancia del cliente al que se le creará la cuenta.

        Returns:
            None

        Examples:
            >>> # flujo_crear_cuenta_cli(banco, cliente)
    """

    flag_crear_cuenta = True

    while flag_crear_cuenta:

        limpiar_pantalla()

        option_crear_cuenta = mostrar_menu_crear_cuenta()

        match option_crear_cuenta:

            case "1": flujo_crear_cuenta_ahorro_cli(banco, cliente)

            case "2": flujo_crear_cuenta_corriente_cli(banco, cliente)

            case "3": flag_crear_cuenta = False

            case _: 

                print("\n Opción inválida. Por favor, elija una opción del 1 al 3.")
                time.sleep(1.5)

def flujo_mostrar_clientes_en_gestion(banco: Banco) -> None:

    """
        Muestra en pantalla el listado completo de todos los clientes registrados en el banco.

        Recorre la cartera de clientes de la entidad e imprime su representación en texto
        o un mensaje indicando que no existen registros previos.

        Args:
            banco (Banco): Instancia del banco que contiene la lista de clientes.

        Returns:
            None

        Examples:
            >>> # flujo_mostrar_clientes_en_gestion(banco)
    """

    limpiar_pantalla()

    if banco.clientes:

        print("\n--------------------------------------------\n")

        for cl in banco.clientes: 
            print("++++++++++++++++++++++++++++++++++++++++++++\n")
            print(f"{cl}\n")
            #print("++++++++++++++++++++++++++++++++++++++++++++\n")

        print("\n--------------------------------------------\n")
        logger.info("Listado de clientes consultado exitosamente desde CLI.")

    else:

        print("\n")

        print("Sin Clientes registrados...")

        print("\n")

        logger.info("Consulta de listado de clientes vacía desde CLI.")

    input("\nPresione Enter para continuar...")

def flujo_seleccionar_clientes_en_gestion_cli(banco: Banco) -> None: # pragma: no cover

    """
        Gestiona el flujo de búsqueda y selección de un cliente específico por su DNI.

        Si el cliente es hallado en el sistema, abre un submenú interactivo de operaciones
        (crear cuentas, depositar, extraer) específico para dicho usuario.

        Args:
            banco (Banco): Instancia del banco donde se realizará la búsqueda.

        Returns:
            None

        Examples:
            >>> # flujo_seleccionar_clientes_en_gestion_cli(banco)
    """

    limpiar_pantalla()
    print("--- SELECCIONAR CLIENTE ---\n")

    dni_cliente = input("Ingrese el DNI del Cliente: ").strip().replace(".", "")

    cliente_encontrado = banco.buscar_cliente_por_dni(dni_cliente)

    if cliente_encontrado:

        print(f"\n¡Cliente seleccionado con éxito: {cliente_encontrado.get_nombre()}!")
        logger.info(f"Cliente seleccionado correctamente en CLI: DNI {dni_cliente}")

        flag_clientes_operaciones_option = True

        while flag_clientes_operaciones_option:

            limpiar_pantalla()
            option_operaciones_clientes = mostrar_menu_operaciones_cliente(cliente_encontrado)

            match option_operaciones_clientes:

                case "1": flujo_crear_cuenta_cli(banco, cliente_encontrado)

                case "2": flujo_depositar_cli(banco, cliente_encontrado)

                case "3": flujo_extraer_cli(banco, cliente_encontrado)

                case "4": flag_clientes_operaciones_option = False

                case _: 

                    print("\n Opción inválida. Por favor, elija una opción del 1 al 3.")
                    time.sleep(1.5)

    else:

        print("\n No se encontró ningún cliente registrado con ese DNI.")
        logger.warning(f"Intento de selección de cliente fallido en CLI: DNI {dni_cliente} no encontrado.")
        time.sleep(1.5)

def flujo_gestion_clientes_cli(banco: Banco) -> None: # pragma: no cover

    """
        Controla el menú principal de gestión de clientes dentro del CLI.

        Mantiene un bucle interactivo que permite listar todos los clientes registrados
        o seleccionar uno en particular para operar sobre sus cuentas.

        Args:
            banco (Banco): Instancia del banco en gestión.

        Returns:
            None

        Examples:
            >>> # flujo_gestion_clientes_cli(banco)
    """

    flag_cliente_option = True

    while flag_cliente_option:

        limpiar_pantalla()
        option = mostrar_menu_gestionar_cliente()

        match option:

            case "1": flujo_mostrar_clientes_en_gestion(banco)

            case "2": flujo_seleccionar_clientes_en_gestion_cli(banco)

            case "3": flag_cliente_option = False

            case _: 

                print("\nOpción inválida. Por favor, elija una opción del 1 al 3.")
                time.sleep(1.5)