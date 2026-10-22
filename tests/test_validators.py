#Pruebas de los validadores (utils/valitators.py):
#Cada validador devuelve True/False y nunca lanza errores con tipos incorrectos.

#Imports:
 
from datetime import datetime
from decimal import Decimal
 
import pytest
 
from utils.enums import TipoTransaccion
from utils.valitators import (
    es_numero_cuenta_valido,
    es_saldo_cuenta_valido,
    es_historial_cuenta_valido,
    es_descubierto_cuenta_valido,
    es_monto_valido,
    es_nombre_cliente_valido,
    es_dni_cliente_valido,
    es_nombre_banco_valido
)

from models.objects_models import CuentaAhorro

NUMERO_PRUEBA = "1" * 22
 
#Con parametrize, un mismo test se repite por cada valor de la lista
#(pytest lo cuenta como un test por valor).
 
#Numero de cuenta-------------------------------------------------
 
@pytest.mark.parametrize("valor", ["1" * 22, "0" * 22, " " + "1" * 22 + " "])
def test_numero_cuenta_valido(valor) -> None:

    """
        Prueba que la función `es_numero_cuenta_valido` retorne True cuando se le pasan
        cadenas numéricas que cumplen exactamente con la longitud esperada (22 caracteres),
        permitiendo espacios alrededor.

        Args:
            valor (str): Cadena numérica candidata a número de cuenta.

        Returns:
            None

        Examples:
            >>> # test_numero_cuenta_valido("1" * 22)
    """

    assert es_numero_cuenta_valido(valor, 22) is True
 
 
@pytest.mark.parametrize("valor", [
    "1" * 21,            # un digito de menos
    "1" * 23,            # un digito de mas
    "",                  # vacio
    "a" * 22,            # letras
    "1" * 21 + "x",      # una letra al final
    "1111 1111 1111 1111 1111 11",  # espacios en el medio
    None,                # no es str
    12345678901234567890,  # int, no str
])
def test_numero_cuenta_invalido(valor) -> None:

    """
        Prueba que la función `es_numero_cuenta_valido` retorne False cuando el valor
        provisto no cumple con la longitud requerida, contiene caracteres alfanuméricos
        inválidos, espacios internos o no corresponde al tipo de dato esperado.

        Args:
            valor (Any): Valor candidato inválido (cadenas con longitudes incorrectas, letras, nulos, enteros).

        Returns:
            None

        Examples:
            >>> # test_numero_cuenta_invalido("1" * 21)
    """

    assert es_numero_cuenta_valido(valor, 22) is False
 
 
#Saldo------------------------------------------------------------
 
@pytest.mark.parametrize("saldo", [Decimal("0"), Decimal("0.00"), Decimal("100.50")])
def test_saldo_valido(saldo) -> None:

    """
        Prueba que la función `es_saldo_cuenta_valido` retorne True cuando se le pasa
        un objeto Decimal positivo o igual a cero asociado a una cuenta válida.

        Args:
            saldo (Decimal): Objeto decimal que representa un saldo permitido.

        Returns:
            None

        Examples:
            >>> # test_saldo_valido(Decimal("100.50"))
    """

    cuenta = CuentaAhorro(NUMERO_PRUEBA)
    assert es_saldo_cuenta_valido(saldo, cuenta) is True
 
 
@pytest.mark.parametrize("saldo", [Decimal("-0.01"), 100, 100.0, "100", None])
def test_saldo_invalido(saldo) -> None:

    """
        Prueba que la función `es_saldo_cuenta_valido` retorne False ante saldos negativos,
        números enteros, de punto flotante, cadenas de texto o valores nulos.

        Args:
            saldo (Any): Valor candidato inválido para el saldo.

        Returns:
            None

        Examples:
            >>> # test_saldo_invalido(Decimal("-0.01"))
    """

    cuenta = CuentaAhorro(NUMERO_PRUEBA)
    # Usamos type: ignore para el linter si le pasamos tipos incorrectos como int o str al test
    assert es_saldo_cuenta_valido(saldo, cuenta) is False # type: ignore
 
 
#Monto (borde: el 0 NO es valido, a diferencia del saldo)---------
 
def test_monto_valido() -> None:

    """
        Prueba que la función `es_monto_valido` retorne True cuando el monto especificado
        es estrictamente mayor a cero (Decimal positivo).

        Returns:
            None

        Examples:
            >>> # test_monto_valido()
    """

    assert es_monto_valido(Decimal("0.01")) is True
 
 
@pytest.mark.parametrize("monto", [Decimal("0"), Decimal("-5.00"), 10, 10.5, "10", None])
def test_monto_invalido(monto) -> None:

    """
        Prueba que la función `es_monto_valido` retorne False cuando el monto es cero,
        negativo o pertenece a tipos de datos no permitidos (enteros, floats, strings, None).

        Args:
            monto (Any): Valor candidato inválido para el monto de transacción.

        Returns:
            None

        Examples:
            >>> # test_monto_invalido(Decimal("0"))
    """

    assert es_monto_valido(monto) is False
 
 
#Descubierto (borde: el 0 SI es valido)---------------------------
 
@pytest.mark.parametrize("descubierto", [Decimal("0"), Decimal("500.00")])
def test_descubierto_valido(descubierto) -> None:

    """
        Prueba que la función `es_descubierto_cuenta_valido` retorne True cuando se le pasa
        un límite de descubierto en formato Decimal que es mayor o igual a cero.

        Args:
            descubierto (Decimal): Límite de descubierto válido.

        Returns:
            None

        Examples:
            >>> # test_descubierto_valido(Decimal("500.00"))
    """

    assert es_descubierto_cuenta_valido(descubierto) is True
 
 
