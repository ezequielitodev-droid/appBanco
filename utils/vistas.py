import os
import time

def limpiar_pantalla() -> None:

    """
        Limpia la terminal de la consola según el sistema operativo.

        Ejecuta el comando 'cls' si se ejecuta en entornos Windows ('nt')
        o 'clear' para sistemas basados en Unix (Linux / macOS).

        Returns:
            None

        Examples:
            >>> limpiar_pantalla()
    """

    """Limpia la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_bienvenida(banco) -> None:

    """
        Muestra el mensaje de bienvenida inicial de la aplicación en pantalla.

        Limpia la terminal, imprime una cabecera con el nombre del banco
        proporcionado por el objeto y realiza una pausa de 2 segundos para
        permitir que el usuario lea el mensaje.

        Args:
            banco: Instancia del objeto Banco de la cual se obtiene el nombre.

        Returns:
            None

        Examples:
            >>> class BancoMock:
            ...     def get_nombre(self): return "Nación"
            >>> # mostrar_bienvenida(BancoMock())
    """
    
    limpiar_pantalla()
    print("\n\n")
    print(f"Bienvenido al Banco {banco.get_nombre()}!!\n")
    print("\n\n")
    # Para hacer una pausa y que el mensaje se lea antes de continuar:
    time.sleep(2) 

def mostrar_menu_principal(banco) -> str:

    """
        Muestra el menú principal de la aplicación y captura la opción elegida.

        Limpia la terminal y presenta las opciones principales de navegación
        (dar de alta cliente, gestionar cliente, mostrar resumen o salir).

        Args:
            banco: Instancia del objeto Banco para mostrar su nombre en el título.

        Returns:
            str: La opción seleccionada por el usuario como una cadena limpia de espacios.

        Examples:
            >>> # Resultado simulado de la selección del usuario en consola:
            >>> opcion = "1"
            >>> isinstance(opcion, str)
            True
    """

    limpiar_pantalla()
    print("\n" + "="*40)
    print(f"--- MENÚ PRINCIPAL: Banco {banco.get_nombre()} ---")
    print("="*40)
    print("1. Dar de alta cliente")
    print("2. Gestionar cliente")
    print("3. Mostrar resumen del banco")
    print("4. Salir")
    print("="*40)
    
    return input("Seleccione una opción (1-4): ").strip()

def mostrar_menu_gestionar_cliente() -> str:

    """
        Muestra el submenú de gestión de clientes y captura la opción elegida.

        Presenta las opciones para listar clientes existentes, seleccionar
        un cliente específico para operar o regresar al menú anterior.

        Returns:
            str: La opción seleccionada por el usuario como una cadena limpia de espacios.

        Examples:
            >>> # menu_opcion = mostrar_menu_gestionar_cliente()
    """

    print("\n--- GESTIÓN DE CLIENTES ---")
    print("1. Mostrar Clientes")
    print("2. Seleccionar Clientes")
    print("3. Atras")

    return input("\nElija una opción (1-3): ").strip()

def mostrar_menu_operaciones_cliente(cliente) -> str:

    """
        Muestra el menú de operaciones disponibles para un cliente seleccionado.

        Presenta las acciones que se pueden realizar sobre las cuentas del cliente
        (crear cuenta, depositar, extraer o regresar).

        Args:
            cliente: Instancia del Cliente activo sobre el cual se operará.

        Returns:
            str: La opción seleccionada por el usuario como una cadena limpia de espacios.

        Examples:
            >>> class ClienteMock:
            ...     def get_nombre(self): return "María Gómez"
            >>> # mostrar_menu_operaciones_cliente(ClienteMock())
    """

    print(f"\n--- CLIENTE: {cliente.get_nombre()} ---")
    print("1. Crear cuenta")
    print("2. Depositar")
    print("3. Extraer")
    print("4. Atrás")

    return input("\nElija una opción (1-4): ").strip()

def mostrar_menu_crear_cuenta() -> str:

    """
        Muestra el submenú para la creación de un nuevo tipo de cuenta bancaria.

        Presenta las opciones para crear una cuenta de ahorro o una cuenta corriente.

        Returns:
            str: La opción seleccionada por el usuario como una cadena limpia de espacios.

        Examples:
            >>> # opcion_cuenta = mostrar_menu_crear_cuenta()
    """
    print("\n--- CREAR CUENTA ---")
    print("1. Crear Cuenta ahorro")
    print("2. Crear Cuenta corriente")
    print("3. Atrás")

    return input("\nElija una opción (1-3): ").strip()