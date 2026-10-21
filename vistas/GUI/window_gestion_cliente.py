# Ventana donde se hara todo lo relacionado a la gestion de clientes...

# Imports:

from PySide6.QtWidgets import (
    QVBoxLayout, 
    QPushButton, 
    QLabel, 
    QWidget, 
    QStackedWidget
)
from PySide6.QtCore import Qt

from models.objects_models import Banco
from core.core_gui import flujo_seleccionar_cliente_gui, flujo_mostrar_clientes_gui

# Constants:

# Class:

class WindowGestionCliente(QWidget): #pragma: no cover

    # Constructor:
    def __init__(
            self, 
            parent: QWidget | None = None, 
            banco: Banco | None = None
    ) -> None:
        super().__init__(parent)
        self.banco: Banco | None = banco
        self.init_ui()

    # Methods:
    def ejecutar_seleccionar_cliente(self) -> None:
        from typing import cast, Any
        from vistas.GUI.window_cliente import WindowCliente

        # Llamamos a la funcion de flujo correspondiente:
        cliente_seleccionado = flujo_seleccionar_cliente_gui(
            self.banco, 
            self
        )

        if not cliente_seleccionado: return

        # Obtenemos la ventana principal (MainWindow)
        ventana_principal = cast(Any, self.window())

        # Instanciamos la vista del cliente pasándole el cliente ya seleccionado
        pagina_cliente = WindowCliente(
            parent=ventana_principal, 
            banco=self.banco, 
            cliente=cliente_seleccionado
        )

        # La agregamos dinámicamente al QStackedWidget y guardamos su índice
        indice_nueva_pagina = ventana_principal.stacked_widget.addWidget(pagina_cliente)

        # Nos movemos instantáneamente a esa nueva página
        ventana_principal.stacked_widget.setCurrentIndex(indice_nueva_pagina)

    def ejecutar_mostrar_cliente(self) -> None:
        # Llamamos a la logica ya hecha:
        flujo_mostrar_clientes_gui(
            self.banco, 
            self
        )

    def ejecutar_volver_atras(self) -> None:
        from typing import cast, Any

        # self.window() obtiene directamente la ventana principal (MainWindow)
        ventana_principal = cast(Any, self.window())
        ventana_principal.stacked_widget.setCurrentIndex(0)

    def init_ui(self) -> None:

        # Configuración básica del contenedor:
        layout_exterior = QVBoxLayout(self)

        # Creamos otro QWidget (panel) para mantener el diseño de caja con márgenes
        panel_gestion = QWidget(self)
        panel_layout = QVBoxLayout(panel_gestion)

        # Creamos los Widgets a usar:
        label_gestion_clientes = QLabel("⚙️ Gestión de Clientes", panel_gestion)

        button_mostrar_clientes = QPushButton("Mostrar Clientes", panel_gestion)
        button_seleccionar_clientes = QPushButton("Seleccionar Cliente", panel_gestion)
        button_volver_atras = QPushButton("Atrás", panel_gestion)

        # Sincronizamos los Widgets al Layout del panel:
        panel_layout.addWidget(label_gestion_clientes)
        panel_layout.addWidget(button_mostrar_clientes)
        panel_layout.addWidget(button_seleccionar_clientes)
        panel_layout.addStretch()
        panel_layout.addWidget(button_volver_atras)

        # Metemos el panel dentro del layout exterior
        layout_exterior.addWidget(panel_gestion)

        # Sincronizamos los botones a sus acciones:
        button_seleccionar_clientes.clicked.connect(self.ejecutar_seleccionar_cliente)
        button_mostrar_clientes.clicked.connect(self.ejecutar_mostrar_cliente)
        button_volver_atras.clicked.connect(self.ejecutar_volver_atras)

        # Estilos:

        # Estilo del panel contenedor (la caja central)
        panel_gestion.setStyleSheet("""
            background-color: #0F0525;
            border-radius: 10px;
        """)

        # Estilo del título principal
        label_gestion_clientes.setStyleSheet("""
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
        button_mostrar_clientes.setStyleSheet(estilo_botones)
        button_seleccionar_clientes.setStyleSheet(estilo_botones)
        button_volver_atras.setStyleSheet(estilo_boton_volver)

        # Alineaciones:
        label_gestion_clientes.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Margenes:
        panel_layout.setContentsMargins(25, 25, 25, 25)

        # Colores de fondo de la ventana contenedora:
        self.setStyleSheet("background-color: #000000;")


# Prueba de ventana:

if __name__ == "__main__": #pragma: no cover

    # Importo localmente lo necesario:
    import sys
    from PySide6.QtWidgets import QApplication
    
    from logs.loggers import configurar_logging
    from datos.persistencia import cargar_datos

    # Configuramos el logging:
    configurar_logging()

    # Instancio la app de prueba:
    app_prueba = QApplication(sys.argv)

    # Instancio el banco cargando del JSON:
    banco_prueba: Banco = cargar_datos()

    # Instancio la ventana a probar:
    ventana_a_probar = WindowGestionCliente(banco=banco_prueba)

    # Muestro la ventana a probar:
    ventana_a_probar.resize(450, 450)
    ventana_a_probar.show()

    # Ahora, pongo ejecutar el event Loop:
    sys.exit(app_prueba.exec())