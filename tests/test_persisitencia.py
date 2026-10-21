# Archivo para probar la persistencia de datos (guardar y cargar JSON):

from decimal import Decimal
import pytest

from models.objects_models import Banco, CuentaAhorro, CuentaCorriente
from utils.enums import TipoTransaccion
from datos.persistencia import guardar_datos, cargar_datos
import datos.persistencia as persistencia_mod

NUMERO_PRUEBA = "1" * 22
NUMERO_CORRIENTE = "2" * 22

def test_cargar_datos_si_no_existe_archivo(tmp_path, monkeypatch) -> None:
    # Simulamos que el archivo de datos apunta a una ruta temporal que no existe
    archivo_falso = tmp_path / "banco_inexistente.json"
    monkeypatch.setattr(persistencia_mod, "ARCHIVO_DATOS", archivo_falso)
    
    banco = cargar_datos()
    
    assert isinstance(banco, Banco)
    assert banco.get_nombre() == "Mi Banco"
    assert banco.clientes == []

def test_guardar_y_cargar_datos_banco_completo(tmp_path, monkeypatch) -> None:
    # Apuntamos la persistencia a un archivo temporal
    archivo_temp = tmp_path / "banco_datos.json"
    monkeypatch.setattr(persistencia_mod, "ARCHIVO_DATOS", archivo_temp)
    
    # 1. Creamos un banco de prueba con clientes, cuentas e historial
    banco_original = Banco("BancoPrueba")
    cliente = banco_original.alta_cliente("Elizabeth", "42246485")
    
    # Cuenta de ahorro con saldo e historial
    cuenta_ahorro = CuentaAhorro(NUMERO_PRUEBA, Decimal("1000.00"))
    cuenta_ahorro.depositar(Decimal("500.00"))
    cliente.agregar_cuenta(cuenta_ahorro)
    
    # Cuenta corriente con descubierto personalizado
    cuenta_corriente = CuentaCorriente(NUMERO_CORRIENTE, Decimal("-100.00"), descubierto=Decimal("300.00"))
    cliente.agregar_cuenta(cuenta_corriente)
    
    # 2. Guardamos los datos
    guardar_datos(banco_original)
    assert archivo_temp.exists()
    
    # 3. Cargamos los datos en una nueva instancia de banco
    banco_cargado = cargar_datos()
    
    # 4. Verificamos que se haya reconstruido todo correctamente
    assert banco_cargado.get_nombre() == "BancoPrueba"
    assert len(banco_cargado.clientes) == 1
    
    cliente_cargado = banco_cargado.clientes[0]
    assert cliente_cargado.get_nombre() == "Elizabeth"
    assert cliente_cargado.get_dni() == "42246485"
    assert len(cliente_cargado.cuentas) == 2
    
    # Verificamos cuenta de ahorro
    c_ahorro_cargada = cliente_cargado.cuentas[0]
    assert isinstance(c_ahorro_cargada, CuentaAhorro)
    assert c_ahorro_cargada.get_numero() == NUMERO_PRUEBA
    assert c_ahorro_cargada.get_saldo() == Decimal("1500.00")
    assert len(c_ahorro_cargada.get_historial()) == 1
    _, tipo_tx, monto_tx = c_ahorro_cargada.get_historial()[0]
    assert tipo_tx == TipoTransaccion.DEPOSITO
    assert monto_tx == Decimal("500.00")
    
    # Verificamos cuenta corriente
    c_corr_cargada = cliente_cargado.cuentas[1]
    assert isinstance(c_corr_cargada, CuentaCorriente)
    assert c_corr_cargada.get_numero() == NUMERO_CORRIENTE
    assert c_corr_cargada.get_saldo() == Decimal("-100.00")
    assert c_corr_cargada.get_descubierto() == Decimal("300.00")