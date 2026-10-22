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

    """
        Prueba que la clase base abstracta `Cuenta` no pueda ser instanciada directamente,
        lanzando un TypeError.

        Returns:
            None
    """
    
    with pytest.raises(TypeError):
        Cuenta(NUMERO_CUENTA_PRUEBA) #type: ignore

def test_cuenta_ahorro_con_parametros_minimos() -> None:

    """
        Prueba que se pueda instanciar una `CuentaAhorro` con los parámetros mínimos,
        verificando su número, saldo inicial en cero y un historial vacío.

        Returns:
            None
    """
    
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA)

    assert cuenta.get_numero() == NUMERO_CUENTA_PRUEBA
    assert cuenta.get_saldo() == Decimal("0.00")
    assert cuenta.get_historial() == []

def test_cuenta_corriente_con_parametros_minimos() -> None:

    """
        Prueba que se pueda instanciar una `CuentaCorriente` con los parámetros mínimos,
        verificando su número, saldo inicial en cero, historial vacío y límite de descubierto por defecto.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA)

    assert cuenta.get_numero() == NUMERO_CUENTA_PRUEBA
    assert cuenta.get_saldo() == Decimal("0.00")
    assert cuenta.get_historial() == []
    assert cuenta.get_descubierto() == Decimal("500.00")

def test_cuenta_con_saldo_inicial() -> None:

    """
        Prueba que se pueda instanciar una cuenta asignándole un saldo inicial válido en formato Decimal.

        Returns:
            None
    """

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("250.00"))

    assert cuenta.get_saldo() == Decimal("250.00")

def test_cuenta_con_historial_inicial() -> None:

    """
        Prueba que se pueda instanciar una cuenta cargándole un historial previo de transacciones.

        Returns:
            None
    """

    historial = [(datetime.now(), TipoTransaccion.DEPOSITO, Decimal("10.00"))]

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, historial=historial)

    assert cuenta.get_historial() == historial

#Pruebas de instanciacion--------------------------
#Pruebas de datos invalidos------------------------

@pytest.mark.parametrize("numero", ["1" * 21, "1" * 23, "", "a" * 22, None])
def test_numero_de_cuenta_invalido_lanza_error(numero) -> None:

    """
        Prueba que se lance un ValueError al intentar crear una cuenta con un número
        que no cumpla con los requisitos de longitud o formato.

        Args:
            numero: Número de cuenta inválido a evaluar.

        Returns:
            None
    """

    with pytest.raises(ValueError, match="Numero de cuenta"):
        CuentaAhorro(numero)

@pytest.mark.parametrize("saldo", [Decimal("-1.00"), 100, 100.0, "100"])
def test_saldo_inicial_invalido_lanza_error(saldo) -> None:

    """
        Prueba que se lance un ValueError al intentar instanciar una cuenta con un saldo
        inicial inválido (negativo o de un tipo distinto a Decimal).

        Args:
            saldo: Saldo inválido a evaluar.

        Returns:
            None
    """

    with pytest.raises(ValueError, match="Saldo"):
        CuentaAhorro(NUMERO_CUENTA_PRUEBA, saldo)

def test_historial_inicial_invalido_lanza_error() -> None:

    """
        Prueba que se lance un ValueError al intentar asignar un historial inicial
        que no corresponda a una estructura de lista válida.

        Returns:
            None
    """

    with pytest.raises(ValueError, match="Historia"):
        CuentaAhorro(NUMERO_CUENTA_PRUEBA, historial="no_es_una_lista") #type: ignore

#Pruebas de datos invalidos------------------------

#Pruebas de depositos------------------------------

def test_depositar_suma_al_saldo() -> None:

    """
        Prueba que realizar un depósito válido incremente correctamente el saldo de la cuenta.

        Returns:
            None
    """

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA)
    cuenta.depositar(Decimal("100.00"))

    assert cuenta.get_saldo() == Decimal("100.00")
 
 
def test_depositar_varias_veces_acumula() -> None:

    """
        Prueba que múltiples depósitos consecutivos acumulen correctamente el monto total en el saldo.

        Returns:
            None
    """
    
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
    cuenta.depositar(Decimal("100.00"))
    cuenta.depositar(Decimal("0.50"))

    assert cuenta.get_saldo() == Decimal("150.50")
 
 
def test_depositar_registra_la_transaccion() -> None:

    """
        Prueba que cada depósito exitoso registre adecuadamente la transacción en el historial
        con su marca temporal, tipo y monto correspondiente.

        Returns:
            None
    """
    
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

    """
        Prueba que se lance un ValueError al intentar depositar un monto inválido
        y que la operación rechazada no modifique el saldo ni agregue registros al historial.

        Args:
            monto: Monto inválido a depositar.

        Returns:
            None
    """

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))

    with pytest.raises(ValueError, match="Monto invalido"):
        cuenta.depositar(monto)

    #Una operacion rechazada no debe dejar rastros:
    assert cuenta.get_saldo() == Decimal("50.00")
    assert cuenta.get_historial() == []

#Pruebas de depositos------------------------------

#Extraer: CuentaAhorro--------------------------------------------
 
def test_ahorro_extraer_resta_del_saldo() -> None:

    """
        Prueba que una extracción válida en una cuenta de ahorro reste correctamente del saldo disponible.

        Returns:
            None
    """

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    cuenta.extraer(Decimal("30.00"))
    assert cuenta.get_saldo() == Decimal("70.00")
 
 
def test_ahorro_extraer_todo_el_saldo_es_valido() -> None:   # borde
    """

        Prueba que extraer la totalidad del saldo de una cuenta de ahorro sea una operación válida
        dejando el saldo exactamente en cero.

        Returns:
            None
    """
    
    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    cuenta.extraer(Decimal("100.00"))
    assert cuenta.get_saldo() == Decimal("0.00")
 
 
def test_ahorro_extraer_un_centavo_de_mas_lanza_error() -> None:   # borde
    
    """
        Prueba que se lance un ValueError por saldo insuficiente al intentar extraer
        un centavo más del saldo disponible en una cuenta de ahorro.

        Returns:
            None
    """

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    with pytest.raises(ValueError, match="Saldo insuficiente"):
        cuenta.extraer(Decimal("100.01"))
 
 
def test_ahorro_extraer_registra_la_transaccion() -> None:

    """
        Prueba que una extracción exitosa en cuenta de ahorro registre correctamente
        la transacción de tipo extracción en el historial.

        Returns:
            None
    """

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    cuenta.extraer(Decimal("30.00"))
 
    _, tipo, monto = cuenta.get_historial()[0]
    assert tipo == TipoTransaccion.EXTRACCION
    assert monto == Decimal("30.00")

@pytest.mark.parametrize("monto", [Decimal("0"), Decimal("-10.00"), 10, 10.5, None])
def test_ahorro_extraer_monto_invalido_lanza_error(monto) -> None:

    """
        Prueba que se lance un ValueError al intentar extraer montos inválidos en una cuenta de ahorro.

        Args:
            monto: Monto inválido a extraer.

        Returns:
            None
    """

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    with pytest.raises(ValueError, match="Monto"):
        cuenta.extraer(monto)
 
 
def test_ahorro_extraccion_rechazada_no_modifica_nada() -> None:

    """
        Prueba que una extracción rechazada en cuenta de ahorro no altere el saldo
        ni genere registros en el historial de transacciones.

        Returns:
            None
    """

    cuenta = CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("50.01"))
 
    assert cuenta.get_saldo() == Decimal("50.00")
    assert cuenta.get_historial() == []

#Extraer: CuentaAhorro--------------------------------------------

#Extraer: CuentaCorriente (descubierto)---------------------------
 
def test_corriente_extraer_dentro_del_saldo() -> None:

    """
        Prueba que una extracción dentro del saldo positivo en una cuenta corriente
        reduzca correctamente el monto disponible.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    cuenta.extraer(Decimal("40.00"))
    assert cuenta.get_saldo() == Decimal("60.00")
 
 
