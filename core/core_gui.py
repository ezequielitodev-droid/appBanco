#Archivo donde estan los modulos mas importantes del flujo con GUI:

#Imports:

from decimal import Decimal
import decimal
import random
import string
import logging

from PySide6.QtWidgets import (
    QMessageBox, 
    QWidget, 
    QInputDialog, 
    QComboBox, 
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QPushButton, 
    QLineEdit, 
    QTableWidget, 
    QTableWidgetItem, 
    QHeaderView, 
    QAbstractItemView
)
from PySide6.QtCore import Qt

from datos.persistencia import guardar_datos
from utils.valitators import es_descubierto_cuenta_valido
from errors.personalizate_errors import DescubiertoInvalidError
from models.objects_models import (
    Banco, 
    Cliente, 
    CuentaAhorro, 
    CuentaCorriente
)

#Constans:

#Global Variables:

logger = logging.getLogger(__name__)

#Moduls:

def flujo_crear_cuenta_ahorro_gui(
        banco: Banco | None = None, 
        cliente: Cliente | None = None, 
        v_padre: QWidget | None = None
    ) -> None: #pragma: no cover

    """
    
    Modulo encargado de ejecutar la accion de "crear una cuenta de ahorro en la GUI"...
    
    """

    #Creamos un numero rando para asignarle a la cuenta:
    num_cuenta: str = "".join(random.choices(string.digits, k=22))

    try:

        nueva_cuenta: CuentaAhorro = CuentaAhorro(num_cuenta)
        if cliente:
            cliente.agregar_cuenta(nueva_cuenta)
        else:
            raise ValueError

        logger.info(
            f"Cuenta de Ahorro agregada exitosamente desde la GUI: "
            f"Cuenta {num_cuenta} para Cliente DNI {cliente.get_dni()}"
        )

        if banco:
            guardar_datos(banco)
        else:
            raise ValueError

        vm_creacion_exitosa = QMessageBox.information(v_padre, "Exito", "¡Cuenta de Ahorro creada con éxito!")

    except ValueError as e:

        vm_error_crear_cuenta = QMessageBox.critical(v_padre, "Error", f"Error al crear la cuenta: {e}")

        logger.error(f"Error en creacion de Cuenta de Ahorro desde la GUI [ValueError]: {e}")

    except Exception as e:

        vm_error_inesperado = QMessageBox.critical(v_padre, "Error", f"Ocurrió un error inesperado: {e}")
        logger.error(f"Error inesperado en creación de Cuenta de Ahorro desde la GUI: {e}")

