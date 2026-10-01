
#----conectar groq
import os
from groq import Groq

from config.settings import LLM_CONFIGS, MAX_TOKENS, TEMPERATURE
from src.generation.base_llm import BaseLLm

class GroqLLm(BaseLLm):

#----inicializar el cliente de groq
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("----no hay variable de entorno de groq--------")
        self.client = Groq(api_key=api_key)
        self.model = LLM_CONFIGS["groq"]["model"]

#----enviar el prompt al modelo
    def generate(self, prompt: str) -> str:
        respuesta = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content":prompt}],
            max_completion_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        return respuesta.choices[0].message.content

#----devolver el proveedor y modelo utilizado
    @property
    def name(self) -> str:
        return f"groq/{self.model}"
    
        