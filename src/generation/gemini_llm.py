
#----conectar gemini
import os
import google.genai as genai
from google.genai import types


from config.settings import LLM_CONFIGS, MAX_TOKENS, TEMPERATURE
from src.generation.base_llm import BaseLLm

class GeminiLLm(BaseLLm):

#----inicializar el cliente de groq
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("----no hay variable de entorno de Gemini--------")
        self.client = genai.Client(api_key=api_key)
        self.model_name = LLM_CONFIGS["gemini"]["model"]
        

#----enviar el prompt al modelo
    def generate(self, prompt: str) -> str:
        respuesta = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                        ),
        )
        return respuesta.text

#----devolver el proveedor y modelo utilizado
    @property
    def name(self) -> str:
        return f"gemini/{self.model_name}"
    

  