#Archivo para probar los modelos de Cuentas:

#Imports:

from decimal import Decimal
from datetime import datetime
import pytest

from models.objects_models import Cuenta, CuentaAhorro, CuentaCorriente
from utils.enums import TipoTransaccion

#Pruebas:

NUMERO_CUENTA_PRUEBA = "1" * 22

#Pruebas de instanciacion--------------------------

def test_cuenta_abstracta_no_se_puede_instanciar() -> None:
    
    with pytest.raises(TypeError):
        Cuenta(NUMERO_CUENTA_PRUEBA) #type: ignore

def test_cuenta_ahorro_con_parametros_minimos() -> None:
    
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA)

    assert cuenta.get_numero() == NUMERO_CUENTA_PRUEBA
    assert cuenta.get_saldo() == Decimal("0.00")
    assert cuenta.get_historial() == []

def test_cuenta_corriente_con_parametros_minimos() -> None:

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA)

    assert cuenta.get_numero() == NUMERO_CUENTA_PRUEBA
    assert cuenta.get_saldo() == Decimal("0.00")
    assert cuenta.get_historial() == []
    assert cuenta.get_descubierto() == Decimal("500.00")

def test_cuenta_con_saldo_inicial() -> None:

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("250.00"))

    assert cuenta.get_saldo() == Decimal("250.00")

def test_cuenta_con_historial_inicial() -> None:

    historial = [(datetime.now(), TipoTransaccion.DEPOSITO, Decimal("10.00"))]

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, historial=historial)

    assert cuenta.get_historial() == historial

#Pruebas de instanciacion--------------------------
#Pruebas de datos invalidos------------------------

@pytest.mark.parametrize("numero", ["1" * 21, "1" * 23, "", "a" * 22, None])
def test_numero_de_cuenta_invalido_lanza_error(numero) -> None:

    with pytest.raises(ValueError, match="Numero de cuenta"):
        CuentaAhorro(numero)

@pytest.mark.parametrize("saldo", [Decimal("-1.00"), 100, 100.0, "100"])
def test_saldo_inicial_invalido_lanza_error(saldo) -> None:

    with pytest.raises(ValueError, match="Saldo"):
        CuentaAhorro(NUMERO_CUENTA_PRUEBA, saldo)

def test_historial_inicial_invalido_lanza_error() -> None:
    with pytest.raises(ValueError, match="Historia"):
        CuentaAhorro(NUMERO_CUENTA_PRUEBA, historial="no_es_una_lista") #type: ignore

#Pruebas de datos invalidos------------------------

#Pruebas de depositos------------------------------

def test_depositar_suma_al_saldo() -> None:

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA)
    cuenta.depositar(Decimal("100.00"))

    assert cuenta.get_saldo() == Decimal("100.00")
 
 
def test_depositar_varias_veces_acumula() -> None:
    
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
    cuenta.depositar(Decimal("100.00"))
    cuenta.depositar(Decimal("0.50"))

    assert cuenta.get_saldo() == Decimal("150.50")
 
 
def test_depositar_registra_la_transaccion() -> None:
    
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA)
 
    antes = datetime.now()
    cuenta.depositar(Decimal("100.00"))
    despues = datetime.now()
 
    historial = cuenta.get_historial()
    assert len(historial) == 1
 
    fecha, tipo, monto = historial[0]
    assert antes <= fecha <= despues
    assert tipo == TipoTransaccion.DEPOSITO
    assert monto == Decimal("100.00")

@pytest.mark.parametrize("monto", [Decimal("-1.00"), Decimal("0"), 1, 1.5, "1", None])
def test_depositar_monto_invalido_lanza_error(monto) -> None:

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))

    with pytest.raises(ValueError, match="Monto invalido"):
        cuenta.depositar(monto)

    #Una operacion rechazada no debe dejar rastros:
    assert cuenta.get_saldo() == Decimal("50.00")
    assert cuenta.get_historial() == []

#Pruebas de depositos------------------------------

#Extraer: CuentaAhorro--------------------------------------------
 
def test_ahorro_extraer_resta_del_saldo() -> None:
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    cuenta.extraer(Decimal("30.00"))
    assert cuenta.get_saldo() == Decimal("70.00")
 
 
def test_ahorro_extraer_todo_el_saldo_es_valido() -> None:   # borde
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    cuenta.extraer(Decimal("100.00"))
    assert cuenta.get_saldo() == Decimal("0.00")
 
 
def test_ahorro_extraer_un_centavo_de_mas_lanza_error() -> None:   # borde
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    with pytest.raises(ValueError, match="Saldo insuficiente"):
        cuenta.extraer(Decimal("100.01"))
 
 
