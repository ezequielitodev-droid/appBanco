#Archivo para probar los modelos de Clientes:

#Imports:

from decimal import Decimal
import pytest

from models.objects_models import Cliente, CuentaAhorro, CuentaCorriente

NUMERO_A = "1" * 22
NUMERO_B = "2" * 22

#Pruebas de instanciacion------------------------------

def test_cliente_con_parametros_minimos() -> None:

    """
        Prueba que se pueda instanciar un cliente con los parámetros mínimos obligatorios,
        verificando la asignación correcta del nombre, DNI y una lista de cuentas vacía.

        Returns:
            None
    """

    cliente = Cliente("Elizabeth", "42246485")

    assert cliente.get_nombre() == "Elizabeth"
    assert cliente.get_dni() == "42246485"
    assert cliente.cuentas == []

def test_cliente_guarda_nombre_y_dni_normalizados() -> None:

    """
        Prueba que el cliente normalice y limpie correctamente los espacios en blanco
        y caracteres adicionales al recibir el nombre y el DNI.

        Returns:
            None
    """

    cliente = Cliente("  Ana Perez  ", " 12.345.678 ")
 
    assert cliente.get_nombre() == "Ana Perez"
    assert cliente.get_dni() == "12345678"

@pytest.mark.parametrize("nombre", ["", "   ", None, 123])
def test_cliente_nombre_invalido_lanza_error(nombre) -> None:

    """
        Prueba que se lance un ValueError al intentar instanciar un cliente con un nombre inválido.

        Args:
            nombre: Valor inválido a evaluar como nombre del cliente.

        Returns:
            None
    """

    with pytest.raises(ValueError, match="Nombre"):
        Cliente(nombre, "12345678")
 
 
@pytest.mark.parametrize("dni", ["123456", "123456789", "1234567a", "", None, 12345678])
def test_cliente_dni_invalido_lanza_error(dni) -> None:

    """
        Prueba que se lance un ValueError al intentar instanciar un cliente con un DNI inválido.

        Args:
            dni: Valor inválido a evaluar como DNI del cliente.

        Returns:
            None
    """

    with pytest.raises(ValueError, match="DNI"):
        Cliente("Ana", dni)

def test_cliente_con_cuentas_asociadas() -> None:

    """
        Prueba que se pueda instanciar un cliente asociándole una lista inicial de cuentas válidas.

        Returns:
            None
    """

    cuenta_a, cuenta_b = CuentaAhorro(NUMERO_A), CuentaCorriente(NUMERO_B)

    cliente = Cliente("Elizabeth", "42246485", [cuenta_a, cuenta_b])

    assert cliente.cuentas == [cuenta_a, cuenta_b]

@pytest.mark.parametrize("cuentas", [
    ["no soy una cuenta"],                # elemento que no es Cuenta
    [CuentaAhorro(NUMERO_A), None],       # uno bueno y uno malo
    (CuentaAhorro(NUMERO_A),),            # tupla en vez de lista
    "cuentas",                            # string
])
def test_cliente_lista_de_cuentas_invalida_lanza_error(cuentas) -> None:

    """
        Prueba que se lance un ValueError al intentar instanciar un cliente con una lista
        de cuentas que posea un formato o elementos inválidos.

        Args:
            cuentas: Estructura o elementos inválidos simulando la lista de cuentas.

        Returns:
            None
    """

    with pytest.raises(ValueError, match="Lista de cuentas"):
        Cliente("Ana", "12345678", cuentas)

#Pruebas de instanciacion------------------------------

#Pruebas sobre los metodos-----------------------------

@pytest.mark.parametrize("nombre", [
    "Apolos Costilla", 
    "Elizabeth Costilla", 
    "  Apolos Costilla ",
])
def test_set_cambia_nombre_y_limpia_espacios(nombre) -> None:

    """
        Prueba que el método `set_nombre` actualice correctamente el nombre del cliente
        aplicando la limpieza de espacios en blanco.

        Args:
            nombre: Nombre a establecer en el cliente.

        Returns:
            None
    """

    cliente = Cliente("Elizabeth", "42246485")
    
    cliente.set_nombre(nombre)
    
    assert cliente.get_nombre() == nombre.strip()

@pytest.mark.parametrize("nombre", ["", "   ", None, 123])
def test_set_nombre_invalido_lanza_error_y_conserva_el_anterior(nombre) -> None:

    """
        Prueba que se lance un ValueError al intentar establecer un nombre inválido
        mediante `set_nombre`, asegurando que el nombre previo del cliente no se modifique.

        Args:
            nombre: Nombre inválido a evaluar.

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678")
 
    with pytest.raises(ValueError, match="Nombre"):
        cliente.set_nombre(nombre)
 
    assert cliente.get_nombre() == "Ana"

def test_agregar_cuenta() -> None:

    """
        Prueba que se pueda agregar una cuenta de manera exitosa a la lista de cuentas del cliente.

        Returns:
            None
    """

    cuenta_a = CuentaCorriente(NUMERO_A)

    cliente = Cliente("Elizabeth", "42246485")

    cliente.agregar_cuenta(cuenta_a)

    assert cliente.cuentas == [cuenta_a]

def test_agregar_varias_cuentas_distintas() -> None:

    """
        Prueba que se puedan agregar múltiples cuentas de diferentes tipos a un mismo cliente.

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678")
    cliente.agregar_cuenta(CuentaAhorro(NUMERO_A))
    cliente.agregar_cuenta(CuentaCorriente(NUMERO_B))
 
    assert len(cliente.cuentas) == 2

