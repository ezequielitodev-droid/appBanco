import os
import time

def limpiar_pantalla() -> None:
    """Limpia la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_bienvenida(banco) -> None:
    """Muestra el mensaje de bienvenida inicial."""
    limpiar_pantalla()
    print("\n\n")
    print(f"Bienvenido al Banco {banco.get_nombre()}!!\n")
    print("\n\n")
    # Para hacer una pausa y que el mensaje se lea antes de continuar:
    time.sleep(2) 

def mostrar_menu_principal(banco) -> str:
    """Muestra el menú principal y retorna la opción elegida."""
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
    """Muestra el menú de gestión de cliente y retorna la opción elegida."""
    print("\n--- GESTIÓN DE CLIENTES ---")
    print("1. Mostrar Clientes")
    print("2. Seleccionar Clientes")
    print("3. Atras")
    return input("\nElija una opción (1-3): ").strip()


def mostrar_menu_operaciones_cliente(cliente) -> str:
    """Muestra el menú de operaciones del cliente y retorna la opción elegida."""
    print(f"\n--- CLIENTE: {cliente.get_nombre()} ---")
    print("1. Crear cuenta")
    print("2. Depositar")
    print("3. Extraer")
    print("4. Atrás")
    return input("\nElija una opción (1-4): ").strip()


def mostrar_menu_crear_cuenta() -> str:
    """Muestra el menú de creación de cuenta y retorna la opción elegida."""
    print("\n--- CREAR CUENTA ---")
    print("1. Crear Cuenta ahorro")
    print("2. Crear Cuenta corriente")
    print("3. Atrás")
    return input("\nElija una opción (1-3): ").strip()