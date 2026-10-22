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

    """
        Clase abstracta base que representa una cuenta bancaria genérica dentro del sistema.

        Define la estructura fundamental, atributos protegidos y contratos que deben
        cumplir los distintos tipos de cuentas específicas (Ahorro, Corriente).

        Attributes:
            _numero (str): Número identificador único de la cuenta (exactamente 22 dígitos).
            _saldo (Decimal): Balance actual de dinero disponible en la cuenta.
            _historial (Historial): Registro cronológico de todas las transacciones realizadas.

        Examples:
            >>> # Al ser abstracta, no se instancia directamente, sino a través de sus subclases.
            >>> isinstance(Cuenta, ABC)
            True
    """

    #Constructor: 

    def __init__(
            self, 
            numero: str, 
            saldo: Decimal | None = None, 
            historial: Historial | None = None
        ) -> None:

        """
            Inicializa una nueva cuenta bancaria validando sus parámetros base.

            Args:
                numero (str): Número identificador de la cuenta (22 dígitos).
                saldo (Decimal | None, optional): Saldo inicial. Si es None, inicia en 0.00.
                historial (Historial | None, optional): Historial previo de transacciones. Si es None, inicia vacío.

            Raises:
                ValueError: Si el número de cuenta, el saldo o el historial no son válidos.
        """

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

        """
            Obtiene el número identificador de la cuenta.

            Returns:
                str: Número de cuenta de 22 dígitos.

            Examples:
                >>> cuenta = CuentaAhorro("1234567890123456789012")
                >>> cuenta.get_numero()
                '1234567890123456789012'
        """

        return self._numero

    def get_saldo(self) -> Decimal:

        """
            Obtiene el saldo actual de la cuenta.

            Returns:
                Decimal: Balance monetario actual.

            Examples:
                >>> from decimal import Decimal
                >>> cuenta = CuentaAhorro("1234567890123456789012", saldo=Decimal("1500.00"))
                >>> cuenta.get_saldo()
                Decimal('1500.00')
        """

        return self._saldo

    def get_historial(self) -> Historial:

        """
            Obtiene una copia del historial de transacciones de la cuenta.

            Returns:
                Historial: Lista de tuplas con las transacciones (fecha, tipo, monto).

            Examples:
                >>> cuenta = CuentaAhorro("1234567890123456789012")
                >>> isinstance(cuenta.get_historial(), list)
                True
        """

        return self._historial.copy()

    #Getters:-------------------

    def _registrar_historial(self, tipo_transaccion: TipoTransaccion, monto: Decimal) -> None:

        """
            Registra internamente una nueva transacción en el historial de la cuenta.

            Args:
                tipo_transaccion (TipoTransaccion): Tipo de operación (DEPOSITO o EXTRACCION).
                monto (Decimal): Cantidad monetaria involucrada.

            Returns:
                None
        """

        self._historial.append((datetime.now(), tipo_transaccion, monto))

    def depositar(self, monto: Decimal) -> None:

        """
            Deposita una cantidad de dinero en la cuenta, incrementando el saldo
            y registrando la operación en el historial y en el sistema de logs.

            Args:
                monto (Decimal): Cantidad de dinero a depositar (debe ser mayor a 0).

            Returns:
                None

            Raises:
                ValueError: Si el monto ingresado no es válido.

            Examples:
                >>> from decimal import Decimal
                >>> cuenta = CuentaAhorro("1234567890123456789012", saldo=Decimal("1000.00"))
                >>> cuenta.depositar(Decimal("500.00"))
                >>> cuenta.get_saldo()
                Decimal('1500.00')
        """

        if not es_monto_valido(monto):
            logger.error(f"Intento de deposito fallido [Monto Invalido]: {monto}")
            raise ValueError("Monto invalido...")

        self._saldo = self._saldo + monto
        self._registrar_historial(TipoTransaccion.DEPOSITO, monto)

        logger.info(f"Deposito exitoso de [${monto}] en (ID_Cuenta[{self._numero}]): (Nuevo saldo[{self._saldo}])")

    @abstractmethod

    def extraer(self, monto: Decimal) -> None: 

        """
            Método abstracto para realizar extracciones de dinero según las reglas de cada cuenta.
        """
        
        pass #pragma: no cover

    #Strs:

    @abstractmethod

    def __str__(self) -> str: 
        
        """
            Método abstracto para representar la cuenta como cadena de texto.
        """
        
        pass #pragma: no cover

