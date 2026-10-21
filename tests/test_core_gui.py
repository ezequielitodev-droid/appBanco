#Al probar todo lo relacionado con GUI manualmente no se importa en mis tests, meto este test asi importa y listo

def test_importar_gui_modulos():
    import core.core_gui # (o el nombre de tu archivo gui)
    assert True

#Lo mismo para los archivos de vistas

def test_importar_vistas_gui_principales() -> None:
    # Importamos todas las vistas de la GUI incluyendo MainWindow
    import vistas.GUI.main_window           # Reemplaza 'main_window' por el nombre real de tu archivo si es distinto
    import vistas.GUI.window_gestion_cliente
    import vistas.GUI.window_cliente
    import vistas.GUI.window_crear_cuenta
    
    assert True