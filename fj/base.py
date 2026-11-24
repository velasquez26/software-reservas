
from abc import ABC, abstractmethod
from datetime import datetime


class EntidadFJ(ABC):
 

    PREFIJO = "ENT"          # cada subclase define el suyo
    _consecutivos: dict = {}  # contador compartido, uno por prefijo

    def __init__(self) -> None:
       
        numero = EntidadFJ._consecutivos.get(self.PREFIJO, 0) + 1
        EntidadFJ._consecutivos[self.PREFIJO] = numero
        self._codigo = f"{self.PREFIJO}-{numero:03d}"
        self._creada_en = datetime.now()

    @property
    def codigo(self) -> str:
     
        return self._codigo

    @abstractmethod
    def resumen(self) -> str:
        
    def __str__(self) -> str:
    
        return self.resumen()