def flujo_crear_cuenta_corriente_gui(
        banco: Banco | None = None, 
        cliente: Cliente | None = None, 
        v_padre: QWidget | None = None
) -> None: #pragma: no cover

    """
    Modulo encargado de ejecutar la accion "Crear una Cuenta Corriente en un Cliente con la GUI"...
    """

    if not banco or not cliente: 
        return

    # Creamos un QDialog personalizado para mantener la estética oscura y corporativa
    dialog = QDialog(v_padre)
    dialog.setWindowTitle("Crear Cuenta Corriente")

    layout = QVBoxLayout(dialog)

    label_instruccion = QLabel("Ingrese el monto máximo de descubierto (ej: 477.43):", dialog)
    input_descubierto = QLineEdit(dialog)
    input_descubierto.setPlaceholderText("Máximo 500.00 (Por defecto: 500)")

    button_accept = QPushButton("Aceptar", dialog)

    layout.addWidget(label_instruccion)
    layout.addWidget(input_descubierto)
    
    layout.addSpacing(15)
    
    layout.addWidget(button_accept)

    resultado_descubierto: list[str] = []

    def procesar_creacion() -> None:
        try:
            descubierto_texto = input_descubierto.text().strip().replace(",", ".")

            if not descubierto_texto:
                descubierto_texto = "500"
            elif not es_descubierto_cuenta_valido(Decimal(descubierto_texto)):
                raise DescubiertoInvalidError("Descubierto inválido...")

            monto_descubierto = Decimal(descubierto_texto)

            num_cuenta: str = "".join(random.choices(string.digits, k=22))

            nueva_cuenta: CuentaCorriente = CuentaCorriente(num_cuenta, descubierto=monto_descubierto)
            cliente.agregar_cuenta(nueva_cuenta)

            logger.info(
                f"Cuenta Corriente agregada exitosamente desde la GUI: "
                f"Cuenta {num_cuenta} para Cliente DNI {cliente.get_dni()}"
            )

            guardar_datos(banco)

            QMessageBox.information(
                dialog, 
                "Éxito", 
                "¡Cuenta Corriente creada con éxito!"
            )

            dialog.accept()

        except DescubiertoInvalidError as e:
            logger.error(f"Error específico de descubierto, el descubierto no es válido: {e}")
            QMessageBox.warning(
                dialog, 
                "Aviso", 
                f"El descubierto es inválido: {e}"
            )

        except (ValueError, decimal.InvalidOperation) as e:
            logger.error(f"Error en la creacion de Cuenta Corriente desde la GUI [ValueError]: {e}")
            QMessageBox.critical(
                dialog, 
                "Error", 
                f"Error al crear la cuenta: {e}"
            )

        except Exception as e:
            logger.error(f"Error inesperado en la creacion de Cuenta Corriente desde la GUI: {e}")
            QMessageBox.critical(
                dialog, 
                "Error", 
                f"Ocurrió un error inesperado: {e}"
            )

    button_accept.clicked.connect(procesar_creacion)

    # Estilos:

    estilo_label = """
        QLabel {
            color: #F5F2EB;
            font-size: 16pt;
            font-weight: bold;
        }
    """

    estilo_input = """
        QLineEdit {
            background-color: #1a0b3c;
            color: #F5F2EB;
            border: 1px solid #5500CC;
            border-radius: 4px;
            padding: 6px;
            font-size: 12pt;
        }
    """

    estilo_boton = """
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

    label_instruccion.setStyleSheet(estilo_label)
    input_descubierto.setStyleSheet(estilo_input)
    button_accept.setStyleSheet(estilo_boton)

    dialog.resize(420, 140)
    layout.setContentsMargins(15, 15, 15, 15)
    layout.setSpacing(8)
    dialog.setStyleSheet("background-color: #0F0525;")

    dialog.exec()

def flujo_depositar_gui(
        banco: Banco | None = None, 
        cliente: Cliente | None = None, 
        v_padre: QWidget | None = None
) -> None: #pragma: no cover

    """
    Modulo encargado de ejecutar la accion de "Depositar en una cuenta, sea Corriente o de Ahorro, en la GUI"...
    """

    if not cliente or not banco: 
        return

    if cliente.cuentas:

        v_dialog = QDialog(v_padre)
        v_dialog.setWindowTitle("Seleccionar Cuenta")

        # Creamos el Layout del diálogo:
        layout = QVBoxLayout(v_dialog)

        # Creamos los Widgets necesarios:
        label_combo = QLabel("Seleccione la cuenta a depositar:", v_dialog)
        combo_box = QComboBox(v_dialog)

        label_monto = QLabel("Ingrese el monto (ej: 500.34):", v_dialog)
        input_monto = QLineEdit(v_dialog)

        button_accept = QPushButton("Aceptar", v_dialog)

        # Llenamos el combo box con las cuentas del cliente:
        for cuenta, tipo_ahorro in cliente.listar_cuentas_con_tipo():
            if tipo_ahorro: 
                texto_item = f"Cuenta de Ahorro — Nro: {cuenta.get_numero()} — Saldo: ${cuenta.get_saldo()}"
            else: 
                texto_item = f"Cuenta Corriente — Nro: {cuenta.get_numero()} — Saldo: ${cuenta.get_saldo()}"
        
            combo_box.addItem(texto_item, cuenta)

        # Sincronizamos los Widgets al Layout:
        layout.addWidget(label_combo)
        layout.addWidget(combo_box)
        
        layout.addSpacing(10)  # Espacio visual
        
        layout.addWidget(label_monto)
        layout.addWidget(input_monto)
        
        layout.addSpacing(15)  # Espacio antes del botón
        
        layout.addWidget(button_accept)

        def procesar_eleccion() -> None:
            try:
                cuenta_elegida: CuentaAhorro | CuentaCorriente = combo_box.currentData()
                if not cuenta_elegida: 
                    return

                numero_cuenta = cuenta_elegida.get_numero()

                texto_monto = input_monto.text().strip().replace(",", ".")
                if not texto_monto:
                    raise ValueError("El campo de monto está vacío.")

                monto_en_decimal = Decimal(texto_monto)

                cliente.depositar_en_cuenta(numero_cuenta, monto_en_decimal)

                QMessageBox.information(
                    v_dialog, 
                    "Éxito", 
                    "Depósito realizado con éxito."
                )

                logger.info(f"Depósito en CLI exitoso: Cuenta {numero_cuenta}, Monto ${monto_en_decimal}")

                guardar_datos(banco)
                v_dialog.accept()

            except (ValueError, decimal.InvalidOperation) as e:
                QMessageBox.critical(
                    v_dialog, 
                    "Error", 
                    f"Error: Monto inválido o problema en el depósito ({e})"
                )
                logger.error(f"Error de depósito en CLI [Monto/Valor]: {e}")

        # Conectamos el botón de aceptar:
        button_accept.clicked.connect(procesar_eleccion)

        # Estilos:

        # Estilo común para las etiquetas
        estilo_label = """
            QLabel {
                color: #F5F2EB;
                font-size: 16pt;
                font-weight: bold;
            }
        """

        # Estilo para el campo de texto (QLineEdit)
        estilo_input = """
            QLineEdit {
                background-color: #1a0b3c;
                color: #F5F2EB;
                border: 1px solid #5500CC;
                border-radius: 4px;
                padding: 6px;
                font-size: 12pt;
            }
        """

        # Estilo para el ComboBox (desplegable)
        estilo_combobox = """
            QComboBox {
                background-color: #1a0b3c;
                color: #F5F2EB;
                border: 1px solid #5500CC;
                border-radius: 4px;
                padding: 6px;
                font-size: 12pt;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #0F0525;
                color: #F5F2EB;
                selection-background-color: #6A00FF;
                selection-color: #F5F2EB;
                border: 1px solid #5500CC;
            }
        """

        # Estilo para el botón de aceptar
        estilo_boton = """
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

        # Aplicaciones de Estilos predefinidos:
        label_combo.setStyleSheet(estilo_label)
        label_monto.setStyleSheet(estilo_label)
        combo_box.setStyleSheet(estilo_combobox)
        input_monto.setStyleSheet(estilo_input)
        button_accept.setStyleSheet(estilo_boton)

        # Tamaños:
        v_dialog.resize(420, 260)  # Establece el tamaño de la ventana de diálogo

        # Margenes:
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos del diálogo

        # Colores de fondo:
        v_dialog.setStyleSheet("background-color: #0F0525;")  # Cambia el color de fondo del diálogo

        v_dialog.exec()

    else:
        QMessageBox.warning(
            v_padre, 
            "Advertencia", 
            "El cliente no posee cuentas asociadas para depositar."
        )
            
        logger.warning(f"Intento de depósito fallido en la GUI: Cliente {cliente.get_dni()} sin cuentas asociadas.")

