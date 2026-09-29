#-----------base vectorial
#-----------se almacena los documentos y sus embeddings en chroma db
#-----------para despues realizar búsquedas semánticas
import chromadb
from config.settings import VECTORSTORE_DIR, COLLECTION_NAME, TOP_K
from src.retrieval.embedder import Embedder

class VectorStore:

#-----------inicializamos el modelo de embeddings y la base vectorial
    def __init__(self, embedder: Embedder | None = None):
        self.embedder = embedder or Embedder()
        VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(VECTORSTORE_DIR))
        #---------se añade la distancia cosine
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})  

#-----------se indexa los documentos dentro de ChromaDB
    def index(self, ids: list[str], documents:list[str],
              metadatas: list[dict], batch_size: int=500):   
        total = len(documents)
        for i in range(0, total, batch_size):
            fin = min(i+batch_size,total)
            lote_docs = documents[i:fin]
            embeddings = self.embedder.embed(lote_docs)
            self.collection.add(
                ids=ids[i:fin],
                documents=lote_docs,
                embeddings=embeddings,
                metadatas=metadatas[i:fin],
            )
        return self.collection.count()

    

#------------se realiza ua búsqueda semántica
    def search(self, query:str, top_k:int = TOP_K) -> list[dict]:

        query_embedding = self.embedder.embed_one(query)
        resultados = self.collection.query(
            query_embeddings=[query_embedding],
            n_results= top_k,
        )
        salida = []
        for doc, meta, dist in zip(
            resultados["documents"][0],
            resultados["metadatas"][0],
            resultados["distances"][0],
        ):
            salida.append({"document":doc,"metadata":meta, "distance":dist})
        return salida


#-------------devuelve la cantidad de documentos almacenados en ChormaDB
    def count(self) -> int:
        return self.collection.count()