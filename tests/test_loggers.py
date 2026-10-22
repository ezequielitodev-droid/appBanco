# Archivo para probar la configuración de logs:

import logging
import pytest
from logs.loggers import configurar_logging

def test_configurar_logging(tmp_path, monkeypatch) -> None:

    """
        Prueba que la función `configurar_logging` configure correctamente los manejadores
        de archivos (`FileHandler`), creando el archivo de registro en disco y escribiendo
        exitosamente los mensajes de log con su respectivo nivel de severidad.

        Args:
            tmp_path: Fixture de pytest que provee un directorio temporal aislado.
            monkeypatch: Fixture de pytest para modificar temporalmente el directorio de trabajo.

        Returns:
            None

        Examples:
            >>> # test_configurar_logging(tmp_path, monkeypatch)
    """
    
    # 1. Cambiamos temporalmente el directorio de trabajo a una carpeta temporal 
    # para que "app.log" se cree ahí y no ensucie el proyecto.
    monkeypatch.chdir(tmp_path)
    
    # Limpiamos los handlers existentes del root logger para evitar duplicados en el test
    raiz = logging.getLogger()
    for h in raiz.handlers[:]:
        raiz.removeHandler(h)
        
    # 2. Ejecutamos la función a probar
    configurar_logging()
    
    # 3. Verificamos que se haya agregado al menos un handler de tipo FileHandler
    handlers_archivo = [h for h in raiz.handlers if isinstance(h, logging.FileHandler)]
    assert len(handlers_archivo) > 0
    
    # 4. Probamos escribiendo un log real para ver si impacta en el archivo
    logger_prueba = logging.getLogger("test_modulo")
    logger_prueba.info("Mensaje de prueba para el log")
    
    # Forzamos el cierre o flush de los handlers para asegurarnos de que se escriba en disco
    for h in raiz.handlers:
        h.flush()
        
    # 5. Comprobamos que el archivo app.log se creó y contiene el mensaje
    archivo_log = tmp_path / "app.log"
    assert archivo_log.exists()
    
    contenido = archivo_log.read_text(encoding="utf-8")
    assert "Mensaje de prueba para el log" in contenido
    assert "INFO" in contenido