def test_corriente_extraer_hasta_el_limite_funciona() -> None:   # borde: 50 + 500 = 550

    """
        Prueba que se pueda extraer hasta el límite exacto del saldo más el descubierto permitido
        en una cuenta corriente, dejando el saldo en negativo.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
    cuenta.extraer(Decimal("550.00"))
    assert cuenta.get_saldo() == Decimal("-500.00")
 
 
def test_corriente_extraer_un_centavo_pasado_del_limite_lanza_error() -> None:   # borde
   
    """
        Prueba que se lance un ValueError por superar el descubierto al intentar extraer
        un centavo por encima del límite permitido en una cuenta corriente.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
    with pytest.raises(ValueError, match="descubierto"):
        cuenta.extraer(Decimal("550.01"))

def test_corriente_el_descubierto_no_se_renueva_en_cada_extraccion() -> None:

    """
        Prueba que el límite de descubierto en una cuenta corriente no se renueve
        con cada extracción parcial, agotándose de forma acumulativa.

        Returns:
            None
    """
    
    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("1000.00"))   # descubierto 500
    cuenta.extraer(Decimal("1500.00"))   # usa todo: saldo -500
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("0.01"))   # ya no queda nada disponible
 
 
def test_corriente_depositar_libera_descubierto() -> None:

    """
        Prueba que realizar un depósito en una cuenta corriente con saldo negativo
        libere proporcionalmente el descubierto disponible.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
    cuenta.extraer(Decimal("550.00"))     # saldo -500, disponible 0
 
    cuenta.depositar(Decimal("200.00"))   # saldo -300, disponible 200
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("200.01"))
 
    cuenta.extraer(Decimal("200.00"))
    assert cuenta.get_saldo() == Decimal("-500.00")
 
 
def test_corriente_con_descubierto_cero_no_admite_negativos() -> None:

    """
        Prueba que una cuenta corriente configurada con descubierto en cero no permita
        alcanzar saldos negativos bajo ninguna circunstancia.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"), descubierto=Decimal("0.00"))
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("50.01"))
 
    cuenta.extraer(Decimal("50.00"))
    assert cuenta.get_saldo() == Decimal("0.00")
 
 
