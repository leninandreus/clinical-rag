#--------generación de embeddings
#--------convertimos los textos en vectores numéricos para comparar


from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODELO

class Embedder:

#--------se carga el modelo de embeddings una sola vez
    def __init__(self, model_name:str = EMBEDDING_MODELO):
        self.model = SentenceTransformer(model_name)

#--------recibir varios textos y generar un embedding para cada uno
    def embed(self,texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts,show_progress_bar=False,normalize_embeddings=True)
        return embeddings.tolist()

#--------genera el embedding de un solo texto
    def embed_one(self, text: str) -> list[float]:
        return self.model.encode(
            text,
            normalize_embeddings=True
        ).tolist()
