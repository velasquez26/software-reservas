
import logging
from pathlib import Path

RUTA_BITACORA = Path(__file__).resolve().parent.parent / "logs" / "bitacora_fj.log"


def _crear_bitacora() -> logging.Logger:
   
    registro = logging.getLogger("software_fj")
    if not registro.handlers:
        RUTA_BITACORA.parent.mkdir(parents=True, exist_ok=True)
        registro.setLevel(logging.INFO)
        archivo = logging.FileHandler(RUTA_BITACORA, mode="w", encoding="utf-8")
        archivo.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s :: %(message)s"))
        registro.addHandler(archivo)
    return registro


bitacora = _crear_bitacora()