class CuentaAhorro(Cuenta): 

    """
        Representa una cuenta de ahorro tradicional dentro del sistema bancario.

        No permite realizar extracciones que dejen el saldo en números negativos.

        Examples:
            >>> from decimal import Decimal
            >>> ca = CuentaAhorro("1234567890123456789012", saldo=Decimal("1000.00"))
            >>> ca.extraer(Decimal("200.00"))
            >>> ca.get_saldo()
            Decimal('800.00')
    """

    #Constructor:

    def __init__(
            self, 
            numero: str, 
            saldo: Decimal | None = None, 
            historial: Historial | None = None
    ) -> None:
        
        """
            Inicializa una instancia de CuentaAhorro heredando de Cuenta.
        """

        super().__init__(numero, saldo, historial)

    @override

    def extraer(self, monto: Decimal) -> None:

        """
            Extrae una cantidad de dinero de la cuenta de ahorro.

            Verifica que el monto sea válido y que el saldo disponible sea suficiente.

            Args:
                monto (Decimal): Cantidad de dinero a retirar.

            Returns:
                None

            Raises:
                ValueError: Si el monto es inválido o si supera el saldo disponible.
        """

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

        """
            Retorna una representación legible de la cuenta de ahorro.
        """

        return f"Cuenta A-{self._numero} | Saldo:${self._saldo}"

class CuentaCorriente(Cuenta):

    """
        Representa una cuenta corriente que admite un límite de descubierto autorizado.

        Permite extraer dinero incluso con saldo cero, hasta alcanzar el límite
        de descubierto configurado.

        Attributes:
            _descubierto (Decimal): Límite máximo de saldo negativo permitido.
    """

    #Constructor: 

    def __init__(
        self,
        numero: str,
        saldo: Decimal | None = None,
        historial: Historial | None = None,
        descubierto: Decimal | None = None
    ) -> None:

        """
            Inicializa una CuentaCorriente configurando opcionalmente su límite de descubierto.

            Args:
                numero (str): Número identificador de la cuenta (22 dígitos).
                saldo (Decimal | None, optional): Saldo inicial.
                historial (Historial | None, optional): Historial previo de transacciones.
                descubierto (Decimal | None, optional): Límite de descubierto. Si es None, toma `DESCUBIERTO_POR_DEFECTO`.

            Raises:
                ValueError: Si el descubierto especificado no es válido.
        """
        
        super().__init__(numero, saldo, historial)

        if descubierto is not None:
            if not es_descubierto_cuenta_valido(descubierto): 
                raise ValueError("Descubierto invalido...")
            self._descubierto = descubierto
        else: self._descubierto = DESCUBIERTO_POR_DEFECTO

    #Getters:

    def get_descubierto(self) -> Decimal:

        """
            Obtiene el límite de descubierto autorizado de la cuenta corriente.

            Returns:
                Decimal: Monto máximo de descubierto permitido.
        """

        return self._descubierto

    @override

    def extraer(self, monto: Decimal) -> None:

        """
            Extrae dinero de la cuenta corriente considerando el saldo y el descubierto disponible.

            Args:
                monto (Decimal): Cantidad de dinero a retirar.

            Returns:
                None

            Raises:
                ValueError: Si el monto es inválido o si supera la suma del saldo y el descubierto.
        """

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

        """
            Retorna una representación legible de la cuenta corriente.
        """

        return f"Cuenta C-{self._numero} | Saldo: {self._saldo} | Descubierto: {self._descubierto}"

