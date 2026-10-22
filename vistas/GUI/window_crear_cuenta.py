# Ventana donde se ejecutara la logica de crear una Cuenta para un Cliente teniendo en cuenta el DNI, sin importar si es Cuenta de Ahorro o Cuenta Corriente...

# Imports:

from PySide6.QtWidgets import (
    QPushButton, 
    QVBoxLayout, 
    QLabel, 
    QWidget
)
from PySide6.QtCore import Qt

from models.objects_models import (
    Banco, 
    Cliente
)
from core.core_gui import (
    flujo_crear_cuenta_corriente_gui, 
    flujo_crear_cuenta_ahorro_gui
)

# Constants:

# Class:

class WindowCrearCuenta(QWidget): #pragma: no cover

    """
        Representa la vista de selección y creación de cuentas (`QWidget`) para un cliente en la GUI.

        Permite al usuario elegir entre crear una cuenta de ahorro o una cuenta corriente
        para el cliente activo, invocando los flujos correspondientes y manejando
        el retorno dinámico a la ventana previa mediante el sistema de navegación.

        Attributes:
            banco (Banco | None): Instancia actual del banco.
            cliente (Cliente | None): Instancia del cliente al cual se le asociará la cuenta.
            preview_window (QWidget | None): Referencia a la ventana anterior para un retorno fluido.

        Examples:
            >>> # ventana_crear = WindowCrearCuenta(parent=None, banco=banco, cliente=cliente, preview_window=ventana_anterior)
            >>> # ventana_crear.show()
    """

    # Constructor que hereda de QWidget:
    def __init__(
            self, 
            parent: QWidget | None = None, 
            banco: Banco | None = None, 
            cliente: Cliente | None = None, 
            preview_window: QWidget | None = None
    ) -> None:

        """
            Inicializa la ventana de creación de cuentas configurando los modelos de datos
            y construyendo los componentes visuales de la interfaz.

            Args:
                parent (QWidget | None, optional): Widget padre de la vista.
                banco (Banco | None, optional): Instancia del banco actual.
                cliente (Cliente | None, optional): Instancia del cliente titular.
                preview_window (QWidget | None, optional): Ventana previa para navegación hacia atrás.
        """
        
        super().__init__(parent)
        self.banco: Banco | None = banco
        self.cliente: Cliente | None = cliente
        self.preview_window: QWidget | None = preview_window
        self.init_ui()

    # Methods:
    def cargar_cliente(self, cliente: Cliente) -> None:

        """
            Actualiza dinámicamente el cliente asociado al navegar entre vistas.

            Args:
                cliente (Cliente): Nueva instancia de cliente activo.

            Returns:
                None
        """

        # Método para actualizar dinámicamente el cliente si es necesario al navegar
        self.cliente = cliente

    def ejecutar_crear_cuenta_ahorro(self) -> None:

        """
            Ejecuta el flujo visual de la GUI para crear y asociar una cuenta de ahorro.
        """

        # Llamamos a la funcion encargada de esta tarea:
        flujo_crear_cuenta_ahorro_gui(self.banco, self.cliente, self)

    def ejecutar_crear_cuenta_corriente(self) -> None:

        """
            Ejecuta el flujo visual de la GUI para crear y asociar una cuenta corriente.
        """

        # Llamamos a la funcion encargada de esta tarea:
        flujo_crear_cuenta_corriente_gui(self.banco, self.cliente, self)

    def ejecutar_volver_atras(self) -> None:

        """
            Navega de regreso a la ventana anterior guardada en `preview_window`.
        """

        from typing import cast, Any

        # Si tenemos guardada la ventana anterior, volvemos exactamente a ella de forma dinámica
        if self.preview_window:
            ventana_principal = cast(Any, self.window())
            ventana_principal.stacked_widget.setCurrentWidget(self.preview_window)

    # Modulo instanciador:
    def init_ui(self) -> None:

        """
            Configura la estructura de contenedores, los botones de opción (ahorro o corriente),
            las conexiones de eventos y los estilos visuales de la ventana.
        """

        # Configuración básica del contenedor exterior:
        layout_exterior = QVBoxLayout(self)

        # Creamos otro QWidget (panel) para mantener el diseño de caja con márgenes
        panel_crear_cuenta = QWidget(self)
        panel_layout = QVBoxLayout(panel_crear_cuenta)

        # Creamos los elementos:
        label_titulo_crear_cuenta = QLabel("💳 CREAR CUENTA", panel_crear_cuenta)

        button_crear_cuenta_a = QPushButton("Crear Cuenta de Ahorro", panel_crear_cuenta)
        button_crear_cuenta_c = QPushButton("Crear Cuenta Corriente", panel_crear_cuenta)
        button_atras = QPushButton("Atrás", panel_crear_cuenta)

        # Sincronizamos los elementos al Layout del panel:
        panel_layout.addWidget(label_titulo_crear_cuenta)
        
        panel_layout.addSpacing(10)
        
        panel_layout.addWidget(button_crear_cuenta_a)
        panel_layout.addWidget(button_crear_cuenta_c)
        
        panel_layout.addStretch()
        
        panel_layout.addWidget(button_atras)

        # Metemos el panel dentro del layout exterior
        layout_exterior.addWidget(panel_crear_cuenta)

        # Sincronizamos los elementos con su accion:
        button_crear_cuenta_a.clicked.connect(self.ejecutar_crear_cuenta_ahorro)
        button_crear_cuenta_c.clicked.connect(self.ejecutar_crear_cuenta_corriente)
        button_atras.clicked.connect(self.ejecutar_volver_atras)

        # Estilos:

        # Estilo del panel contenedor (la caja central)
        panel_crear_cuenta.setStyleSheet("""
            background-color: #0F0525;
            border-radius: 10px;
        """)

        # Estilo del título principal
        label_titulo_crear_cuenta.setStyleSheet("""
            color: #F5F2EB;
            font-size: 20pt;
            font-weight: bold;
            margin-bottom: 15px;
        """)

        # Estilo común para los botones de acción
        estilo_botones = """
            QPushButton {
                background-color: #6A00FF;
                color: #F5F2EB;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 5px;
            }
            QPushButton:hover {
                background-color: #5500CC;
            }
        """

        # Estilo diferenciado para el botón de volver atrás
        estilo_boton_volver = """
            QPushButton {
                background-color: #FF0041;
                color: #F5F2EB;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #D90037;
            }
        """

        # Aplicaciones de Estilos predefinidos:
        button_crear_cuenta_a.setStyleSheet(estilo_botones)
        button_crear_cuenta_c.setStyleSheet(estilo_botones)
        button_atras.setStyleSheet(estilo_boton_volver)

        # Alineaciones:
        label_titulo_crear_cuenta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Margenes:
        panel_layout.setContentsMargins(25, 25, 25, 25)

        # Colores de fondo de la ventana contenedora:
        self.setStyleSheet("background-color: #000000;")


# Prueba de ventana:

if __name__ == "__main__": #pragma: no cover

    # Local Imports:
    import sys
    from PySide6.QtWidgets import QApplication
    from logs.loggers import configurar_logging
    from datos.persistencia import cargar_datos

    # Configuro el logging:
    configurar_logging()

    # Inicializamos la app:
    ventana_app = QApplication(sys.argv)

    banco_prueba = cargar_datos()
    cliente_encontrado = None
    dni_normalizado_cliente = input("Ingrese el DNI del Cliente: ").strip().replace(".", "")

    for cliente in banco_prueba.clientes:
        if cliente.get_dni() == dni_normalizado_cliente:
            cliente_encontrado = cliente
            break

    if cliente_encontrado:
        # Instanciamos la ventana a probar individualmente:
        ventana_a_probar = WindowCrearCuenta(banco=banco_prueba, cliente=cliente_encontrado)
        ventana_a_probar.resize(450, 450)
        ventana_a_probar.show()
        sys.exit(ventana_app.exec())
    else:
        print("No se encontró ese cliente...")