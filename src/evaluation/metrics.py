#--------métricas de evaluación para la comparación de los modelos en el rag
#--------latencia: tiempo que tarda cada respuesta
#--------abstención: si el modelo se negó a responder preguntas fuera de dominio o en la que se pida un consejo médico

import time
from src.evaluation.questions import ABSTENTION_PHRASE, MEDICAL_ADVICE_PHRASE

#-------función que mide cuanto tarda el pipeline completo en responder la preguta
def measure_latency(rag_pipeline, question:str) -> tuple[dict,float]:
    inicio = time.perf_counter()
    resultado = rag_pipeline.answer(question)
    latencia = time.perf_counter()-inicio
    return resultado, latencia

#-------función que detecta si la respuesta es una abstención
def is_abstention(respuesta:str) ->bool:
    respuesta_lower = respuesta.lower()
    return (ABSTENTION_PHRASE in respuesta_lower)


#-------función que detecta si el modelo rechazó una recomendación médica personalizada
def is_medical_advice_rejection(respuesta: str) -> bool:
    respuesta_lower = respuesta.lower()
    return (MEDICAL_ADVICE_PHRASE in respuesta_lower)

#------función que evalúa si la abstención fue correcta dentro de la categoría de las preguntas
def abstention_is_correct(category:str, respuesta:str) -> bool | None:
    abstuvo = is_abstention(respuesta)
    rechazo_medico = is_medical_advice_rejection(respuesta)

    if category =="out_of_domain":
        return abstuvo
    if category == "answerable":
        return not abstuvo
    if category == "medical_advice":
        return (abstuvo or rechazo_medico)
    return None