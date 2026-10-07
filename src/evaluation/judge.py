#-----Uso de un LLM para evaluar la calidad de las respuestas del RAG

import re
from src.generation.base_llm import BaseLLm

#-----promp que enviamos al LLM judge

JUDGE_PROMPT = """Eres un evaluador experto de sistemas de preguntas y respuestas sobre medicamentos.
Evalúa la respuesta de un asistente según el contexto y la pregunta.

Califica dos criterios en una escala de 1 a 5:
-FIDELIDAD: ¿La respuesta se basa únicamente en el contexto, sin inventar información? (5= todo está respaldado por el contexto; 
1= inventa datos que no están)

-RELEVANCIA: ¿La respuesta contesta realmente lo que se preguntó? (5= responde con precisión; 
1= no responde la pregunta)

PREGUNTA:
{pregunta}

CONTEXTO:
{pregunta}

RESPUESTA A EVALUAR:
{respuesta}

Responde solo en este formato exacto, sin texto adicional:
FIDELIDAD: <número>
RELEVANCIA: <número>"""


def _parse_score(texto:str, etiqueta:str) -> int | None:
    
    patron = rf"{etiqueta}:\s*([1-5])"
    match = re.search(patron, texto, re.IGNORECASE)
    
    return int(match.group(1)) if match else None

def judge_answer(judge_llm:BaseLLm, pregunta:str, contexto:str, respuesta:str) -> dict:
    prompt = JUDGE_PROMPT.format(pregunta=pregunta, contexto=contexto, respuesta=respuesta)
    veredicto = judge_llm.generate(prompt)
    return{
        "fidelidad": _parse_score(veredicto, "FIDELIDAD"),
        "relevancia": _parse_score(veredicto, "RELEVANCIA"),
    }