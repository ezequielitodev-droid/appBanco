#Imports: 

from datetime import datetime
from decimal import Decimal

from utils.enums import TipoTransaccion

#Validators: 

#Cuentas Bancarias-------------------------

def es_numero_cuenta_valido(valor: str, largo: int) -> bool:

    """
    Verifica que un número de cuenta tenga un formato válido.

    Se considera válido si es un string compuesto únicamente por dígitos
    y su longitud coincide con la indicada. Los espacios al inicio y al
    final se ignoran.

    Args:
        valor (str): Número de cuenta a validar.
        largo (int): Cantidad exacta de dígitos que debe tener.

    Returns:
        bool: True si el número es válido, False en caso contrario
        (incluye el caso en que `valor` no sea un str).
    """

    if not isinstance(valor, str): return False

    valor = valor.strip()

    return valor.isdigit() and len(valor) == largo

def es_saldo_cuenta_valido(saldo: Decimal, cuenta) -> bool:

    """
    Verifica que un saldo de cuenta sea válido.

    Se considera válido si es una instancia de Decimal y su valor
    es mayor o igual a cero.

    Args:
        saldo (Decimal): Saldo a validar.

    Returns:
        bool: True si el saldo es un Decimal no negativo, False en caso
        contrario.
    """

    #MODIFICO ESTA FUNCION PORQUE NO TENIA CONTEMPLADO ANTES EL DESCUBIERTO, EL CUAL AHORA SI...

    #return isinstance(saldo, Decimal) and saldo >= 0

    from models.objects_models import CuentaCorriente

    if isinstance(cuenta, CuentaCorriente): return isinstance(saldo, Decimal) and saldo >= -500
    else: return isinstance(saldo, Decimal) and saldo >= 0

def es_historial_cuenta_valido(lista_historial: list[tuple[datetime, TipoTransaccion, Decimal]]) -> bool:

    """
    Verifica que el historial de transacciones de una cuenta sea válido.

    El historial debe ser una lista donde cada elemento es una tupla de
    tres valores: (fecha, tipo de transacción, monto). Una lista vacía
    es válida.

    Args:
        lista_historial (list[tuple[datetime, TipoTransaccion, Decimal]]):
            Lista de transacciones, donde cada tupla contiene:
            - datetime: fecha y hora de la transacción.
            - TipoTransaccion: tipo de la transacción.
            - Decimal: monto de la transacción.

    Returns:
        bool: True si la lista y todos sus elementos cumplen con la
        estructura y los tipos esperados, False en caso contrario.
    """

    if not isinstance(lista_historial, list): return False #Validacion de la lista...

    for item in lista_historial:

        if not isinstance(item, tuple) or len(item) != 3:
            return False

        fecha, tipo, monto = item

        if not isinstance(fecha, datetime): return False
        if not isinstance(tipo, TipoTransaccion): return False
        if not isinstance(monto, Decimal): return False

    return True

def es_descubierto_cuenta_valido(descubierto: Decimal) -> bool: 

    """
    Verifica que el descubierto de una cuenta corriente sea válido.

    Se considera válido si es una instancia de Decimal y su valor
    es mayor o igual a cero (un descubierto de 0 significa que la
    cuenta no admite saldo negativo).

    Args:
        descubierto (Decimal): Monto máximo de descubierto a validar.

    Returns:
        bool: True si el descubierto es un Decimal no negativo, False
        en caso contrario.
    """


    return isinstance(descubierto, Decimal) and descubierto >= 0 and descubierto <= 500

#Cuentas Bancarias-------------------------

#Saldos------------------------------------

def es_monto_valido(monto: Decimal) -> bool:

    """
    Verifica que el monto de una transacción sea válido.

    Se considera válido si es una instancia de Decimal y su valor
    es estrictamente mayor a cero. A diferencia del saldo, un monto
    de 0 no es válido, ya que no representa una operación real.

    Args:
        monto (Decimal): Monto a depositar o extraer.

    Returns:
        bool: True si el monto es un Decimal mayor a cero, False en
        caso contrario.
    """

    return isinstance(monto, Decimal) and monto > 0

#Saldos------------------------------------

#Clientes----------------------------------

def es_nombre_cliente_valido(nombre: str) -> bool:

    """
    Verifica que el nombre de un cliente sea válido.

    Se considera válido si es un string que contiene al menos un
    carácter distinto de espacio. Los espacios al inicio y al final
    se ignoran.

    Args:
        nombre (str): Nombre del cliente a validar.

    Returns:
        bool: True si el nombre es un str no vacío, False en caso
        contrario (incluye el caso en que `nombre` no sea un str).
    """

    return isinstance(nombre, str) and len(nombre.strip()) > 0

def es_dni_cliente_valido(dni: str) -> bool:

    """
    Verifica que el DNI de un cliente tenga un formato válido.

    Se considera válido si es un string compuesto únicamente por
    dígitos, con 7 u 8 de largo. Los espacios al inicio y al final,
    y los puntos separadores (por ejemplo "12.345.678"), se ignoran
    al validar.

    Args:
        dni (str): DNI a validar, con o sin puntos.

    Returns:
        bool: True si el DNI cumple el formato, False en caso
        contrario (incluye el caso en que `dni` no sea un str).
    """

    if not isinstance(dni, str): return False

    dni = dni.strip().replace(".", "")

    return dni.isdigit() and len(dni) in (7, 8)

#Clientes----------------------------------

#Bancos------------------------------------

def es_nombre_banco_valido(nombre: str) -> bool:

    return isinstance(nombre, str) and len(nombre.strip()) > 0

#Bancos------------------------------------