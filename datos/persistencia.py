#Imports:

import json
from pathlib import Path
import os
from decimal import Decimal
from datetime import datetime
from models.objects_models import Banco, Cliente, CuentaAhorro, CuentaCorriente
from utils.enums import TipoTransaccion

#Constants:

CARPETA_DATOS = Path(__file__).parent
CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
ARCHIVO_DATOS= CARPETA_DATOS / "banco_datos.json"

#Funciones:

def guardar_datos(banco: Banco) -> None:
    
    """
        Serializa y guarda el estado actual del banco en un archivo JSON local.

        Recorre la estructura de objetos del banco (clientes, cuentas y el historial
        de transacciones de cada una), convirtiendo tipos de datos complejos que
        JSON no soporta de forma nativa (como `Decimal`, `datetime` y `TipoTransaccion`)
        en tipos primitivos compatibles (cadenas de texto y formatos ISO).

        Args:
            banco (Banco): La instancia del objeto Banco que contiene todos los datos a persistir.

        Returns:
            None

        Raises:
            OSError: Si ocurre un error al intentar escribir o crear el archivo en el disco.

        Examples:
            >>> banco = Banco("Banco Central")
            >>> cliente = banco.alta_cliente("Juan Pérez", "12345678")
            >>> cuenta = CuentaAhorro("CA-001", saldo=Decimal("1500.00"))
            >>> cliente.agregar_cuenta(cuenta)
            >>> guardar_datos(banco)

        Note:
            El archivo resultante se almacena en la ruta definida por `ARCHIVO_DATOS`
            utilizando codificación UTF-8 e indentación de 4 espacios para legibilidad.
    """

    data = {
        "nombre": banco.get_nombre(),
        "clientes": []
    }

    for cliente in banco.clientes: 
        cliente_data = {
            "nombre": cliente.get_nombre(),
            "dni": cliente.get_dni(),
            "cuentas": []
        }
        for cuenta in cliente.cuentas:
            #Como que las cuentas difieran de tipo implica que tiene mas o menos datos, las identificamos...
            tipo = "ahorro" if isinstance(cuenta, CuentaAhorro) else "corriente"
            cuenta_data = {
                "tipo": tipo,
                "numero": cuenta.get_numero(),
                "saldo": str(cuenta.get_saldo()), #Decimal se guarda como string
                "historial": [
                    #Aqui en el historial hay un problema, JSON no reconoce ni los tipos DATETIME ni ENUMS asi que tengo que convertirlos...
                    (t[0].isoformat(), t[1].value, str(t[2])) for t in cuenta.get_historial()
                ]
            }
            if isinstance(cuenta, CuentaCorriente):
                cuenta_data["descubierto"] = str(cuenta.get_descubierto())

            cliente_data["cuentas"].append(cuenta_data)

        data["clientes"].append(cliente_data)

    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def cargar_datos() -> Banco:

    """
        Carga y reconstruye el estado del banco desde el archivo JSON local.

        Lee el archivo de persistencia, deserializa los datos primitivos y los
        reconvierte a sus tipos originales de dominio (instancias de `Decimal` para
        montos y saldos, objetos `datetime` para fechas, `TipoTransaccion` para los enums
        y las subclases correspondientes de cuentas y clientes).

        Returns:
            Banco: Una nueva instancia de Banco con todos sus clientes, cuentas
            y historiales completamente restaurados. Si el archivo no existe,
            retorna un objeto Banco nuevo con un nombre predeterminado ("Mi Banco").

        Raises:
            json.JSONDecodeError: Si el archivo JSON está corrupto o mal formado.
            KeyError: Si falta alguna clave obligatoria en la estructura del archivo.

        Examples:
            >>> banco_restaurado = cargar_datos()
            >>> banco_restaurado.get_nombre()
            'Banco Central'
            >>> len(banco_restaurado.clientes) > 0
            True
    """

    if not ARCHIVO_DATOS.exists():
        return Banco("Mi Banco")

    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
        data = json.load(f)

    banco = Banco(data["nombre"])

    for c_data in data["clientes"]:
        cliente = banco.alta_cliente(c_data["nombre"], c_data["dni"])

        for cue_data in c_data["cuentas"]:
            saldo = Decimal(cue_data["saldo"])

            historial_reconstruido = []
            for t_data in cue_data.get("historial", []):
                fecha = datetime.fromisoformat(t_data[0])
                tipo_transaccion = TipoTransaccion(t_data[1])
                monto = Decimal(t_data[2])
                historial_reconstruido.append((fecha, tipo_transaccion, monto))

            # Instanciamos según el tipo de cuenta
            if cue_data["tipo"] == "ahorro":
                cuenta = CuentaAhorro(cue_data["numero"], saldo=saldo, historial=historial_reconstruido)
            else:
                descubierto = Decimal(cue_data["descubierto"])
                cuenta = CuentaCorriente(
                    cue_data["numero"], 
                    saldo=saldo, 
                    historial=historial_reconstruido, 
                    descubierto=descubierto
                )
                
            cliente.agregar_cuenta(cuenta)

    return banco