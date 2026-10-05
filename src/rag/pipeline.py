#---- unir el retrieval con los LLMs

from src.retrieval.vector_store import VectorStore
from src.generation.base_llm import BaseLLm
from config.settings import TOP_K


#-----promp que enviamos al LLM indicando al modelo como debe utilizar la información recuperada desde ChromaDB

PROMPT_TEMPLATE  = """Eres un experto de información sobre medicamentos. Responde las preguntas
de los usuarios usando únicamente la información del conexto proporcionado .
Reglas:
1. Si la información no está en el contexto, responde "No tengo información suficiente para responder esa pregunta."
2. No inventes datos que no estén en el contexto
3. Cita el nombre del medicmaneto en el que basas tu respuesta.
4. Responde en español, de forma clara y concisa.
5. No realices diagnósticos ni indiques tratamientos personalizados
6.  El contexto puede estar escrito en inglés. Debes comprender esa información y responder completamente en español.

Contexto: {contexto}
Pregunta: {pregunta}
Respuesta: """

#----el 6 del prompt le añadi para ver si funciona el ollama


class RAGPipeline:

#----inicializamos el pipeline
    def __init__(self, llm:BaseLLm, vector_store:VectorStore | None=None):
        self.llm = llm
        self.vector_store = vector_store or VectorStore()
#----método para responder las preguntas, primero recuperamos la información y después utilizamos el LLm para generar la respuesta
    def answer(self, pregunta:str, top_k: int = TOP_K) -> dict:

        resultados = self.vector_store.search(pregunta, top_k=top_k)
        contexto = "\n\n".join(r["document"] for r in resultados)

        prompt = PROMPT_TEMPLATE.format(contexto=contexto,pregunta=pregunta)

        respuesta = self.llm.generate(prompt)
        return {
            "pregunta":pregunta,
            "respuesta": respuesta,
            "fuentes": [r["metadata"]["name"] for r in resultados],
            "modelo": self.llm.name,
        }

        