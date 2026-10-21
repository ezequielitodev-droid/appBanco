#Imports: 

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import override
import logging

from utils.enums import TipoTransaccion
from utils.valitators import (
    es_historial_cuenta_valido,
    es_numero_cuenta_valido,
    es_saldo_cuenta_valido, 
    es_monto_valido, 
    es_descubierto_cuenta_valido, 
    es_nombre_cliente_valido, 
    es_dni_cliente_valido, 
    es_nombre_banco_valido
)

#Creacion de microfono:

logger = logging.getLogger(__name__)

#Types:

type Transaccion = tuple[datetime, TipoTransaccion, Decimal]
type Historial = list[Transaccion]

#Constans:  

DESCUBIERTO_POR_DEFECTO = Decimal("500.00")

#Class: 

#Cuentas-------------------------------

class Cuenta(ABC):

    #Constructor: 

    def __init__(
            self, 
            numero: str, 
            saldo: Decimal | None = None, 
            historial: Historial | None = None
        ) -> None:

        if not es_numero_cuenta_valido(numero, 22): #Un numero de cuenta siempre tendra 22 digitos.
            raise ValueError("Numero de cuenta invalido...")
        self._numero: str = numero

        if saldo is not None:
            if not es_saldo_cuenta_valido(saldo, self): #Validacion
                raise ValueError("Saldo de cuenta invalido...")
            self._saldo: Decimal = saldo
        else: self._saldo = Decimal("0.00")

        if historial is not None: 
            if not es_historial_cuenta_valido(historial):
                raise ValueError("Historia de cuenta invalido...")
            self._historial = historial
        else: self._historial = []

    #Methods: 

    #Getters:-------------------

    def get_numero(self) -> str:

        return self._numero

    def get_saldo(self) -> Decimal:

        return self._saldo

    def get_historial(self) -> Historial:

        return self._historial.copy()

    #Getters:-------------------

    def _registrar_historial(self, tipo_transaccion: TipoTransaccion, monto: Decimal) -> None:
        self._historial.append((datetime.now(), tipo_transaccion, monto))

    def depositar(self, monto: Decimal) -> None:

        if not es_monto_valido(monto):
            logger.error(f"Intento de deposito fallido [Monto Invalido]: {monto}")
            raise ValueError("Monto invalido...")

        self._saldo = self._saldo + monto
        self._registrar_historial(TipoTransaccion.DEPOSITO, monto)

        logger.info(f"Deposito exitoso de [${monto}] en (ID_Cuenta[{self._numero}]): (Nuevo saldo[{self._saldo}])")

    @abstractmethod

    def extraer(self, monto: Decimal) -> None: pass #pragma: no cover

    #Strs:

    @abstractmethod

    def __str__(self) -> str: pass #pragma: no cover

class CuentaAhorro(Cuenta): 

    #Constructor:

    def __init__(
            self, 
            numero: str, 
            saldo: Decimal | None = None, 
            historial: Historial | None = None
    ) -> None:
        
        super().__init__(numero, saldo, historial)

    @override

    def extraer(self, monto: Decimal) -> None:

        if not es_monto_valido(monto):
            logger.error(f"Intento de extraccion fallido [Monto Invalido]: {monto}")
            raise ValueError("Monto invalido...")

        if monto > self._saldo:
            logger.error(f"Intento de extraccion fallido [Saldo Insuficiente]: (Monto[{monto}]), (Saldo[{self._saldo}])")
            raise ValueError("Saldo insuficiente...")

        self._saldo = self._saldo - monto
        self._registrar_historial(TipoTransaccion.EXTRACCION, monto)

        logger.info(f"Extraccion exitosa de [${monto}] en (ID_Cuenta[{self._numero}]): (Nuevo Saldo[{self._saldo}])")

    @override
    
    def __str__(self) -> str:

        return f"Cuenta A-{self._numero} | Saldo:${self._saldo}"

