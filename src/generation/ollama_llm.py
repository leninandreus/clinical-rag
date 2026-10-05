
#----conectar modelo local ollama
import ollama


from config.settings import LLM_CONFIGS, MAX_TOKENS, TEMPERATURE
from src.generation.base_llm import BaseLLm

class OllamaLLm(BaseLLm):

#----inicializar el cliente de ollama
    def __init__(self):
        self.model_name = LLM_CONFIGS["ollama"]["model"]
        

#----enviar el prompt al modelo
    def generate(self, prompt: str) -> str:
        respuesta = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                "num_predict": MAX_TOKENS,
                "temperature": TEMPERATURE,
            }
        
        )
        return respuesta["response"]

#----devolver el proveedor y modelo utilizado
    @property
    def name(self) -> str:
        return f"ollama/{self.model_name}"
    

  