@pytest.mark.parametrize("descubierto", [Decimal("-1.00"), 500, 500.0, "500"])
def test_corriente_descubierto_invalido_lanza_error(descubierto) -> None:

    """
        Prueba que se lance un ValueError al intentar instanciar una cuenta corriente
        con un límite de descubierto inválido.

        Args:
            descubierto: Límite de descubierto inválido a evaluar.

        Returns:
            None
    """

    with pytest.raises(ValueError, match="Descubierto"):
        CuentaCorriente(NUMERO_CUENTA_PRUEBA, descubierto=descubierto)
 
 
@pytest.mark.parametrize("monto", [Decimal("0"), Decimal("-10.00"), 10, 10.5, None])
def test_corriente_extraer_monto_invalido_lanza_error(monto) -> None:

    """
        Prueba que se lance un ValueError al intentar extraer montos inválidos en una cuenta corriente.

        Args:
            monto: Monto inválido a extraer.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("100.00"))
    with pytest.raises(ValueError, match="Monto"):
        cuenta.extraer(monto)
 
 
def test_corriente_extraccion_rechazada_no_modifica_nada() -> None:

    """
        Prueba que una extracción rechazada en cuenta corriente por exceder el descubierto
        mantenga intacto el saldo y el historial de transacciones.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("50.00"))
 
    with pytest.raises(ValueError):
        cuenta.extraer(Decimal("550.01"))
 
    assert cuenta.get_saldo() == Decimal("50.00")
    assert cuenta.get_historial() == []
 
 
def test_corriente_extraer_registra_la_transaccion() -> None:

    """
        Prueba que una extracción exitosa en cuenta corriente registre correctamente
        la operación de tipo extracción en el historial.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA)
    cuenta.extraer(Decimal("100.00"))
 
    _, tipo, monto = cuenta.get_historial()[0]
    assert tipo == TipoTransaccion.EXTRACCION
    assert monto == Decimal("100.00")

#Extraer: CuentaCorriente (descubierto)---------------------------

#Historial con varias operaciones---------------------------------
 
def test_historial_conserva_el_orden_de_las_operaciones() -> None:

    """
        Prueba que el historial de transacciones conserve estrictamente el orden cronológico
        en que se ejecutaron las operaciones de depósito y extracción.

        Returns:
            None
    """

    cuenta = CuentaCorriente(NUMERO_CUENTA_PRUEBA)
    cuenta.depositar(Decimal("100.00"))
    cuenta.extraer(Decimal("30.00"))
    cuenta.depositar(Decimal("5.00"))
 
    tipos = [tipo for _, tipo, _ in cuenta.get_historial()]
    assert tipos == [TipoTransaccion.DEPOSITO, TipoTransaccion.EXTRACCION, TipoTransaccion.DEPOSITO]

#Historial con varias operaciones---------------------------------

#__str__----------------------------------------------------------
 
def test_str_cuenta_ahorro() -> None:

    """
        Prueba que la representación en cadena (`__str__`) de una cuenta de ahorro
        incluya el prefijo correspondiente, el número de cuenta y el saldo actual.

        Returns:
            None
    """

    texto = str(CuentaAhorro(NUMERO_CUENTA_PRUEBA, Decimal("10.00")))
    assert texto.startswith("Cuenta A-")
    assert NUMERO_CUENTA_PRUEBA in texto
    assert "10.00" in texto
 
 
def test_str_cuenta_corriente() -> None:

    """
        Prueba que la representación en cadena (`__str__`) de una cuenta corriente
        incluya el prefijo correspondiente, el número de cuenta y la información de descubierto.

        Returns:
            None
    """
    
    texto = str(CuentaCorriente(NUMERO_CUENTA_PRUEBA, Decimal("10.00")))
    assert texto.startswith("Cuenta C-")
    assert NUMERO_CUENTA_PRUEBA in texto
    assert "500.00" in texto

#__str__----------------------------------------------------------