def test_ahorro_extraer_registra_la_transaccion() -> None:
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    cuenta.extraer(Decimal("30.00"))
 
    _, tipo, monto = cuenta.get_historial()[0]
    assert tipo == TipoTransaccion.EXTRACCION
    assert monto == Decimal("30.00")

@pytest.mark.parametrize("monto", [Decimal("0"), Decimal("-10.00"), 10, 10.5, None])
def test_ahorro_extraer_monto_invalido_lanza_error(monto) -> None:
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    with pytest.raises(ValueError, match="Monto"):
        cuenta.extraer(monto)
 
 
def test_ahorro_extraccion_rechazada_no_modifica_nada() -> None:
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("50.01"))
 
    assert cuenta.get_saldo() == Decimal("50.00")
    assert cuenta.get_historial() == []

#Extraer: CuentaAhorro--------------------------------------------

#Extraer: CuentaCorriente (descubierto)---------------------------
 
def test_corriente_extraer_dentro_del_saldo() -> None:
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    cuenta.extraer(Decimal("40.00"))
    assert cuenta.get_saldo() == Decimal("60.00")
 
 
def test_corriente_extraer_hasta_el_limite_funciona() -> None:   # borde: 50 + 500 = 550
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
    cuenta.extraer(Decimal("550.00"))
    assert cuenta.get_saldo() == Decimal("-500.00")
 
 
def test_corriente_extraer_un_centavo_pasado_del_limite_lanza_error() -> None:   # borde
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
    with pytest.raises(ValueError, match="descubierto"):
        cuenta.extraer(Decimal("550.01"))

def test_corriente_el_descubierto_no_se_renueva_en_cada_extraccion() -> None:
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("1000.00"))   # descubierto 500
    cuenta.extraer(Decimal("1500.00"))   # usa todo: saldo -500
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("0.01"))   # ya no queda nada disponible
 
 
def test_corriente_depositar_libera_descubierto() -> None:
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
    cuenta.extraer(Decimal("550.00"))     # saldo -500, disponible 0
 
    cuenta.depositar(Decimal("200.00"))   # saldo -300, disponible 200
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("200.01"))
 
    cuenta.extraer(Decimal("200.00"))
    assert cuenta.get_saldo() == Decimal("-500.00")
 
 
def test_corriente_con_descubierto_cero_no_admite_negativos() -> None:
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"), descubierto=Decimal("0.00"))
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("50.01"))
 
    cuenta.extraer(Decimal("50.00"))
    assert cuenta.get_saldo() == Decimal("0.00")
 
 
@pytest.mark.parametrize("descubierto", [Decimal("-1.00"), 500, 500.0, "500"])
def test_corriente_descubierto_invalido_lanza_error(descubierto) -> None:
    with pytest.raises(ValueError, match="Descubierto"):
        CuentaCorriente(NUMERO_CUENTA_PRUEBA, descubierto=descubierto)
 
 
@pytest.mark.parametrize("monto", [Decimal("0"), Decimal("-10.00"), 10, 10.5, None])
def test_corriente_extraer_monto_invalido_lanza_error(monto) -> None:
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    with pytest.raises(ValueError, match="Monto"):
        cuenta.extraer(monto)
 
 
def test_corriente_extraccion_rechazada_no_modifica_nada() -> None:
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("550.01"))
 
    assert cuenta.get_saldo() == Decimal("50.00")
    assert cuenta.get_historial() == []
 
 
def test_corriente_extraer_registra_la_transaccion() -> None:
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA)
    cuenta.extraer(Decimal("100.00"))
 
    _, tipo, monto = cuenta.get_historial()[0]
    assert tipo == TipoTransaccion.EXTRACCION
    assert monto == Decimal("100.00")

#Extraer: CuentaCorriente (descubierto)---------------------------

#Historial con varias operaciones---------------------------------
 
def test_historial_conserva_el_orden_de_las_operaciones() -> None:
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA)
    cuenta.depositar(Decimal("100.00"))
    cuenta.extraer(Decimal("30.00"))
    cuenta.depositar(Decimal("5.00"))
 
    tipos = [tipo for _, tipo, _ in cuenta.get_historial()]
    assert tipos == [TipoTransaccion.DEPOSITO, TipoTransaccion.EXTRACCION, TipoTransaccion.DEPOSITO]

#Historial con varias operaciones---------------------------------

#__str__----------------------------------------------------------
 
def test_str_cuenta_ahorro() -> None:
    texto = str(CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("10.00")))
    assert texto.startswith("Cuenta A-")
    assert NUMERO_CUENTA_PRUEBA in texto
    assert "10.00" in texto
 
 
def test_str_cuenta_corriente() -> None:
    texto = str(CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("10.00")))
    assert texto.startswith("Cuenta C-")
    assert NUMERO_CUENTA_PRUEBA in texto
    assert "500.00" in texto

#__str__----------------------------------------------------------