class CuentaCorriente(Cuenta):

    #Constructor: 

    def __init__(
        self,
        numero: str,
        saldo: Decimal | None = None,
        historial: Historial | None = None,
        descubierto: Decimal | None = None
    ) -> None:
        
        super().__init__(numero, saldo, historial)

        if descubierto is not None:
            if not es_descubierto_cuenta_valido(descubierto): 
                raise ValueError("Descubierto invalido...")
            self._descubierto = descubierto
        else: self._descubierto = DESCUBIERTO_POR_DEFECTO

    #Getters:

    def get_descubierto(self) -> Decimal:

        return self._descubierto

    @override

    def extraer(self, monto: Decimal) -> None:

        if not es_monto_valido(monto): 
            logger.error(f"Intento de extraccion fallido [Monto Invalido]: {monto}")
            raise ValueError("Monto invalido...")

        if monto > self._saldo + self._descubierto:
            logger.error(f"Intento de extraccion fallido [Saldo + Descubierto Insuficiente]: (Monto[{monto}]), (Saldo[{self._saldo}]), (Descubierto[{self._descubierto}])")
            raise ValueError("Limite de descubierto superado...")

        self._saldo -= monto
        self._registrar_historial(TipoTransaccion.EXTRACCION, monto)

        logger.info(f"Extraccion exitosa de [${monto}] en (ID_Cuenta[{self._numero}]): (Nuevo Saldo[{self._saldo}]), (Descubierto[{self._descubierto}])")

    @override

    def __str__(self) -> str:

        return f"Cuenta C-{self._numero} | Saldo: {self._saldo} | Descubierto: {self._descubierto}"

#Cuentas-------------------------------

#Clietes-------------------------------

class Cliente():

    #Constructor:

    def __init__(
                 self, 
                 nombre: str, 
                 dni: str, 
                 cuentas: list[Cuenta] | None = None
        ) -> None:

        if not es_nombre_cliente_valido(nombre):
            raise ValueError("Nombre invalido...")
        self._nombre: str = nombre.strip()

        if not es_dni_cliente_valido(dni):
            raise ValueError("DNI invalido...")
        self._dni: str = dni.strip().replace(".", "")

        if cuentas is not None:
            #Validacion hecha aqui, porque sino tengo importacion circular con "validators.py"
            if not isinstance(cuentas, list) or not all(isinstance(c, Cuenta) for c in cuentas):
                raise ValueError("Lista de cuentas invalida...")
            self._cuentas: list[Cuenta] = list(cuentas)
        else: self._cuentas = []

    #Getters:

    def get_nombre(self) -> str:

        return self._nombre

    def get_dni(self) -> str:

        return self._dni

    @property

    def cuentas(self) -> list[Cuenta]:

        return self._cuentas.copy()

    #Setters:

    def set_nombre(self, nombre: str) -> None:

        if not es_nombre_cliente_valido(nombre):
            raise ValueError("Nombre invalido...")
        self._nombre = nombre.strip()

    #Methods;

    def listar_cuentas_con_tipo(self) -> list[tuple[CuentaAhorro | CuentaCorriente, bool]]:

        lista_cuentas_con_tipo_asignado = []

        for cuenta in self.cuentas:
            lista_cuentas_con_tipo_asignado.append((cuenta, True)) if isinstance(cuenta, CuentaAhorro) else lista_cuentas_con_tipo_asignado.append((cuenta, False))

        return lista_cuentas_con_tipo_asignado


    def agregar_cuenta(self, cuenta: Cuenta) -> None:

        if not isinstance(cuenta, Cuenta): #Valido que la Cuenta sea valida...
            logger.error(f"Intento de agregar cuenta fallido [Cuenta Invalida]: {cuenta}")
            raise ValueError("Cuenta invalida...")

        if any(c.get_numero() == cuenta.get_numero() for c in self._cuentas):
            logger.error(f"Intento de agregar cuenta fallido [Cuenta Ya Existente]: {cuenta}")
            raise ValueError("La cuenta ya pertenece al cliente...")

        self._cuentas.append(cuenta)

        logger.info(f"Agregacion de Cuenta exitosa: (Nueva Cuenta[{cuenta}])")

    def depositar_en_cuenta(self, numero_cuenta: str, monto: Decimal) -> None:
        """Busca la cuenta del cliente y realiza el depósito."""
        for cuenta in self._cuentas:
            if cuenta.get_numero() == numero_cuenta:
                cuenta.depositar(monto)
                return
        raise ValueError("No se encontró una cuenta con ese número asociada al cliente.")

    def extraer_de_cuenta(self, numero_cuenta: str, monto: Decimal) -> None:
        """Busca la cuenta del cliente y realiza la extracción."""
        for cuenta in self._cuentas:
            if cuenta.get_numero() == numero_cuenta:
                cuenta.extraer(monto)  # Ya maneja los límites de caja de ahorro o corriente
                return
        raise ValueError("No se encontró una cuenta con ese número asociada al cliente.")

    def total(self) -> Decimal:

        return sum((c.get_saldo() for c in self._cuentas), Decimal("0.00"))

    #SRT Method:

    # SRT Method: ESTE ME LO HIZO LA IA PORQUE NO SE QUE COSA DE STR DENTRO DE OTRO STR...

    def __str__(self) -> str:
        # Unimos las representaciones de cada cuenta usando una list comprehension limpia
        cuentas_str = "\n  - ".join(str(cuenta) for cuenta in self._cuentas)
        
        return f"Cliente — [Nombre: {self._nombre}] [DNI: {self._dni}]\nCuentas Asociadas:\n  - {cuentas_str}"

