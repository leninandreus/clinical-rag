#----define la estrcutura que deben respetar todos los modelos que se conectarán.
from abc import ABC, abstractclassmethod

class BaseLLm(ABC):
#----método para generar una respuesta
    @abstractclassmethod
    def generate(self,prompt:str) -> str:
        pass
#----devolver el nombre del proveedor y modelo que se usa
    @property
    @abstractclassmethod
    def name(self) -> str:
        pass