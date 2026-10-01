#--------------Configuración central del rpoyecto---------
from pathlib import Path

#-------rutas----------
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT/ "data"
VECTORSTORE_DIR = ROOT / "data" / "vectorstore"

#---------dataset de medicamentos descargado de kaggle
#https://www.kaggle.com/datasets/shudhanshusingh/250k-medicines-usage-side-effects-and-substitutes?resource=download
DATASET_PATH = DATA_DIR / "medicines.csv"

#--------Embeddings---------
# EMBEDDING_MODELO = "all-MiniLM-L6-v2"
EMBEDDING_MODELO = "paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "medicines"

#documentos a recuperar por consulta
TOP_K = 4

#---------LLMs a comparar

LLM_CONFIGS = {
    "groq":     {"model": "openai/gpt-oss-120b"},
    "gemini":   {"model": "gemini-2.0-flash"},
    "ollama":   {"model": "llama3.2:3b"},
}

#------Generación
MAX_TOKENS = 512
TEMPERATURE = 0.1  #asegurarnos que las repsuestas sean fundamentadas

#-------Reproducibilidad
RANDOM_STATE = 42