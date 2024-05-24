import csv
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions

# Module-level variables
chroma_client = None
collection = None

def chromadbclient():
    global chroma_client, collection
    chroma_client = chromadb.PersistentClient(path="my_vectordb")
    embedding_model = "all-mpnet-base-v2"
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model)

    try:
        print("TRY")
        print(chroma_client.list_collections())
        collection = chroma_client.get_collection(name="my_collection", embedding_function=sentence_transformer_ef)
        print(collection, "collection")
    except Exception as e:
        print(f"Exception: {e}")
        with open('HarshInfo.csv') as file:
            lines = csv.reader(file)
            documents = []
            metadatas = []
            ids = []
            id = 1
            for i, line in enumerate(lines):
                if i == 0:
                    continue
                documents.append(line[1])
                metadatas.append({"item_id": line[0]})
                ids.append(str(id))
                id += 1
        
        collection = chroma_client.get_or_create_collection(
            name="my_collection", embedding_function=sentence_transformer_ef)

        collection.add(documents=documents, metadatas=metadatas, ids=ids)

def get_collection():
    global collection
    if collection is None:
        raise Exception("ChromaDB client is not initialized. Call 'chromadbclient' first.")
    return collection
