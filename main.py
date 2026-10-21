# Archivo principal:

# Imports:
import sys
from PySide6.QtWidgets import (
    QApplication, 
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QPushButton
)
from PySide6.QtCore import Qt

from vistas.cli import flujo_cli_app
from logs.loggers import configurar_logging
from datos.persistencia import cargar_datos
from models.objects_models import Banco
# Importa tu ventana principal desde donde la tengas guardada:
from vistas.GUI.main_window import MainWindow


# Función para elegir el modo:

def seleccionar_interfaz() -> str | None:
    """Abre una mini ventana con PySide6 para elegir el modo de ejecución."""
    
    dialog = QDialog()
    dialog.setWindowTitle("Selector de Interfaz")
    dialog.setFixedSize(300, 160)
    dialog.setModal(True)

    # Creamos el contenedor:
    layout = QVBoxLayout(dialog)

    # Creamos los Widgets:
    label = QLabel("¿Cómo deseas iniciar?", dialog)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("font-size: 11pt; font-weight: bold;")

    btn_cli = QPushButton("💻 Terminal (CLI)", dialog)
    btn_gui = QPushButton("🖥️ Interfaz Gráfica (GUI)", dialog)

    # Sincronizamos los Widgets a su contenedor:
    layout.addWidget(label)
    layout.addWidget(btn_cli)
    layout.addWidget(btn_gui)

    # Diccionario para capturar la elección:
    resultado: dict[str, str | None] = {"modo": None}

    def elegir_cli() -> None:
        resultado["modo"] = "cli"
        dialog.accept()

    def elegir_gui() -> None:
        resultado["modo"] = "gui"
        dialog.accept()

    # Conectamos los botones:
    btn_cli.clicked.connect(elegir_cli)
    btn_gui.clicked.connect(elegir_gui)

    # Lanzamos el diálogo y esperamos la selección:
    dialog.exec()
    return resultado["modo"]


# Flujo principal:

if __name__ == "__main__":

    # Llamada a crear y configurar el equipo instrumental...
    configurar_logging()

    # Inicializamos la aplicación de Qt antes de abrir cualquier ventana:
    app = QApplication(sys.argv)

    # Seleccionamos el modo de ejecución mediante la ventana gráfica de PySide6:
    modo_operandum = seleccionar_interfaz()

    if modo_operandum == "gui":
        
        # Cargamos el banco desde el JSON:
        banco_prueba: Banco = cargar_datos()

        # Instanciamos y mostramos la ventana principal:
        ventana_principal = MainWindow(None, banco_prueba)
        ventana_principal.show()

        # Ejecutamos el loop de la aplicación:
        sys.exit(app.exec())

    else:
        # Ejecutamos la terminal:
        flujo_cli_app()