#Cuentas-------------------------------

#Clietes-------------------------------

class Cliente():

    """
        Representa a un cliente del banco, titular de una o varias cuentas bancarias.

        Attributes:
            _nombre (str): Nombre completo del cliente.
            _dni (str): Documento Nacional de Identidad normalizado (sin puntos ni espacios).
            _cuentas (list[Cuenta]): Lista de cuentas asociadas al cliente.

        Examples:
            >>> cliente = Cliente("Juan Pérez", "12345678")
            >>> cliente.get_nombre()
            'Juan Pérez'
            >>> cliente.get_dni()
            '12345678'
    """

    #Constructor:

    def __init__(
                 self, 
                 nombre: str, 
                 dni: str, 
                 cuentas: list[Cuenta] | None = None
        ) -> None:

        """
        Inicializa una nueva instancia de Cliente validando sus datos personales
        y su colección inicial de cuentas.

        Args:
            nombre (str): Nombre completo del cliente.
            dni (str): Número de DNI (con o sin puntos separadores).
            cuentas (list[Cuenta] | None, optional): Lista inicial de cuentas a asociar.
                Si es None, se inicializa como una lista vacía.

        Raises:
            ValueError: Si el nombre no es válido, si el DNI no cumple con el formato
                esperado o si alguno de los elementos de la lista de cuentas no es válido.

        Examples:
            >>> c = Cliente("María Pérez", "25456789")
            >>> len(c.cuentas)
            0
        """

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

        """
            Obtiene el nombre actual del cliente.

            Returns:
                str: Nombre completo del titular.

            Examples:
                >>> cliente = Cliente("Carlos Ruiz", "30111222")
                >>> cliente.get_nombre()
                'Carlos Ruiz'
        """

        return self._nombre

    def get_dni(self) -> str:

        """
            Obtiene el DNI normalizado del cliente (sin puntos ni espacios).

            Returns:
                str: DNI en formato de cadena numérica pura.

            Examples:
                >>> cliente = Cliente("Carlos Ruiz", "30.111.222")
                >>> cliente.get_dni()
                '30111222'
        """

        return self._dni

    @property

    def cuentas(self) -> list[Cuenta]:

        """
            Retorna una copia de la lista de cuentas asociadas al cliente
            para proteger el encapsulamiento interno.

            Returns:
                list[Cuenta]: Copia superficial de la colección de cuentas.

            Examples:
                >>> cliente = Cliente("Ana López", "28999888")
                >>> isinstance(cliente.cuentas, list)
                True
        """

        return self._cuentas.copy()

    #Setters:

    def set_nombre(self, nombre: str) -> None:

        """
            Actualiza el nombre del cliente previa validación de formato.

            Args:
                nombre (str): Nuevo nombre para el cliente.

            Returns:
                None

            Raises:
                ValueError: Si el nuevo nombre proporcionado no es válido.

            Examples:
                >>> cliente = Cliente("Ana López", "28999888")
                >>> cliente.set_nombre("Ana María López")
                >>> cliente.get_nombre()
                'Ana María López'
        """

        if not es_nombre_cliente_valido(nombre):
            raise ValueError("Nombre invalido...")
        self._nombre = nombre.strip()

    #Methods;

    def listar_cuentas_con_tipo(self) -> list[tuple[CuentaAhorro | CuentaCorriente, bool]]:

        """
            Genera un mapeo detallado de las cuentas del cliente indicando mediante
            un booleano si corresponden a una cuenta de ahorro o corriente.

            Returns:
                list[tuple[CuentaAhorro | CuentaCorriente, bool]]: Lista de tuplas donde
                el primer elemento es la cuenta y el segundo es True si es CuentaAhorro,
                o False si es CuentaCorriente.
        """

        lista_cuentas_con_tipo_asignado = []

        for cuenta in self.cuentas:
            lista_cuentas_con_tipo_asignado.append((cuenta, True)) if isinstance(cuenta, CuentaAhorro) else lista_cuentas_con_tipo_asignado.append((cuenta, False))

        return lista_cuentas_con_tipo_asignado


    def agregar_cuenta(self, cuenta: Cuenta) -> None:

        """
            Asocia una nueva cuenta bancaria al cliente tras validar que pertenezca
            a la jerarquía correcta y que su número no esté duplicado en su cartera.

            Args:
                cuenta (Cuenta): Instancia de CuentaAhorro o CuentaCorriente a agregar.

            Returns:
                None

            Raises:
                ValueError: Si el objeto no es una cuenta válida o si el número de cuenta
                    ya se encuentra registrado para este cliente.

            Examples:
                >>> cliente = Cliente("Luis Gomez", "32111444")
                >>> cuenta = CuentaAhorro("1234567890123456789012")
                >>> cliente.agregar_cuenta(cuenta)
                >>> len(cliente.cuentas)
                1
        """

        if not isinstance(cuenta, Cuenta): #Valido que la Cuenta sea valida...
            logger.error(f"Intento de agregar cuenta fallido [Cuenta Invalida]: {cuenta}")
            raise ValueError("Cuenta invalida...")

        if any(c.get_numero() == cuenta.get_numero() for c in self._cuentas):
            logger.error(f"Intento de agregar cuenta fallido [Cuenta Ya Existente]: {cuenta}")
            raise ValueError("La cuenta ya pertenece al cliente...")

        self._cuentas.append(cuenta)

        logger.info(f"Agregacion de Cuenta exitosa: (Nueva Cuenta[{cuenta}])")

    def depositar_en_cuenta(self, numero_cuenta: str, monto: Decimal) -> None:

        """
            Busca una cuenta específica del cliente por su número identificador
            y efectúa un depósito de dinero.

            Args:
                numero_cuenta (str): Número de la cuenta donde se depositará.
                monto (Decimal): Cantidad monetaria a ingresar.

            Returns:
                None

            Raises:
                ValueError: Si no se encuentra ninguna cuenta asociada con ese número
                    o si el monto del depósito no es válido.
        """
        
        for cuenta in self._cuentas:
            if cuenta.get_numero() == numero_cuenta:
                cuenta.depositar(monto)
                return
        raise ValueError("No se encontró una cuenta con ese número asociada al cliente.")

    def extraer_de_cuenta(self, numero_cuenta: str, monto: Decimal) -> None:

        """
            Busca una cuenta específica del cliente por su número identificador
            y efectúa una extracción de fondos respetando las reglas de la cuenta.

            Args:
                numero_cuenta (str): Número de la cuenta de donde se retirará.
                monto (Decimal): Cantidad monetaria a extraer.

            Returns:
                None

            Raises:
                ValueError: Si no se encuentra la cuenta asociada, si el monto es inválido
                    o si se superan los límites de saldo/descubierto.
        """
        
        for cuenta in self._cuentas:
            if cuenta.get_numero() == numero_cuenta:
                cuenta.extraer(monto)  # Ya maneja los límites de caja de ahorro o corriente
                return
        raise ValueError("No se encontró una cuenta con ese número asociada al cliente.")

    def total(self) -> Decimal:

        """
            Calcula la sumatoria total de los saldos disponibles en todas
            las cuentas asociadas al cliente.

            Returns:
                Decimal: Balance económico total acumulado por el cliente.

            Examples:
                >>> cliente = Cliente("Sofia Paz", "35777888")
                >>> cliente.total()
                Decimal('0.00')
        """

        return sum((c.get_saldo() for c in self._cuentas), Decimal("0.00"))

    #SRT Method:

    # SRT Method: ESTE ME LO HIZO LA IA PORQUE NO SE QUE COSA DE STR DENTRO DE OTRO STR...

    def __str__(self) -> str:

        """
            Genera una representación formateada en texto del cliente, mostrando
            sus datos personales y el detalle desglosado de todas sus cuentas.

            Returns:
                str: Cadena multilinea con la información completa del cliente.
        """
        
        # Unimos las representaciones de cada cuenta usando una list comprehension limpia
        cuentas_str = "\n  - ".join(str(cuenta) for cuenta in self._cuentas)
        
        return f"Cliente — [Nombre: {self._nombre}] [DNI: {self._dni}]\nCuentas Asociadas:\n  - {cuentas_str}"

