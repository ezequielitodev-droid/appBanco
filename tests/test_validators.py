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
 
#Con parametrize, un mismo test se repite por cada valor de la lista
#(pytest lo cuenta como un test por valor).
 
#Numero de cuenta-------------------------------------------------
 
@pytest.mark.parametrize("valor", ["1" * 22, "0" * 22, " " + "1" * 22 + " "])
def test_numero_cuenta_valido(valor) -> None:
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
    assert es_numero_cuenta_valido(valor, 22) is False
 
 
#Saldo------------------------------------------------------------
 
@pytest.mark.parametrize("saldo", [Decimal("0"), Decimal("0.00"), Decimal("100.50")])
def test_saldo_valido(saldo) -> None:
    assert es_saldo_cuenta_valido(saldo) is True
 
 
@pytest.mark.parametrize("saldo", [Decimal("-0.01"), 100, 100.0, "100", None])
def test_saldo_invalido(saldo) -> None:
    assert es_saldo_cuenta_valido(saldo) is False
 
 
#Monto (borde: el 0 NO es valido, a diferencia del saldo)---------
 
def test_monto_valido() -> None:
    assert es_monto_valido(Decimal("0.01")) is True
 
 
@pytest.mark.parametrize("monto", [Decimal("0"), Decimal("-5.00"), 10, 10.5, "10", None])
def test_monto_invalido(monto) -> None:
    assert es_monto_valido(monto) is False
 
 
#Descubierto (borde: el 0 SI es valido)---------------------------
 
@pytest.mark.parametrize("descubierto", [Decimal("0"), Decimal("500.00")])
def test_descubierto_valido(descubierto) -> None:
    assert es_descubierto_cuenta_valido(descubierto) is True
 
 
@pytest.mark.parametrize("descubierto", [Decimal("-1.00"), 500, 500.0, None])
def test_descubierto_invalido(descubierto) -> None:
    assert es_descubierto_cuenta_valido(descubierto) is False
 
 
#Historial--------------------------------------------------------
 
def _transaccion():
    return (datetime.now(), TipoTransaccion.DEPOSITO, Decimal("10.00"))
 
 
def test_historial_vacio_es_valido() -> None:
    assert es_historial_cuenta_valido([]) is True
 
 
def test_historial_con_transacciones_validas() -> None:
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
    assert es_historial_cuenta_valido(historial) is False
 
 
#Cliente: nombre y DNI--------------------------------------------
 
@pytest.mark.parametrize("nombre", ["Ana", " Ana ", "Juan Perez"])
def test_nombre_valido(nombre) -> None:
    assert es_nombre_cliente_valido(nombre) is True
 
 
@pytest.mark.parametrize("nombre", ["", "   ", None, 123])
def test_nombre_invalido(nombre) -> None:
    assert es_nombre_cliente_valido(nombre) is False
 
 
@pytest.mark.parametrize("dni", ["12345678", "1234567", "12.345.678", "1.234.567", " 12345678 "])
def test_dni_valido(dni) -> None:
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
    assert es_dni_cliente_valido(dni) is False

@pytest.mark.parametrize("nombre", [
    "", 
    "  ", 
    None, 
    123
])
def test_nombre_banco_invalido(nombre) -> None:
    assert es_nombre_banco_valido(nombre) is False