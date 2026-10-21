#Archivo para la prueba del modelo de Banco:

from decimal import Decimal

import pytest

from models.objects_models import Banco, Cliente, CuentaAhorro

NUMERO_A = "1" * 22

"""
CASOS A PROBAR - CLASE BANCO:

1. Constructor y Validaciones (__init__):
   - [ ] Instanciar un banco con nombre válido. @
   - [ ] Lanzar ValueError si el nombre del banco es inválido (según validador). @

2. Encapsulamiento:
   - [ ] Probar que la propiedad .clientes devuelve una COPIA de la lista (para que alterar la lista devuelta no rompa el banco internamente). @

3. Método alta_cliente():
   - [ ] Dar de alta un cliente con datos válidos (debe agregarse a la lista interna y devolver el objeto Cliente creado). @
   - [ ] Validar que si le pasas un nombre o DNI inválido al dar el alta, el propio objeto Cliente (o el validador) lance el error correspondiente. @

4. Método resumen():
   - [ ] (Opcional/Avanzado) Verificar que se ejecute sin lanzar excepciones (a veces se usa `capsys` de pytest para capturar el print y revisar que imprima los datos del banco). POR AHORA TOTALMENTE INNECESARIO...
"""

#Pruebas:

#1. Constructor y Validaciones (__init__)--------------------------

def test_instanciar_banco_nombre_valido() -> None:

    banco = Banco("Galicia")
    
    assert banco.get_nombre() == "Galicia"

@pytest.mark.parametrize("nombre", [
    "", 
    "     ", 
    None, 
    123
])
def test_instanciar_banco_nombre_invalido(nombre) -> None:
    
    with pytest.raises(ValueError, match="Nombre banco invalido..."):
        Banco(nombre)
        

# - [] test_es_nombre_valido() esta en test_validators.py

#1. Constructor y Validaciones (__init__)--------------------------

#2. Encapsulamiento--------------------------------------

"""def test_property_clientes_devuelve_copia() -> None:

    banco = Banco("Galicia")
    
    clientes_externos = banco.clientes #Esto deberia tener una lista vacia ([])...

    clientes_externos.append("Cliente Falso")

    assert len(banco.clientes) == 0"""

#2. Encapsulamiento--------------------------------------

#3. Metodo alta cliente----------------------------------

def test_dar_alta_cliente_valido_retornando_el_cliente() -> None:

    banco = Banco("Galicia")

    cliente = banco.alta_cliente("Elizabeth", "42246485")

    assert isinstance(cliente, Cliente) is True
    assert cliente.get_nombre() == "Elizabeth"
    assert cliente.get_dni() == "42246485"
    assert len(banco.clientes) == 1

def test_dar_alta_cliente_con_nombre_invalido() -> None:

    banco = Banco("Galicia")

    with pytest.raises(ValueError):
        banco.alta_cliente("", "44802136")

    assert len(banco.clientes) == 0

def test_dat_alta_cliente_con_dni_invalido() -> None:

    banco = Banco("Galicia")

    with pytest.raises(ValueError):
        banco.alta_cliente("Elizabeth", "")

    assert len(banco.clientes) == 0

def test_dar_alta_cliente_con_dni_ya_registrado() -> None:

    banco = Banco("Galicia")

    banco.alta_cliente("Elizabeth", "42246485")

    with pytest.raises(ValueError):
        banco.alta_cliente("Bruno", "42246485")

    assert len(banco.clientes) == 1

def test_buscar_cliente_por_dni() -> None:
    banco = Banco("Galicia")
    
    # Buscar en banco vacío (cubre cuando self.clientes está vacío)
    assert banco.buscar_cliente_por_dni("12345678") is None
    
    cliente = banco.alta_cliente("Ana", "12345678")
    
    # Buscar cliente existente
    assert banco.buscar_cliente_por_dni("12345678") == cliente
    
    # Buscar cliente inexistente (reorre la lista pero no lo encuentra)
    assert banco.buscar_cliente_por_dni("87654321") is None


def test_resumen_banco(capsys) -> None:
    banco = Banco("Galicia")
    banco.alta_cliente("Ana", "12345678")
    
    # Ejecuta el procedimiento resumen imprimiendo por terminal
    banco.resumen()
    
    captured = capsys.readouterr()
    assert "Galicia" in captured.out
    assert "Ana" in captured.out

def test_resumen_banco_con_cuentas(capsys) -> None:
    banco = Banco("Galicia")
    cliente = banco.alta_cliente("Ana", "12345678")
    cliente.agregar_cuenta(CuentaAhorro(NUMERO_A))  # <-- Esto hace que entre al bucle de la línea 379
    
    banco.resumen()
    
    captured = capsys.readouterr()
    assert "Cuenta A-" in captured.out

#3. Metodo alta cliente----------------------------------