#Clietes-------------------------------

#Bancos--------------------------------

class Banco():

    """
        Representa la institución bancaria central, encargada de administrar
        la base de clientes, coordinar altas y proveer reportes globales del sistema.

        Attributes:
            _nombre (str): Nombre comercial o razón social de la entidad bancaria.
            _clientes (list[Cliente]): Colección interna de clientes registrados en el banco.

        Examples:
            >>> banco = Banco("Banco de la Ciudad")
            >>> banco.get_nombre()
            'Banco de la Ciudad'
            >>> len(banco.clientes)
            0
    """

    #Constructor:

    def __init__(
            self, 
            nombre: str
    ) -> None:

        """
            Inicializa una nueva instancia de la entidad bancaria.

            Args:
                nombre (str): Nombre comercial del banco.

            Raises:
                ValueError: Si el nombre del banco provisto no es válido.

            Examples:
                >>> b = Banco("Banco Regional")
                >>> b.get_nombre()
                'Banco Regional'
        """

        if not es_nombre_banco_valido(nombre):
            raise ValueError("Nombre banco invalido...")
        self._nombre = nombre

        self._clientes: list[Cliente] = []

    #Getters:

    def get_nombre(self) -> str:

        """
            Obtiene el nombre comercial del banco.

            Returns:
                str: Nombre de la institución.
        """

        return self._nombre

    @property

    def clientes(self) -> list[Cliente]:

        """
            Retorna una copia de la lista global de clientes registrados en el banco.

            Returns:
                list[Cliente]: Copia de la cartera de clientes.
        """

        return self._clientes.copy()

    #Methods:

    def buscar_cliente_por_dni(self, dni_normalizado: str) -> Cliente | None:

        """
            Busca y retorna un cliente dentro de la cartera del banco utilizando
            su número de DNI normalizado.

            Args:
                dni_normalizado (str): DNI de 7 u 8 dígitos sin puntos ni espacios.

            Returns:
                Cliente | None: La instancia del cliente si es hallado, o None si no existe.

            Examples:
                >>> banco = Banco("Banco Test")
                >>> banco.buscar_cliente_por_dni("99999999") is None
                True
        """

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

        """
            Registra y da de alta un nuevo cliente en el banco, validando previamente
            que su DNI no se encuentre registrado en el sistema.

            Args:
                nombre (str): Nombre completo del nuevo cliente.
                dni (str): DNI del cliente (con o sin puntos).

            Returns:
                Cliente: La instancia del Cliente recién creado y agregado al banco.

            Raises:
                ValueError: Si el DNI ya pertenece a otro cliente registrado previamente.

            Examples:
                >>> banco = Banco("Banco Test")
                >>> cliente = banco.alta_cliente("Valeria Rios", "34555666")
                >>> cliente.get_nombre()
                'Valeria Rios'
        """

        dni_normalizado = dni.strip().replace(".", "")

        if any(cl.get_dni() == dni_normalizado for cl in self._clientes):
            logger.error(f"Alta a Cliente fallida [DNI ya registrado]: (DNI_normalizado[{dni_normalizado}])")
            raise ValueError("DNI ya registrado...")

        cliente = Cliente(nombre, dni_normalizado)
        self._clientes.append(cliente)


        logger.info(f"Alta a Cliente exitosa: (Nuevo Cliente[{cliente}])")

        return cliente
        
    def resumen(self) -> None:

        """
            Imprime por la terminal un reporte estructurado y legible con el estado
            actual de la entidad bancaria, detallando cada cliente y sus respectivas cuentas.

            Returns:
                None
        """

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