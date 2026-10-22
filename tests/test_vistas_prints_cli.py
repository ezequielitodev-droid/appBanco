# Archivo para probar las vistas y menús de consola:

import time
import pytest

from utils.vistas import (
    limpiar_pantalla,
    mostrar_bienvenida,
    mostrar_menu_principal,
    mostrar_menu_gestionar_cliente,
    mostrar_menu_operaciones_cliente,
    mostrar_menu_crear_cuenta,
)
from models.objects_models import Banco, Cliente

def test_limpiar_pantalla(monkeypatch) -> None:

    """
        Prueba que la función `limpiar_pantalla` invoque correctamente al comando del sistema
        operativo para limpiar la consola, utilizando un mock sobre `os.system`.

        Args:
            monkeypatch: Fixture de pytest para simular o reemplazar funciones del sistema.

        Returns:
            None

        Examples:
            >>> # test_limpiar_pantalla(monkeypatch)
    """

    # Simulamos os.system para que no limpie la terminal real durante el test
    called = False
    def mock_system(cmd):
        nonlocal called
        called = True
    
    monkeypatch.setattr("os.system", mock_system)
    limpiar_pantalla()
    assert called is True

def test_mostrar_bienvenida(monkeypatch) -> None:

    """
        Prueba que la función `mostrar_bienvenida` se ejecute con éxito sin lanzar excepciones,
        mockeando el tiempo de espera (`time.sleep`) y las llamadas al sistema operativo (`os.system`).

        Args:
            monkeypatch: Fixture de pytest para simular funciones de tiempo y sistema.

        Returns:
            None

        Examples:
            >>> # test_mostrar_bienvenida(monkeypatch)
    """

    # Evitamos que time.sleep pause el test 2 segundos y simulamos os.system
    monkeypatch.setattr(time, "sleep", lambda s: None)
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    banco = Banco("Galicia")
    # Debe ejecutarse sin lanzar excepciones
    mostrar_bienvenida(banco)

def test_mostrar_menu_principal(monkeypatch) -> None:

    """
        Prueba que la función `mostrar_menu_principal` despliegue el menú del banco
        y retorne la opción ingresada por el usuario simulando la entrada por consola (`input`).

        Args:
            monkeypatch: Fixture de pytest para simular el comportamiento de `input` y `os.system`.

        Returns:
            None

        Examples:
            >>> # test_mostrar_menu_principal(monkeypatch)
    """

    monkeypatch.setattr("os.system", lambda cmd: None)
    # Simulamos que el usuario ingresa la opción "1"
    monkeypatch.setattr("builtins.input", lambda prompt="": "1")
    
    banco = Banco("Galicia")
    opcion = mostrar_menu_principal(banco)
    assert opcion == "1"

def test_mostrar_menu_gestionar_cliente(monkeypatch) -> None:

    """
        Prueba que la función `mostrar_menu_gestionar_cliente` capture la entrada del usuario
        y retorne correctamente la opción seleccionada para la gestión de clientes.

        Args:
            monkeypatch: Fixture de pytest para simular la entrada estándar de consola (`input`).

        Returns:
            None

        Examples:
            >>> # test_mostrar_menu_gestionar_cliente(monkeypatch)
    """
    
    # Simulamos que el usuario ingresa la opción "2"
    monkeypatch.setattr("builtins.input", lambda prompt="": "2")
    
    opcion = mostrar_menu_gestionar_cliente()
    assert opcion == "2"

def test_mostrar_menu_operaciones_cliente(monkeypatch) -> None:

    """
        Prueba que la función `mostrar_menu_operaciones_cliente` reciba una instancia de `Cliente`
        y devuelva la opción seleccionada mediante la simulación de entrada de texto.

        Args:
            monkeypatch: Fixture de pytest para simular el valor retornado por `input`.

        Returns:
            None

        Examples:
            >>> # test_mostrar_menu_operaciones_cliente(monkeypatch)
    """

    # Simulamos que el usuario ingresa la opción "3"
    monkeypatch.setattr("builtins.input", lambda prompt="": "3")
    
    cliente = Cliente("Ana", "12345678")
    opcion = mostrar_menu_operaciones_cliente(cliente)
    assert opcion == "3"

def test_mostrar_menu_crear_cuenta(monkeypatch) -> None:

    """
        Prueba que la función `mostrar_menu_crear_cuenta` retorne la opción elegida
        para la creación de un nuevo tipo de cuenta bancaria.

        Args:
            monkeypatch: Fixture de pytest para simular la función `input`.

        Returns:
            None

        Examples:
            >>> # test_mostrar_menu_crear_cuenta(monkeypatch)
    """
    
    # Simulamos que el usuario ingresa la opción "1"
    monkeypatch.setattr("builtins.input", lambda prompt="": "1")
    
    opcion = mostrar_menu_crear_cuenta()
    assert opcion == "1"