def flujo_extraer_gui(
        banco: Banco | None = None, 
        cliente: Cliente | None = None, 
        v_padre: QWidget | None = None
) -> None: #pragma: no cover

    """
    Modulo encargado de ejecutar la accion de "Extraer un monto de alguna cuenta de algun Cliente, sea de Ahorro o Corriente, en la GUI"...
    """

    if not banco or not cliente: 
        return

    if cliente.cuentas:

        dialog = QDialog(v_padre)
        dialog.setWindowTitle("Seleccionar Cuenta")

        # Creamos el Layout del diálogo:
        layout = QVBoxLayout(dialog)

        # Creamos los Widgets necesarios:
        label_c_box = QLabel("Seleccione la cuenta a extraer:", dialog)
        c_box = QComboBox(dialog)

        label_monto = QLabel("Ingrese el monto a extraer (ej: 500.34):", dialog)
        input_monto = QLineEdit(dialog)

        button_accept = QPushButton("Aceptar", dialog)

        # Llenamos el combo box con las cuentas del cliente:
        for cuenta, tipo_ahorro in cliente.listar_cuentas_con_tipo():
            if tipo_ahorro: 
                texto_item = f"Cuenta de Ahorro — Nro: {cuenta.get_numero()} — Saldo: ${cuenta.get_saldo()}"
            else: 
                texto_item = f"Cuenta Corriente — Nro: {cuenta.get_numero()} — Saldo: ${cuenta.get_saldo()}"

            c_box.addItem(texto_item, cuenta)

        # Sincronizamos los Widgets al Layout:
        layout.addWidget(label_c_box)
        layout.addWidget(c_box)
        
        layout.addSpacing(10)  # Espacio visual
        
        layout.addWidget(label_monto)
        layout.addWidget(input_monto)
        
        layout.addSpacing(15)  # Espacio antes del botón
        
        layout.addWidget(button_accept)

        def procesar_eleccion() -> None:
            try:
                cuenta_seleccionada: CuentaAhorro | CuentaCorriente = c_box.currentData()
                if not cuenta_seleccionada: 
                    return
                numero_cuenta = cuenta_seleccionada.get_numero()

                monto_texto = input_monto.text().strip().replace(",", ".")
                if not monto_texto:
                    raise ValueError("El campo del monto está vacío.")
                monto = Decimal(monto_texto)

                cliente.extraer_de_cuenta(numero_cuenta, monto)

                QMessageBox.information(
                    dialog, 
                    "Éxito", 
                    "Extracción realizada con éxito."
                )

                logger.info(f"Extracción en CLI exitosa: Cuenta {numero_cuenta}, Monto ${monto}")

                guardar_datos(banco)
                dialog.accept()

            except (ValueError, decimal.InvalidOperation) as e:
                QMessageBox.critical(
                    dialog, 
                    "Error", 
                    f"Error: Monto inválido o problema en la extracción ({e})"
                )
                logger.error(f"Error de extracción en CLI [Monto/Valor]: {e}")

        # Conectamos el botón de aceptar:
        button_accept.clicked.connect(procesar_eleccion)

        # Estilos:

        # Estilo común para las etiquetas
        estilo_label = """
            QLabel {
                color: #F5F2EB;
                font-size: 16pt;
                font-weight: bold;
            }
        """

        # Estilo para el campo de texto (QLineEdit)
        estilo_input = """
            QLineEdit {
                background-color: #1a0b3c;
                color: #F5F2EB;
                border: 1px solid #5500CC;
                border-radius: 4px;
                padding: 6px;
                font-size: 12pt;
            }
        """

        # Estilo para el ComboBox (desplegable)
        estilo_combobox = """
            QComboBox {
                background-color: #1a0b3c;
                color: #F5F2EB;
                border: 1px solid #5500CC;
                border-radius: 4px;
                padding: 6px;
                font-size: 12pt;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #0F0525;
                color: #F5F2EB;
                selection-background-color: #6A00FF;
                selection-color: #F5F2EB;
                border: 1px solid #5500CC;
            }
        """

        # Estilo para el botón de aceptar
        estilo_boton = """
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

        # Aplicaciones de Estilos predefinidos:
        label_c_box.setStyleSheet(estilo_label)
        label_monto.setStyleSheet(estilo_label)
        c_box.setStyleSheet(estilo_combobox)
        input_monto.setStyleSheet(estilo_input)
        button_accept.setStyleSheet(estilo_boton)

        # Tamaños:
        dialog.resize(420, 260)  # Establece el tamaño de la ventana de diálogo

        # Margenes:
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos del diálogo

        # Colores de fondo:
        dialog.setStyleSheet("background-color: #0F0525;")  # Cambia el color de fondo del diálogo

        dialog.exec()

    else:
        QMessageBox.warning(
            v_padre, 
            "Advertencia", 
            "El cliente no posee cuentas asociadas para extraer."
        )
                    
        logger.warning(f"Intento de extracción fallido en la GUI: Cliente {cliente.get_dni()} sin cuentas asociadas.")

def flujo_seleccionar_cliente_gui(
        banco: Banco | None = None, 
        v_padre: QWidget | None = None
) -> Cliente | None: #pragma: no cover

    """
    Modulo encargado de ejecutar la accion de "Seleccionar un cliente para pasar a la vista de Gestion de Cliente, en la GUI"...
    """

    if not banco: return

    # Creo la miniventana para seleccionar el cliente:
    dialog = QDialog(v_padre)
    dialog.setWindowTitle("Seleccionar Cliente")

    # Creo el contenedor principal:
    layout = QVBoxLayout(dialog)

    # Creo los Widgets necesarios:
    label_seleccionar_cliente = QLabel("Selecciona el cliente: ", dialog)
    c_box_seleccionar_cliente = QComboBox(dialog)
    button_accept = QPushButton("Aceptar", dialog)

    # Sincronizamos los Widgets a su contenedor:
    layout.addWidget(label_seleccionar_cliente)
    layout.addWidget(c_box_seleccionar_cliente)
    
    # Espacio para separar el combo box del botón de aceptar
    layout.addSpacing(10)
    
    layout.addWidget(button_accept)

    # Llenamos el combo:
    for cliente in banco.clientes:
        text_item = f"Cliente: {cliente.get_nombre()} —— DNI: {cliente.get_dni()}"
        c_box_seleccionar_cliente.addItem(text_item, cliente)

    # Diccionario para mantener la referencia del cliente seleccionado tras cerrar el diálogo
    cliente_seleccionado: dict[str, Cliente | None] = {"cliente_seleccionado": None}

    def proceso_al_aceptar() -> None:
        # Recuperamos la elección del Combo:
        cliente_seleccionado["cliente_seleccionado"] = c_box_seleccionar_cliente.currentData()
        # Cerramos el dialogo:
        dialog.accept()

    # Conectamos el botón:
    button_accept.clicked.connect(proceso_al_aceptar)

    # Estilos:

    # Estilo para el ComboBox (desplegable)
    estilo_combobox = """
        QComboBox {
            background-color: #1a0b3c;
            color: #F5F2EB;
            border: 1px solid #5500CC;
            border-radius: 4px;
            padding: 6px;
            font-size: 12pt;
        }
        QComboBox::drop-down {
            border: 0px;
        }
        QComboBox QAbstractItemView {
            background-color: #0F0525;
            color: #F5F2EB;
            selection-background-color: #6A00FF;
            selection-color: #F5F2EB;
            border: 1px solid #5500CC;
        }
    """

    # Estilo para el botón de aceptar
    estilo_boton_aceptar = """
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

    # Aplicaciones de Estilos predefinidos:
    c_box_seleccionar_cliente.setStyleSheet(estilo_combobox)
    button_accept.setStyleSheet(estilo_boton_aceptar)

    # Tamaños:
    dialog.resize(380, 180)  # Establece el tamaño de la ventana de diálogo

    # Margenes:
    layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos del diálogo

    # Colores de fondo:
    dialog.setStyleSheet("background-color: #0F0525;")  # Cambia el color de fondo del diálogo

    # Estilo para la etiqueta (Label)
    label_seleccionar_cliente.setStyleSheet("color: #F5F2EB; font-size: 16pt; font-weight: bold;")

    # Lanzamos el dialogo y ponemos la app en espera:
    dialog.exec()

    return cliente_seleccionado["cliente_seleccionado"]