@pytest.mark.parametrize("cuenta", [
    "no soy una cuenta", 
    None, 
    123, 
    Decimal("10.00")
])
def test_agregar_algo_que_no_es_cuenta_lanza_error(cuenta) -> None:

    """
        Prueba que se lance un ValueError al intentar agregar un objeto que no sea una instancia
        de Cuenta a la cartera del cliente.

        Args:
            cuenta: Objeto inválido a agregar como cuenta.

        Returns:
            None
    """

    cliente = Cliente("Elizabeth", "42246485")

    with pytest.raises(ValueError, match="Cuenta invalida..."):
        cliente.agregar_cuenta(cuenta)

    assert cliente.cuentas == []

def test_agregar_cuenta_con_numero_repetido_lanza_error() -> None:

    """
        Prueba que se lance un ValueError al intentar agregar una cuenta cuyo número
        ya pertenezca al cliente.

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678", [CuentaAhorro(NUMERO_A)])
 
    with pytest.raises(ValueError, match="ya pertenece"):
        cliente.agregar_cuenta(CuentaAhorro(NUMERO_A))
 
    assert len(cliente.cuentas) == 1
 
 
def test_agregar_cuenta_de_otro_tipo_con_numero_repetido_lanza_error() -> None:

    """
        Prueba que se lance un ValueError al intentar agregar una cuenta de distinto tipo
        pero que comparta un número de cuenta ya existente en el cliente.

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678", [CuentaAhorro(NUMERO_A)])
 
    with pytest.raises(ValueError):
        cliente.agregar_cuenta(CuentaCorriente(NUMERO_A))

def test_total_sin_cuentas_es_cero_y_es_decimal() -> None:

    """
        Prueba que el cálculo del total de capital de un cliente sin cuentas devuelva
        cero en formato Decimal.

        Returns:
            None
    """

    total = Cliente("Ana", "12345678").total()
 
    assert total == Decimal("0.00")
    assert isinstance(total, Decimal)   # no un int 0 (por eso sum arranca en Decimal)
 
 
def test_total_suma_los_saldos() -> None:

    """
        Prueba que el método `total` sume correctamente los saldos de todas las cuentas asociadas al cliente.

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678")
    cliente.agregar_cuenta(CuentaAhorro(NUMERO_A, Decimal("100.00")))
    cliente.agregar_cuenta(CuentaCorriente(NUMERO_B, Decimal("50.25")))
 
    assert cliente.total() == Decimal("150.25")
 
 
def test_total_incluye_saldos_negativos_de_cuenta_corriente() -> None:

    """
        Prueba que el método `total` incluya y procese correctamente los saldos negativos
        producto de descubiertos en cuentas corrientes.

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678")
    cliente.agregar_cuenta(CuentaAhorro(NUMERO_A, Decimal("100.00")))
    cuenta_corriente = CuentaCorriente(NUMERO_B, Decimal("50.00"))
    cliente.agregar_cuenta(cuenta_corriente)
 
    cuenta_corriente.extraer(Decimal("120.00"))   # su saldo queda en -70
 
    assert cliente.total() == Decimal("30.00")   # 100 + (-70)

def test_listar_cuentas_con_tipo() -> None:

    """
        Prueba que el método `listar_cuentas_con_tipo` devuelva una tupla con las cuentas
        y un booleano identificador del tipo de cuenta correspondiente.

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678")
    ahorro = CuentaAhorro(NUMERO_A)
    corriente = CuentaCorriente(NUMERO_B)
    cliente.agregar_cuenta(ahorro)
    cliente.agregar_cuenta(corriente)
    
    resultado = cliente.listar_cuentas_con_tipo()
    assert resultado == [(ahorro, True), (corriente, False)]

def test_depositar_en_cuenta_existente_y_no_existente() -> None:

    """
        Prueba la funcionalidad de depósito en cuentas del cliente para ambos escenarios:
        cuenta existente (éxito) y cuenta inexistente (lanza error).

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678")
    ahorro = CuentaAhorro(NUMERO_A, Decimal("100.00"))
    cliente.agregar_cuenta(ahorro)
    
    # Caso exitoso
    cliente.depositar_en_cuenta(NUMERO_A, Decimal("50.00"))
    assert ahorro.get_saldo() == Decimal("150.00")
    
    # Caso no encontrada
    with pytest.raises(ValueError, match="No se encontró una cuenta"):
        cliente.depositar_en_cuenta("9" * 22, Decimal("10.00"))


def test_extraer_de_cuenta_existente_y_no_existente() -> None:

    """
        Prueba la funcionalidad de extracción en cuentas del cliente para ambos escenarios:
        cuenta existente (éxito) y cuenta inexistente (lanza error).

        Returns:
            None
    """

    cliente = Cliente("Ana", "12345678")
    ahorro = CuentaAhorro(NUMERO_A, Decimal("100.00"))
    cliente.agregar_cuenta(ahorro)
    
    # Caso exitoso
    cliente.extraer_de_cuenta(NUMERO_A, Decimal("40.00"))
    assert ahorro.get_saldo() == Decimal("60.00")
    
    # Caso no encontrada
    with pytest.raises(ValueError, match="No se encontró una cuenta"):
        cliente.extraer_de_cuenta("9" * 22, Decimal("10.00"))

#Pruebas sobre los metodos-----------------------------