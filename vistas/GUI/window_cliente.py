# Ventana donde se ejecutara la logica de el menu de opciones que tiene un cliente...

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

from core.core_gui import flujo_depositar_gui, flujo_extraer_gui

# Constants:

# Class:

class WindowCliente(QWidget): #pragma: no cover

    """
        Representa la vista de menú de operaciones (`QWidget`) para un cliente específico en la GUI.

        Permite visualizar la información del cliente activo y acceder a las opciones
        para crear cuentas nuevas (ahorro o corriente), realizar depósitos, extracciones
        o regresar al menú anterior de gestión, manteniendo la estética oscura corporativa.

        Attributes:
            banco (Banco | None): Instancia del banco actual.
            cliente (Cliente | None): Instancia del cliente actualmente seleccionado.
            label_titulo_cliente (QLabel): Etiqueta visual con los datos del cliente.

        Examples:
            >>> # ventana_cliente = WindowCliente(parent=None, banco=banco, cliente=cliente)
            >>> # ventana_cliente.show()
    """

    # Constructor:
    def __init__(
            self, 
            parent: QWidget | None = None, 
            banco: Banco | None = None,
            cliente: Cliente | None = None, 
    ) -> None:

        """
            Inicializa la ventana de operaciones del cliente configurando el modelo de datos
            y construyendo los componentes visuales de la interfaz.

            Args:
                parent (QWidget | None, optional): Widget padre de la vista.
                banco (Banco | None, optional): Instancia de la entidad bancaria.
                cliente (Cliente | None, optional): Instancia del cliente activo.
        """
        
        super().__init__(parent)
        self.banco: Banco | None = banco
        self.cliente: Cliente | None = cliente
        self.init_ui()

    # Methods:
    def cargar_cliente(self, cliente: Cliente) -> None:

        """
            Actualiza dinámicamente el cliente activo al navegar desde la vista de selección.

            Args:
                cliente (Cliente): Nueva instancia de cliente seleccionado.

            Returns:
                None
        """

        # Método para actualizar dinámicamente el cliente activo al navegar desde la selección
        self.cliente = cliente
        if self.cliente:
            self.label_titulo_cliente.setText(f"Cliente: {self.cliente.get_nombre()}\nDNI: {self.cliente.get_dni()}")

    def ejecutar_crear_cuenta(self) -> None:

        """
            Instancia y despliega de forma dinámica la vista de creación de cuentas (`WindowCrearCuenta`)
            añadiéndola a la pila de navegación principal (`QStackedWidget`).
        """

        # Importamos localmente la ventana hija asi no hay importacion circular:
        from vistas.GUI.window_crear_cuenta import WindowCrearCuenta
        from typing import cast, Any

        # Obtenemos la ventana principal (MainWindow)
        ventana_principal = cast(Any, self.window())

        # Instanciamos la vista de crear cuenta pasándole el banco y el cliente actual
        pagina_crear_cuenta = WindowCrearCuenta(
            parent=ventana_principal, 
            banco=self.banco, 
            cliente=self.cliente, 
            preview_window=self
        )

        # La agregamos dinámicamente al QStackedWidget y guardamos su índice
        indice_nueva_pagina = ventana_principal.stacked_widget.addWidget(pagina_crear_cuenta)

        # Nos movemos instantáneamente a esa nueva página
        ventana_principal.stacked_widget.setCurrentIndex(indice_nueva_pagina)

    def ejecutar_deposito(self) -> None:

        """
            Ejecuta el flujo visual mediante diálogo para realizar un depósito en una cuenta del cliente.
        """

        # Llamamos a la funcion que tiene el flujo:
        flujo_depositar_gui(
            self.banco, 
            self.cliente, 
            self
        )

    def ejecutar_extracion(self) -> None:

        """
            Ejecuta el flujo visual mediante diálogo para realizar una extracción de una cuenta del cliente.
        """

        # Llamamos a la funcion que tiene el flujo:
        flujo_extraer_gui(
            self.banco, 
            self.cliente, 
            self
        )

    def ejecutar_volver_atras(self) -> None:

        """
            Navega de regreso a la página de gestión de clientes (Índice 1 en la pila principal).
        """

        from typing import cast, Any

        # Volvemos a la página de gestión de clientes (Índice 1 en la pila principal)
        ventana_principal = cast(Any, self.window())
        if hasattr(ventana_principal, "stacked_widget"):
            ventana_principal.stacked_widget.setCurrentIndex(1)

    def init_ui(self) -> None:

        """
            Configura los componentes del menú de operaciones, los diseños de contenedores,
            las conexiones de eventos de los botones y los estilos visuales de la vista.
        """

        # Configuración básica del contenedor:
        layout_exterior = QVBoxLayout(self)

        # Creamos otro QWidget (panel) para mantener el diseño de caja con márgenes
        panel_cliente = QWidget(self)
        panel_layout = QVBoxLayout(panel_cliente)

        # Creamos los Widgets necesarios:
        nombre_inicial = f"👤 Cliente: {self.cliente.get_nombre()}" if self.cliente else "Cliente no seleccionado"
        self.label_titulo_cliente = QLabel(nombre_inicial, panel_cliente)

        button_crear_cuenta = QPushButton("Crear Cuenta", panel_cliente)
        button_depositar = QPushButton("Depositar", panel_cliente)
        button_extraer = QPushButton("Extraer", panel_cliente)
        button_atras = QPushButton("Atrás", panel_cliente)

        # Sincronizamos los Widgets al Layout del panel:
        panel_layout.addWidget(self.label_titulo_cliente)
        panel_layout.addWidget(button_crear_cuenta)
        panel_layout.addWidget(button_depositar)
        panel_layout.addWidget(button_extraer)
        panel_layout.addStretch()
        panel_layout.addWidget(button_atras)

        # Metemos el panel dentro del layout exterior
        layout_exterior.addWidget(panel_cliente)

        # Sincronizamos los botones a sus señales:
        button_crear_cuenta.clicked.connect(self.ejecutar_crear_cuenta)
        button_depositar.clicked.connect(self.ejecutar_deposito)
        button_extraer.clicked.connect(self.ejecutar_extracion)
        button_atras.clicked.connect(self.ejecutar_volver_atras)

        # Estilos:

        # Estilo del panel contenedor (la caja central)
        panel_cliente.setStyleSheet("""
            background-color: #0F0525;
            border-radius: 10px;
        """)

        # Estilo del título del cliente
        self.label_titulo_cliente.setStyleSheet("""
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
        button_crear_cuenta.setStyleSheet(estilo_botones)
        button_depositar.setStyleSheet(estilo_botones)
        button_extraer.setStyleSheet(estilo_botones)
        button_atras.setStyleSheet(estilo_boton_volver)

        # Alineaciones:
        self.label_titulo_cliente.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Margenes:
        panel_layout.setContentsMargins(25, 25, 25, 25)

        # Colores de fondo de la ventana contenedora:
        self.setStyleSheet("background-color: #000000;")


# Prueba de ventana:
if __name__ == "__main__": #pragma: no cover

    # Local imports:
    import sys
    from PySide6.QtWidgets import QApplication

    from logs.loggers import configurar_logging
    from datos.persistencia import cargar_datos

    # Configuro el logging:
    configurar_logging()

    # Instanciamos la app de prueba:
    app_prueba = QApplication(sys.argv)

    # Inicializamos los datos de prueba:
    banco_prueba: Banco = cargar_datos()

    # Buscamos el cliente con el dni:
    cliente_encontrado = None
    dni_normalizado_cliente = input("Ingrese el DNI del Cliente: ").strip().replace(".", "")

    for cliente in banco_prueba.clientes:
        if cliente.get_dni() == dni_normalizado_cliente: 
            cliente_encontrado = cliente
            break

    if cliente_encontrado:
        # Instanciamos la ventana para probarla individualmente:
        ventana_cliente_prueba: WindowCliente = WindowCliente(
            parent=None, 
            banco=banco_prueba, 
            cliente=cliente_encontrado
        )
        ventana_cliente_prueba.resize(450, 450)
        ventana_cliente_prueba.show()
        sys.exit(app_prueba.exec())
    else: 
        print("No se encontró ese cliente.")