#Clietes-------------------------------

#Bancos--------------------------------

class Banco():

    #Constructor:

    def __init__(
            self, 
            nombre: str
    ) -> None:

        if not es_nombre_banco_valido(nombre):
            raise ValueError("Nombre banco invalido...")
        self._nombre = nombre

        self._clientes: list[Cliente] = []

    #Getters:

    def get_nombre(self) -> str:

        return self._nombre

    @property

    def clientes(self) -> list[Cliente]:

        return self._clientes.copy()

    #Methods:

    def buscar_cliente_por_dni(self, dni_normalizado: str) -> Cliente | None:

        i = 0
        cliente_encontrado: Cliente | None = None

        if self.clientes:
            while i < len(self.clientes) and cliente_encontrado is None:
                
                cl = self.clientes[i]

                if cl.get_dni() == dni_normalizado:
                    
                    cliente_encontrado = cl

                i += 1

        return cliente_encontrado

    def alta_cliente(self, nombre: str, dni: str) -> Cliente:

        dni_normalizado = dni.strip().replace(".", "")

        if any(cl.get_dni() == dni_normalizado for cl in self._clientes):
            logger.error(f"Alta a Cliente fallida [DNI ya registrado]: (DNI_normalizado[{dni_normalizado}])")
            raise ValueError("DNI ya registrado...")

        cliente = Cliente(nombre, dni_normalizado)
        self._clientes.append(cliente)


        logger.info(f"Alta a Cliente exitosa: (Nuevo Cliente[{cliente}])")

        return cliente
        
    def resumen(self) -> None:

        #Este es un procedimiento que muestra por terminal el resumen del banco, luego esto se usa temporalmente, luego se hara un metodo que permira mostrar un resumen con sentido.

        print("\n")
        print(f"---------------------- Banco {self._nombre} ----------------------\n")
        print(f"\n------------------------------------------------------------------")
        for cl in self._clientes: 
            print(f"- Cliente: {cl.get_nombre()} - DNI: {cl.get_dni()} — Total: ${cl.total()}\n")
            for cue in cl.cuentas: 
                print(f"\t{cue}")
            print("\n------------------------------------------------------------------\n")
        print("\n")
#Bancos--------------------------------