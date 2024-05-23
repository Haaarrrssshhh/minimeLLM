# mainllm/singleton.py
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class EmbeddingManager:
    _instance = None

    def __init__(self):
        if EmbeddingManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            EmbeddingManager._instance = self
            self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
            self.chroma_client = chromadb.Client(Settings())
            self.collection = self.chroma_client.create_collection(name="embeddings")

    @staticmethod
    def get_instance():
        if EmbeddingManager._instance is None:
            EmbeddingManager()
        return EmbeddingManager._instance

    def add_embeddings(self, embeddings, paragraphs):
        for idx, embedding in enumerate(embeddings):
            self.collection.add(
                embeddings=[embedding.tolist()],
                metadatas=[{"paragraph": paragraphs[idx]}],
                ids=[str(idx)]
            )

    def query_embedding(self, query_embedding):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        return results
