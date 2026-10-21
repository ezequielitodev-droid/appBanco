#Ventana donde se creara la app principal de la GUI:
#Imports:

from PySide6.QtWidgets import (
    QMainWindow, 
    QStackedWidget, 
    QVBoxLayout, 
    QLabel, 
    QWidget, 
    QDialog, 
    QPushButton
)
from PySide6.QtCore import Qt

from models.objects_models import Banco

from core.core_gui import flujo_dar_alta_cliente_gui, flujo_resumen_banco_gui, flujo_seleccionar_cliente_gui
from vistas.GUI.window_gestion_cliente import WindowGestionCliente
from vistas.GUI.window_cliente import WindowCliente
from vistas.GUI.window_crear_cuenta import WindowCrearCuenta

#Class:

class MainWindow(QMainWindow):

    #Constructor:
    def __init__(
            self, 
            parent: QWidget | None = None, 
            banco: Banco | None = None
    ) -> None:
        super().__init__(parent)
        self.banco: Banco | None = banco
        self.init_ui()

    #Methods:
    def ejecutar_dar_alta_cliente(self) -> None:
        
        # Llamamos a la función de flujo:
        flujo_dar_alta_cliente_gui(
            self.banco, 
            self
        )

    def ejecutar_resumen(self) -> None:

         #Llamamos a la función de flujo:
         flujo_resumen_banco_gui(
             self.banco, 
             self
         )

    def ejecutar_seleccionar_cliente(self) -> None:

        self.stacked_widget.setCurrentWidget(self.pagina_gestion) # Salta a la página 1

    def init_ui(self) -> None:

        #Configuración basica de la ventana:
        self.setWindowTitle("Sistema de Gestión Bancaria")

        #Configuramos la pila:
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Creamos la página inicial (Menú Principal) como un QWidget:
        self.main_page = QWidget(self)

        #Creamos el Layout de la ventana principal, este servira para centrar el panel que tendra un margen menor:
        layout_exterior = QVBoxLayout(self.main_page)

        #Creamos otro QWidget (panel) dentro de la pagina principal para dar ese efecto de margen menor, esta confiurado en estilos:
        panel_menu = QWidget(self.main_page)

        #Creo un nuevo layout para ese panel:
        panel_layout = QVBoxLayout(panel_menu)

        #Creamos los Widgets principales:
        if not self.banco: return
        label_titulo = QLabel(f"Banco {self.banco.get_nombre()}", panel_menu)

        button_dar_alta = QPushButton("Dar Alta a Cliente", panel_menu)
        button_gestionar_clientes = QPushButton("Gestionar Clientes", panel_menu)
        button_resumen_banco = QPushButton("Mostrar Resumen de Banco", panel_menu)
        button_salir = QPushButton("Salir", panel_menu)

        #Sincronizamos los Widgets al Layout del panel:
        panel_layout.addWidget(label_titulo)
        panel_layout.addWidget(button_dar_alta)
        panel_layout.addWidget(button_gestionar_clientes)
        panel_layout.addWidget(button_resumen_banco)
        panel_layout.addWidget(button_salir)

        #Metemos el panel dentro del layout exterior
        layout_exterior.addWidget(panel_menu)

        #Índice 0: Menú Principal
        self.stacked_widget.addWidget(self.main_page)

        #Índice 1: Gestión de Clientes
        self.pagina_gestion = WindowGestionCliente(self, self.banco)
        self.stacked_widget.addWidget(self.pagina_gestion)

        #Índice 2: Menú de Acciones del Cliente (WindowCliente)
        self.pagina_cliente = WindowCliente(self, self.banco, cliente=None)
        self.stacked_widget.addWidget(self.pagina_cliente)

        #Indice 3: Menú de Acciones de Crear Cuenta (WindowCrearCuenta)
        self.pagina_crear_cuenta = WindowCrearCuenta(self, self.banco, cliente=None)

        #Conexiones de botones a acciones:
        button_dar_alta.clicked.connect(self.ejecutar_dar_alta_cliente)
        button_resumen_banco.clicked.connect(self.ejecutar_resumen)
        button_gestionar_clientes.clicked.connect(self.ejecutar_seleccionar_cliente)
        button_salir.clicked.connect(self.close)

    











        #Estilos:

        # Estilo del panel contenedor (la "caja" central de otro color con bordes redondeados)
        panel_menu.setStyleSheet("""
            background-color: #0F0525;
            border-radius: 10px;
        """)

        # Estilo del título principal
        label_titulo.setStyleSheet("""
            color: #F5F2EB;
            font-size: 30pt;
            font-weight: bold;
            margin-bottom: 10px;
        """)

        # Estilo común para los botones de acción
        estilo_botones = """
            QPushButton {
                background-color: #6A00FF;
                color: #F5F2EB;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5500CC;
            }
        """

        # Estilo diferenciado para el botón salir
        button_salir.setStyleSheet("""
            QPushButton {
                background-color: #FF0041;
                color: #F5F2EB;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #D90037;
            }
        """)

        #Aplicaciones de Estilos predefinidos:
        button_dar_alta.setStyleSheet(estilo_botones)
        button_gestionar_clientes.setStyleSheet(estilo_botones)
        button_resumen_banco.setStyleSheet(estilo_botones)
        
        #Alineaciones:
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter) #Centra horizontalmente el titulo

        #Tamaños:
        self.resize(450, 450) #Establece el tamanio de la ventana principal

        #Margenes:
        panel_layout.setContentsMargins(20, 20, 20, 20) # Márgenes internos del panel

        #Colores de fondo:
        self.setStyleSheet("background-color: #000000;") #Cambia el color de fondo de la ventana principal


#PALETA DE COLORES:
#Morado: #0F0525
#Negro: #000000
#Purpura: #6A00FF
#Purpura oscuro: #5500CC
#Rojo: #FF0041
#Rojo oscuro: #D90037
#Griz: #716B70
#Blanco huego: #F5F2EB