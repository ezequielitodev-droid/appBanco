# Pruebas para la lógica interactiva del CLI (core/core_cli.py)

from decimal import Decimal
import pytest

from models.objects_models import Banco, CuentaAhorro, CuentaCorriente
from core.core_cli import (
    flujo_dar_alta_cliente,
    flujo_resumen_de_banco,
    flujo_salida_guardado_programa,
    flujo_crear_cuenta_ahorro_cli,
    flujo_crear_cuenta_corriente_cli,
    flujo_depositar_cli,
    flujo_extraer_cli,
    flujo_crear_cuenta_cli,
    flujo_mostrar_clientes_en_gestion,
    flujo_seleccionar_clientes_en_gestion_cli,
    flujo_gestion_clientes_cli,
)
import core.core_cli as core_cli_mod

NUMERO_PRUEBA = "1" * 22

def test_flujo_dar_alta_cliente_exitoso(monkeypatch) -> None:

    """
        Prueba que el flujo de alta de cliente en el CLI registre exitosamente
        a un nuevo cliente simulando los inputs de nombre y DNI.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos del sistema.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    
    # Simulamos inputs: nombre y DNI, luego el Enter final para continuar
    inputs = iter(["Carlos", "12345678", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_dar_alta_cliente(banco)
    
    assert len(banco.clientes) == 1
    assert banco.clientes[0].get_nombre() == "Carlos"

def test_flujo_dar_alta_cliente_dni_duplicado(monkeypatch) -> None:

    """
        Prueba que el flujo de alta de cliente en el CLI capture adecuadamente
        el ValueError al intentar registrar un DNI duplicado sin interrumpir la ejecución.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos del sistema.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    banco.alta_cliente("Carlos", "12345678")
    
    # Intentamos dar de alta el mismo DNI
    inputs = iter(["Carlos 2", "12345678", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    # No debe romper por excepción no manejada, sino atrapar el ValueError
    flujo_dar_alta_cliente(banco)
    assert len(banco.clientes) == 1  # Sigue siendo 1 solo

def test_flujo_resumen_de_banco(monkeypatch, capsys) -> None:

    """
        Prueba que el flujo interactivo de resumen del banco imprima correctamente
        la información general en la salida estándar de la terminal.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.
            capsys: Fixture para capturar la salida estándar (stdout).

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    banco.alta_cliente("Ana", "87654321")
    
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_resumen_de_banco(banco)
    captured = capsys.readouterr()
    assert "RESUMEN DEL BANCO BancoPrueba" in captured.out

def test_flujo_salida_guardado_programa(monkeypatch) -> None:

    """
        Prueba que el flujo de salida y guardado del programa se ejecute
        correctamente simulando las pausas de tiempo y comandos del sistema.

        Args:
            monkeypatch: Fixture de pytest para simular time.sleep y os.system.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("time.sleep", lambda s: None)
    
    # Verificamos que guarde y ejecute sin errores
    flujo_salida_guardado_programa(banco)

def test_flujo_crear_cuenta_ahorro_cli(monkeypatch) -> None:

    """
        Prueba que el flujo CLI para crear una cuenta de ahorro asocie correctamente
        la nueva cuenta al cliente especificado.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Lucia", "11223344")
    
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    
    flujo_crear_cuenta_ahorro_cli(banco, cliente)
    assert len(cliente.cuentas) == 1
    assert isinstance(cliente.cuentas[0], CuentaAhorro)

def test_flujo_crear_cuenta_corriente_cli_por_defecto(monkeypatch) -> None:

    """
        Prueba que el flujo CLI para crear una cuenta corriente configure por defecto
        el monto de descubierto cuando se ingresan valores vacíos.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Pedro", "22334455")
    
    # Simulamos presionar Enter (descubierto por defecto) y el Enter final
    inputs = iter(["", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_crear_cuenta_corriente_cli(banco, cliente)
    assert len(cliente.cuentas) == 1
    assert isinstance(cliente.cuentas[0], CuentaCorriente)
    assert cliente.cuentas[0].get_descubierto() == Decimal("500")

def test_flujo_depositar_cli_sin_cuentas(monkeypatch) -> None:

    """
        Prueba que el flujo de depósito en el CLI maneje correctamente el escenario
        en el que un cliente no posee cuentas asociadas.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Marcos", "33445566")
    
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    
    flujo_depositar_cli(banco, cliente)
    assert len(cliente.cuentas) == 0

def test_flujo_depositar_cli_con_cuenta(monkeypatch) -> None:

    """
        Prueba que el flujo de depósito en el CLI incremente correctamente el saldo
        de una cuenta existente al recibir un monto válido.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Sofía", "44556677")
    cuenta = CuentaAhorro(NUMERO_PRUEBA)
    cliente.agregar_cuenta(cuenta)
    
    # Ingresamos el número de cuenta y el monto a depositar
    inputs = iter([NUMERO_PRUEBA, "1000", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_depositar_cli(banco, cliente)
    assert cuenta.get_saldo() == Decimal("1000")

def test_flujo_extraer_cli_con_cuenta(monkeypatch) -> None:

    """
        Prueba que el flujo de extracción en el CLI reduzca correctamente el saldo
        de una cuenta existente al retirar un monto válido.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Mateo", "55667788")
    cuenta = CuentaAhorro(NUMERO_PRUEBA, saldo=Decimal("2000"))
    cliente.agregar_cuenta(cuenta)
    
    # Ingresamos número de cuenta, monto a extraer, y Enter final
    inputs = iter([NUMERO_PRUEBA, "500", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_extraer_cli(banco, cliente)
    assert cuenta.get_saldo() == Decimal("1500")

#Imposible testear, no lo entiendo...
"""def test_flujo_gestion_clientes_menu(monkeypatch) -> None:
    banco = Banco("BancoPrueba")
    
    # Devolvemos "3" directamente en la primera llamada para romper el while al instante
    monkeypatch.setattr("utils.vistas.mostrar_menu_gestionar_cliente", lambda: "3")
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("time.sleep", lambda s: None)
    
    # Esto corre una sola vez el while, encuentra el "3", sale y termina sin riesgo
    flujo_gestion_clientes_cli(banco)"""

def test_flujo_mostrar_clientes_con_y_sin_clientes(monkeypatch, capsys) -> None:

    """
        Prueba que el flujo para mostrar clientes en gestión maneje adecuadamente
        tanto el estado sin clientes como el listado con clientes registrados.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.
            capsys: Fixture para capturar la salida estándar (stdout).

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    # 1. Sin clientes
    flujo_mostrar_clientes_en_gestion(banco)
    captured = capsys.readouterr()
    assert "Sin Clientes registrados" in captured.out
    
    # 2. Con clientes
    banco.alta_cliente("Esteban", "77889900")
    flujo_mostrar_clientes_en_gestion(banco)
    captured = capsys.readouterr()
    assert "Esteban" in captured.out

def test_flujo_seleccionar_cliente_no_encontrado(monkeypatch) -> None:

    """
        Prueba que el flujo de selección de clientes en el CLI gestione correctamente
        el escenario en el que se ingresa un DNI inexistente.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    
    monkeypatch.setattr("builtins.input", lambda prompt="": "99999999")
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("time.sleep", lambda s: None)
    
    flujo_seleccionar_clientes_en_gestion_cli(banco)


def test_flujo_crear_cuenta_menu_opciones(monkeypatch) -> None:

    """
        Prueba que el menú interactivo para crear cuentas en el CLI procese
        correctamente las opciones seleccionadas mediante el mock del menú.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y funciones del menú.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Valeria", "66778899")
    
    # Controlamos las llamadas con un contador seguro
    intentos = 0
    def mock_menu_crear():
        nonlocal intentos
        intentos += 1
        if intentos == 1:
            return "1"  # Primera vez: crear cuenta de ahorro
        return "3"     # Segunda vez: salir del bucle
    
    monkeypatch.setattr("core.core_cli.mostrar_menu_crear_cuenta", mock_menu_crear)
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("time.sleep", lambda s: None)
    
    flujo_crear_cuenta_cli(banco, cliente)
    assert len(cliente.cuentas) == 1

def test_flujo_dar_alta_cliente_error_inesperado(monkeypatch) -> None:

    """
        Prueba que el flujo de alta de cliente en el CLI capture de forma segura
        excepciones genéricas imprevistas (RuntimeError).

        Args:
            monkeypatch: Fixture de pytest para simular inputs y forzar errores.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    
    # Forzamos que banco.alta_cliente lance un error genérico que no sea ValueError (ej. RuntimeError)
    def mock_alta_error(*args, **kwargs):
        raise RuntimeError("Falla crítica de sistema")
        
    monkeypatch.setattr(banco, "alta_cliente", mock_alta_error)
    inputs = iter(["Carlos", "12345678", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    # Debe capturar el Exception genérico sin romper el test
    flujo_dar_alta_cliente(banco)

def test_flujo_crear_cuenta_ahorro_error_inesperado(monkeypatch) -> None:

    """
        Prueba que el flujo de creación de cuenta de ahorro en el CLI gestione
        adecuadamente errores inesperados durante su instanciación.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y forzar excepciones.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Lucia", "11223344")
    
    # Forzamos un error inesperado al instanciar CuentaAhorro o agregarla
    monkeypatch.setattr("core.core_cli.CuentaAhorro", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("Error raro")))
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    
    flujo_crear_cuenta_ahorro_cli(banco, cliente)

def test_flujo_crear_cuenta_corriente_monto_invalido(monkeypatch) -> None:

    """
        Prueba que el flujo de creación de cuenta corriente en el CLI capture
        formatos de descubierto inválidos (texto) sin registrar cuentas erróneas.

        Args:
            monkeypatch: Fixture de pytest para simular inputs inválidos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Pedro", "22334455")
    
    # Ingresamos un texto que falle al convertirse en Decimal("...")
    inputs = iter(["texto_invalido", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_crear_cuenta_corriente_cli(banco, cliente)
    assert len(cliente.cuentas) == 0  # No se creó por el ValueError

def test_flujo_depositar_cli_monto_invalido(monkeypatch) -> None:

    """
        Prueba que el flujo de depósito en el CLI mantenga intacto el saldo
        cuando se ingresa un monto con formato inválido (letras).

        Args:
            monkeypatch: Fixture de pytest para simular inputs inválidos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Sofía", "44556677")
    cuenta = CuentaAhorro(NUMERO_PRUEBA)
    cliente.agregar_cuenta(cuenta)
    
    # Número de cuenta válido, pero monto inválido (letras en lugar de número)
    inputs = iter([NUMERO_PRUEBA, "abc", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_depositar_cli(banco, cliente)
    assert cuenta.get_saldo() == Decimal("0")  # El saldo no cambió

def test_flujo_extraer_cli_sin_cuentas(monkeypatch) -> None:

    """
        Prueba que el flujo de extracción en el CLI maneje de forma controlada
        el caso en que un cliente carece de cuentas asociadas.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y comandos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Mateo", "55667788")
    
    monkeypatch.setattr("os.system", lambda cmd: None)
    # Importante: mockeamos input para que devuelva "" ante la pausa final
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    
    flujo_extraer_cli(banco, cliente)
    assert len(cliente.cuentas) == 0

def test_flujo_extraer_cli_monto_invalido(monkeypatch) -> None:

    """
        Prueba que el flujo de extracción en el CLI conserve el saldo original
        al ingresar un monto con formato inválido.

        Args:
            monkeypatch: Fixture de pytest para simular inputs inválidos.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Mateo", "55667788")
    cuenta = CuentaAhorro(NUMERO_PRUEBA, saldo=Decimal("2000"))
    cliente.agregar_cuenta(cuenta)
    
    # Número de cuenta válido, pero monto inválido para extraer
    inputs = iter([NUMERO_PRUEBA, "xyz", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_extraer_cli(banco, cliente)
    assert cuenta.get_saldo() == Decimal("2000")  # El saldo quedó intacto

def test_flujo_dar_alta_cliente_excepcion_general(monkeypatch) -> None:

    """
        Prueba que el flujo de alta de cliente en el CLI capture correctamente
        cualquier excepción general no tipada (`except Exception as e`).

        Args:
            monkeypatch: Fixture de pytest para forzar excepciones genéricas.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    
    # Forzamos un error genérico (que no sea ValueError) para cubrir el "except Exception as e"
    def mock_alta_error(*args, **kwargs):
        raise RuntimeError("Error de sistema inesperado")
        
    monkeypatch.setattr(banco, "alta_cliente", mock_alta_error)
    inputs = iter(["Carlos", "12345678", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_dar_alta_cliente(banco)

def test_flujo_crear_cuenta_ahorro_excepcion_general(monkeypatch) -> None:

    """
        Prueba que el flujo de creación de cuenta de ahorro en el CLI capture
        adecuadamente una excepción general inesperada.

        Args:
            monkeypatch: Fixture de pytest para forzar excepciones en tiempo de ejecución.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Lucia", "11223344")
    
    # Forzamos un error genérico al instanciar la cuenta de ahorro
    monkeypatch.setattr("core.core_cli.CuentaAhorro", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("Falla crítica")))
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_crear_cuenta_ahorro_cli(banco, cliente)

def test_flujo_crear_cuenta_corriente_excepcion_general(monkeypatch) -> None:

    """
        Prueba que el flujo de creación de cuenta corriente en el CLI capture
        correctamente excepciones generales inesperadas durante su proceso.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y forzar errores.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Pedro", "22334455")
    
    # Forzamos un error genérico al instanciar la cuenta corriente
    monkeypatch.setattr("core.core_cli.CuentaCorriente", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("Falla crítica corriente")))
    inputs = iter(["500", ""]) # Para el input del descubierto y el de la pausa final
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_crear_cuenta_corriente_cli(banco, cliente)

def test_flujo_crear_cuenta_ahorro_value_error(monkeypatch) -> None:

    """
        Prueba que el flujo de creación de cuenta de ahorro en el CLI capture
        correctamente los errores de valor (`ValueError`).

        Args:
            monkeypatch: Fixture de pytest para simular inputs y forzar ValueError.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Lucia", "11223344")
    
    # Forzamos un ValueError al instanciar CuentaAhorro para atrapar el primer except
    monkeypatch.setattr("core.core_cli.CuentaAhorro", lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("Número de cuenta inválido")))
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_crear_cuenta_ahorro_cli(banco, cliente)

def test_flujo_crear_cuenta_corriente_value_error(monkeypatch) -> None:

    """
        Prueba que el flujo de creación de cuenta corriente en el CLI capture
        correctamente los errores de valor al producirse un fallo interno de validación.

        Args:
            monkeypatch: Fixture de pytest para simular inputs y forzar ValueError.

        Returns:
            None
    """

    banco = Banco("BancoPrueba")
    cliente = banco.alta_cliente("Pedro", "22334455")
    
    # Forzamos que CuentaCorriente lance un ValueError (con un descubierto válido "500" para que el Decimal pase antes)
    monkeypatch.setattr("core.core_cli.CuentaCorriente", lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("Error de validación en cuenta corriente")))
    
    # 1. "500" (descubierto válido para el Decimal)
    # 2. "" (Enter para la pausa final)
    inputs = iter(["500", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("os.system", lambda cmd: None)
    
    flujo_crear_cuenta_corriente_cli(banco, cliente)
    assert len(cliente.cuentas) == 0

def test_importar_vistas_cli():

    """
        Prueba que el módulo de vistas CLI pueda importarse correctamente sin errores.

        Returns:
            None
    """
    
    import vistas.cli
    assert vistas.cli is not None