#Imports: 

from enum import StrEnum

#Enums: 

class TipoTransaccion(StrEnum):
    
    """
        Representa los diferentes tipos de transacciones financieras posibles
        en las cuentas del sistema bancario.

        Hereda de `StrEnum` para permitir comparaciones directas y una
        serialización limpia como cadenas de texto en archivos JSON.

        Attributes:
            EXTRACCION (str): Representa una operación de retiro o extracción de fondos.
            DEPOSITO (str): Representa una operación de ingreso o depósito de fondos.

        Examples:
            >>> TipoTransaccion.EXTRACCION
            <TipoTransaccion.EXTRACCION: 'extraccion'>
            
            >>> TipoTransaccion.DEPOSITO.value
            'deposito'
            
            >>> TipoTransaccion("extraccion") == TipoTransaccion.EXTRACCION
            True
    """

    EXTRACCION = "extraccion"
    DEPOSITO = "deposito"