def flujo_mostrar_clientes_gui(
        banco: Banco | None = None, 
        v_padre: QWidget | None = None
) -> None: #pragma: no cover

    if not banco: 
        return

    dialog = QDialog(v_padre)
    dialog.setWindowTitle("Mostrar Clientes y Cuentas")

    # Creamos el Layout del diálogo:
    layout = QVBoxLayout(dialog)

    # Creamos los Widgets principales:
    label_titulo_clientes = QLabel("Seleccione un cliente para ver sus cuentas:", dialog)
    
    tabla_clientes = QTableWidget(len(banco.clientes), 2, dialog)
    tabla_clientes.setHorizontalHeaderLabels(["Nombre del Cliente", "DNI"])

    label_titulo_cuentas = QLabel("Cuentas del Cliente Seleccionado:", dialog)
    
    tabla_cuentas = QTableWidget(dialog)
    tabla_cuentas.setColumnCount(3)
    tabla_cuentas.setHorizontalHeaderLabels(["Tipo de Cuenta", "Número de Cuenta", "Saldo / Detalles"])

    button_cerrar = QPushButton("Cerrar", dialog)

    # Sincronizamos los Widgets al Layout:
    layout.addWidget(label_titulo_clientes)
    layout.addWidget(tabla_clientes)
    
    layout.addSpacing(10)  # Espacio visual entre tablas
    
    layout.addWidget(label_titulo_cuentas)
    layout.addWidget(tabla_cuentas)
    
    layout.addSpacing(10)  # Espacio antes del botón
    
    layout.addWidget(button_cerrar)

    # Configuraciones de las tablas:
    tabla_clientes.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    tabla_clientes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    tabla_clientes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    tabla_clientes.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    tabla_cuentas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla_cuentas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    tabla_cuentas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    # Llenamos la tabla de clientes:
    for fila, cliente in enumerate(banco.clientes):
        item_nombre = QTableWidgetItem(cliente.get_nombre())
        item_dni = QTableWidgetItem(cliente.get_dni())

        item_nombre.setData(Qt.ItemDataRole.UserRole, cliente)

        tabla_clientes.setItem(fila, 0, item_nombre)
        tabla_clientes.setItem(fila, 1, item_dni)

    def actualizar_tabla_cuentas() -> None:
        items_seleccionados = tabla_clientes.selectedItems()
        if not items_seleccionados: 
            return

        item_nombre = items_seleccionados[0]
        cliente_elegido: Cliente = item_nombre.data(Qt.ItemDataRole.UserRole)

        if not cliente_elegido or not cliente_elegido.cuentas:
            tabla_cuentas.setRowCount(0)
            return

        tabla_cuentas.setRowCount(len(cliente_elegido.cuentas))
        for fila_c, (cuenta, tipo_ahorro) in enumerate(cliente_elegido.listar_cuentas_con_tipo()):
            tipo_str = "Cuenta de Ahorro" if tipo_ahorro else "Cuenta Corriente"
            nro_str = str(cuenta.get_numero())
            saldo_str = f"${cuenta.get_saldo()}"
            if isinstance(cuenta, CuentaCorriente):
                saldo_str += f" (Descubierto: ${cuenta.get_descubierto()})"

            tabla_cuentas.setItem(fila_c, 0, QTableWidgetItem(tipo_str))
            tabla_cuentas.setItem(fila_c, 1, QTableWidgetItem(nro_str))
            tabla_cuentas.setItem(fila_c, 2, QTableWidgetItem(saldo_str))

    # Conexiones de la tabla y botón:
    tabla_clientes.itemSelectionChanged.connect(actualizar_tabla_cuentas)
    button_cerrar.clicked.connect(dialog.accept)

    # Estilos:

    # Estilo común para las etiquetas
    estilo_label = """
        QLabel {
            color: #F5F2EB;
            font-size: 16pt;
            font-weight: bold;
        }
    """

    # Estilo general para las tablas (QTableWidget) y sus cabeceras
    estilo_tabla = """
        QTableWidget {
            background-color: #1a0b3c;
            color: #F5F2EB;
            gridline-color: #5500CC;
            border: 1px solid #5500CC;
            border-radius: 6px;
            font-size: 12pt;
        }
        QTableWidget::item {
            padding: 6px;
        }
        QTableWidget::item:selected {
            background-color: #6A00FF;
            color: #F5F2EB;
        }
        QHeaderView::section {
            background-color: #0F0525;
            color: #F5F2EB;
            padding: 6px;
            border: 1px solid #5500CC;
            font-weight: bold;
            font-size: 12pt;
        }
    """

    # Estilo para el botón de cerrar
    estilo_boton_cerrar = """
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

    # Aplicaciones de Estilos predefinidos:
    label_titulo_clientes.setStyleSheet(estilo_label)
    label_titulo_cuentas.setStyleSheet(estilo_label)
    tabla_clientes.setStyleSheet(estilo_tabla)
    tabla_cuentas.setStyleSheet(estilo_tabla)
    button_cerrar.setStyleSheet(estilo_boton_cerrar)

    # Tamaños:
    dialog.resize(700, 520)  # Establece el tamaño de la ventana de diálogo

    # Margenes:
    layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos del diálogo

    # Colores de fondo:
    dialog.setStyleSheet("background-color: #0F0525;")  # Cambia el color de fondo del diálogo

    dialog.exec()

def flujo_dar_alta_cliente_gui(
        banco: Banco | None = None, 
        v_padre: QWidget | None = None
) -> None: #pragma: no cover

    if not banco: return

    dialog = QDialog(v_padre)
    dialog.setWindowTitle("Dar alta a Cliente")

    # Creamos el Layout del diálogo:
    layout = QVBoxLayout(dialog)

    # Creamos los Widgets principales:
    label_nombre_cliente = QLabel("Nombre Cliente: ", dialog)
    l_edit_nombre_cliente = QLineEdit(dialog)

    label_dni_cliente = QLabel("DNI: ", dialog)
    l_edit_dni_cliente = QLineEdit(dialog)

    button_accept = QPushButton("Aceptar", dialog)

    # Sincronizamos los Widgets al Layout:
    layout.addWidget(label_nombre_cliente)
    layout.addWidget(l_edit_nombre_cliente)
    layout.addWidget(label_dni_cliente)  
    layout.addWidget(l_edit_dni_cliente)
    layout.addWidget(button_accept)

    def procesar_alta() -> None:
        try: 
            nombre_cliente = l_edit_nombre_cliente.text().strip()
            dni_normalizado = l_edit_dni_cliente.text().strip().replace(".", "")
            
            if not nombre_cliente or not dni_normalizado:
                raise ValueError("Los campos no pueden estar vacíos.")

            banco.alta_cliente(nombre_cliente, dni_normalizado)

            QMessageBox.information(
                dialog, 
                "Alta Exitosa", 
                "Alta al cliente exitosa"
            )
            logger.info(f"Alta de cliente procesada desde la GUI con éxito: DNI {dni_normalizado}")

            guardar_datos(banco)
            dialog.accept()  # Cerramos el diálogo solo cuando todo salió bien

        except ValueError as e:
            QMessageBox.critical(
                dialog, 
                "Alta Fallida", 
                f"Error al dar de alta: {e}"
            )
            logger.error(f"Fallo en alta de cliente desde la GUI [ValueError]: {e}")

        except Exception as e:
            QMessageBox.critical(
                dialog, 
                "Alta Fallida", 
                f"Ocurrió un error inesperado: {e}"
            )
            logger.error(f"Error inesperado en alta de cliente desde la GUI: {e}")

    # Conexiones de botones a acciones:
    button_accept.clicked.connect(procesar_alta)

    # Estilos:

    # Estilo común para los campos de texto
    estilo_input = """
        QLineEdit {
            background-color: #F5F2EB;
            color: #000000;
            border: 1px solid #5500CC;
            border-radius: 4px;
            padding: 7px;
            font-size: 12pt;
        }
    """

    # Estilo para el botón de aceptar
    estilo_boton_aceptar = """
        QPushButton {
            background-color: #6A00FF;
            color: #F5F2EB;
            font-size: 12pt;
            font-weight: bold;
            border-radius: 5px;
            padding: 8px;
            margin-bottom: 10px;
        }
        QPushButton:hover {
            background-color: #5500CC;
        }
    """

    # Aplicaciones de Estilos predefinidos:
    l_edit_nombre_cliente.setStyleSheet(estilo_input)
    l_edit_dni_cliente.setStyleSheet(estilo_input)
    button_accept.setStyleSheet(estilo_boton_aceptar)

    # Tamaños:
    dialog.resize(350, 220)  # Establece el tamaño de la ventana de diálogo

    # Margenes:
    layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos del diálogo

    # Colores de fondo:
    dialog.setStyleSheet("background-color: #0F0525;")  # Cambia el color de fondo del diálogo

    # Colores de texto para las etiquetas (Labels)
    estilo_label = "color: #F5F2EB; font-size: 13pt; font-weight: bold;"
    label_nombre_cliente.setStyleSheet(estilo_label)
    label_dni_cliente.setStyleSheet(estilo_label)

    dialog.exec()

def flujo_resumen_banco_gui(
        banco: Banco | None = None, 
        v_padre: QWidget | None = None
) -> None: #pragma: no cover

    if not banco: 
        return

    dialog = QDialog(v_padre)
    dialog.setWindowTitle("Resumen General del Banco")

    # Creamos el Layout del diálogo:
    layout = QVBoxLayout(dialog)

    # Creamos los Widgets principales:
    label_titulo = QLabel("📊 Panel de Estadísticas del Banco", dialog)

    # --- CALCULAMOS LAS MÉTRICAS ---
    total_clientes = len(banco.clientes)
    
    total_cuentas = 0
    total_ahorro = 0
    total_corriente = 0
    monto_total_dinero = Decimal("0.00")

    for cliente in banco.clientes:
        for cuenta, tipo_ahorro in cliente.listar_cuentas_con_tipo():
            total_cuentas += 1
            monto_total_dinero += cuenta.get_saldo()
            if tipo_ahorro:
                total_ahorro += 1
            else:
                total_corriente += 1

    # Creamos las "tarjetas" como etiquetas informativas:
    label_clientes = QLabel(f"Total de Clientes Registrados: {total_clientes}", dialog)
    label_cuentas = QLabel(f"Total de Cuentas Activas: {total_cuentas}", dialog)
    label_ahorro = QLabel(f"  • Cuentas de Ahorro: {total_ahorro}", dialog)
    label_corriente = QLabel(f"  • Cuentas Corrientes: {total_corriente}", dialog)
    label_capital = QLabel(f"Capital Total en Depósitos: ${monto_total_dinero:.2f}", dialog)

    button_cerrar = QPushButton("Cerrar", dialog)

    # Sincronizamos los Widgets al Layout:
    layout.addWidget(label_titulo)
    layout.addWidget(label_clientes)
    layout.addWidget(label_cuentas)
    layout.addWidget(label_ahorro)
    layout.addWidget(label_corriente)
    layout.addWidget(label_capital)
    
    layout.addStretch()  # Empuja el contenido hacia arriba y deja aire abajo
    
    layout.addWidget(button_cerrar)

    # Conexiones de botones a acciones:
    button_cerrar.clicked.connect(dialog.accept)

    # Estilos:

    # Estilo para el título principal
    label_titulo.setStyleSheet("""
        color: #F5F2EB;
        font-size: 20pt;
        font-weight: bold;
        margin-bottom: 14px;
    """)

    # Estilo tipo "tarjeta" para las métricas de estadísticas
    estilo_tarjeta = """
        QLabel {
            background-color: #1a0b3c;
            color: #F5F2EB;
            border: 1px solid #5500CC;
            border-radius: 6px;
            padding: 10px;
            font-size: 12pt;
            margin-bottom: 4px;
        }
    """

    # Estilo para el botón de cerrar
    estilo_boton_cerrar = """
        QPushButton {
            background-color: #6A00FF;
            color: #F5F2EB;
            font-size: 12pt;
            font-weight: bold;
            border-radius: 5px;
            padding: 8px;
            margin-top: 10px;
        }
        QPushButton:hover {
            background-color: #5500CC;
        }
    """

    # Aplicaciones de Estilos predefinidos:
    label_clientes.setStyleSheet(estilo_tarjeta)
    label_cuentas.setStyleSheet(estilo_tarjeta)
    label_ahorro.setStyleSheet(estilo_tarjeta)
    label_corriente.setStyleSheet(estilo_tarjeta)
    label_capital.setStyleSheet(estilo_tarjeta)
    button_cerrar.setStyleSheet(estilo_boton_cerrar)

    # Alineaciones:
    label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Tamaños:
    dialog.resize(420, 420)  # Establece el tamaño de la ventana de diálogo

    # Margenes:
    layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos del diálogo

    # Colores de fondo:
    dialog.setStyleSheet("background-color: #0F0525;")  # Cambia el color de fondo del diálogo

    dialog.exec()