#--------Ingestión de datos
#-------cargamos el dataset y convertimos cada fila en un documento de texto coherente
#-------que luego lo utilizamos dentro del RAG

import pandas as pd
from config.settings import DATASET_PATH

#-----------prefijos que tienen varias columnas dento del dataset
SIDE_EFFECT_PREFIX = "sideEffect"
SUBSTITUTE_PREFIX = "substitute"
USE_PREFIX = "use"


#---------busca todas las columnas que comienzan con un prefijo
#---------y guarda únicamente los valores que tienen información
def _collect(row: pd.Series, prefix:str) -> list[str]:
    valores = []
    for col in row.index:
        if col.startswith(prefix):
            v = row[col]
            if pd.notna(v) and str(v).strip() and str(v).strip().upper() != "NA":
                valores.append(str(v).strip())

    return valores


#-------limpiar valores individuales del dataset
#-------si está vacío o contiene NA devolvemos cadenas vacía
def _clean(value) -> str:
    if pd.isna(value) or str(value).strip().upper() == "NA":
        return ""
    return str(value).strip()



#-----carga el archivo de medicinas y organiza solo la información que vamos a usar en el RAG
def load_medicines(path= DATASET_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    registros = []
    for _, row in df.iterrows():
        registros.append({
            "id": row.get("id"),
            "name": str(row["name"]).strip(),
            "uses": _collect(row, USE_PREFIX),
            "side_effects": _collect(row,SIDE_EFFECT_PREFIX),
            "substitutes": _collect(row, SUBSTITUTE_PREFIX),
            "chemical_class": _clean(row.get("Chemical Class")),
            "therapeutic_class": _clean(row.get("Therapeutic Class")),
            "action_class": _clean(row.get("Action Class")),
            "habit_forming": _clean(row.get("Habit Forming")),
        })
    return pd.DataFrame(registros)



#--------convierte la información de cada medicamento en un texto continuo
def build_document(med: dict) -> str:

    partes = [f"Medicamento: {med['name']}."]

    if med["uses"]:
        partes.append("Usos: " + "; ".join(med["uses"]) + ".")

    if med["side_effects"]:
        partes.append("Efectos secundarios: " + "; ".join(med["side_effects"]) + ".")

    if med["therapeutic_class"]:
            partes.append(f"Clase terapéutica: {med['therapeutic_class']}.") 

    if med["chemical_class"]:
                partes.append(f"Clase química: {med['chemical_class']}.") 

    if med["action_class"]:
                partes.append(f"Clase de acción: {med['action_class']}.") 

    if med["substitutes"]:
            partes.append("Sustitutos: " + "; ".join(med["substitutes"]) + ".")

    return " ".join(partes)


#--------contrucción del corpus que vamos a utilizar en el RAG
def build_corpus(path=DATASET_PATH) ->pd.DataFrame:

      df= load_medicines(path)
      df["document"] = df.apply(lambda r: build_document(r.to_dict()), axis=1)
      return df