@pytest.mark.parametrize("descubierto", [Decimal("-1.00"), 500, 500.0, None])
def test_descubierto_invalido(descubierto) -> None:

    """
        Prueba que la función `es_descubierto_cuenta_valido` retorne False ante límites
        de descubierto negativos o provistos en tipos de datos no válidos.

        Args:
            descubierto (Any): Valor candidato inválido para el descubierto.

        Returns:
            None

        Examples:
            >>> # test_descubierto_invalido(Decimal("-1.00"))
    """

    assert es_descubierto_cuenta_valido(descubierto) is False
 
 
#Historial--------------------------------------------------------
 
def _transaccion():
    return (datetime.now(), TipoTransaccion.DEPOSITO, Decimal("10.00"))
 
 
def test_historial_vacio_es_valido() -> None:

    """
        Prueba que la función `es_historial_cuenta_valido` considere como válido
        un historial que se encuentra completamente vacío (lista vacía).

        Returns:
            None

        Examples:
            >>> # test_historial_vacio_es_valido()
    """

    assert es_historial_cuenta_valido([]) is True
 
 
def test_historial_con_transacciones_validas() -> None:

    """
        Prueba que la función `es_historial_cuenta_valido` retorne True cuando el historial
        contiene una lista de tuplas bien formadas con fecha, tipo de transacción y monto decimal.

        Returns:
            None

        Examples:
            >>> # test_historial_con_transacciones_validas()
    """

    assert es_historial_cuenta_valido([_transaccion(), _transaccion()]) is True
 
 
@pytest.mark.parametrize("historial", [
    None,                                   # no es lista
    (),                                     # tupla en vez de lista
    "historial",                            # string
    [None],                                 # elemento que no es tupla
    [(datetime.now(), TipoTransaccion.DEPOSITO)],  # tupla de 2 elementos
    [("hoy", TipoTransaccion.DEPOSITO, Decimal("10.00"))],       # fecha no datetime
    [(datetime.now(), "deposito", Decimal("10.00"))],            # tipo no enum
    [(datetime.now(), TipoTransaccion.DEPOSITO, 10.0)],          # monto float
    [(datetime.now(), TipoTransaccion.DEPOSITO, Decimal("1")), "basura"],  # uno bueno y uno malo
])
def test_historial_invalido(historial) -> None:

    """
        Prueba que la función `es_historial_cuenta_valido` retorne False si el historial
        no es una lista o si alguno de sus elementos internos incumple la estructura
        esperada o los tipos de datos de sus campos.

        Args:
            historial (Any): Estructura candidata inválida para el historial de transacciones.

        Returns:
            None

        Examples:
            >>> # test_historial_invalido(None)
    """

    assert es_historial_cuenta_valido(historial) is False
 
 
#Cliente: nombre y DNI--------------------------------------------
 
@pytest.mark.parametrize("nombre", ["Ana", " Ana ", "Juan Perez"])
def test_nombre_valido(nombre) -> None:

    """
        Prueba que la función `es_nombre_cliente_valido` retorne True cuando se le pasa
        una cadena de texto con un nombre de cliente válido (con o sin espacios periféricos).

        Args:
            nombre (str): Cadena de texto que representa un nombre de cliente válido.

        Returns:
            None

        Examples:
            >>> # test_nombre_valido("Ana")
    """

    assert es_nombre_cliente_valido(nombre) is True
 
 
@pytest.mark.parametrize("nombre", ["", "   ", None, 123])
def test_nombre_invalido(nombre) -> None:

    """
        Prueba que la función `es_nombre_cliente_valido` retorne False ante cadenas vacías,
        espacios en blanco, valores nulos o tipos de datos no correspondientes a cadenas.

        Args:
            nombre (Any): Valor candidato inválido para el nombre del cliente.

        Returns:
            None

        Examples:
            >>> # test_nombre_invalido("")
    """

    assert es_nombre_cliente_valido(nombre) is False
 
 
@pytest.mark.parametrize("dni", ["12345678", "1234567", "12.345.678", "1.234.567", " 12345678 "])
def test_dni_valido(dni) -> None:

    """
        Prueba que la función `es_dni_cliente_valido` retorne True cuando se le pasa
        un DNI en formato de cadena con la cantidad de dígitos permitida y posibles
        separadores de puntos o espacios.

        Args:
            dni (str): Cadena con el número de DNI a validar.

        Returns:
            None

        Examples:
            >>> # test_dni_valido("12345678")
    """

    assert es_dni_cliente_valido(dni) is True
 
 
@pytest.mark.parametrize("dni", [
    "123456",       # 6 digitos
    "123456789",    # 9 digitos
    "1234567a",     # letra
    "",             # vacio
    None,           # no es str
    12345678,       # int, no str
])
def test_dni_invalido(dni) -> None:

    """
        Prueba que la función `es_dni_cliente_valido` retorne False cuando el DNI
        contiene una longitud de dígitos incorrecta, caracteres alfabéticos,
        está vacío o no es de tipo cadena.

        Args:
            dni (Any): Valor candidato inválido para el DNI.

        Returns:
            None

        Examples:
            >>> # test_dni_invalido("123456")
    """

    assert es_dni_cliente_valido(dni) is False

@pytest.mark.parametrize("nombre", [
    "", 
    "  ", 
    None, 
    123
])
def test_nombre_banco_invalido(nombre) -> None:

    """
        Prueba que la función `es_nombre_banco_valido` retorne False cuando se le pasan
        cadenas vacías, espacios en blanco, valores nulos o enteros como nombre de banco.

        Args:
            nombre (Any): Valor candidato inválido para el nombre del banco.

        Returns:
            None

        Examples:
            >>> # test_nombre_banco_invalido("")
    """
    
    assert es_nombre_banco_valido(nombre) is False