# mainllm/signals.py
import csv
import chromadb
from sentence_transformers import SentenceTransformer
import os
from django.conf import settings
from chromadb.utils import embedding_functions

def generateVectorDatabase():
    # Initialize ChromaDB HTTP client
    chroma_client = chromadb.PersistentClient(path="my_vectordb")
    # Define global variables
    global collection
    collection = embedding_model = "all-mpnet-base-v2"
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=embedding_model)

    try:
        print("TRY")
        print(chroma_client.list_collections())
        collection = chroma_client.get_collection(
            name="my_collection", embedding_function=sentence_transformer_ef)
        print(collection)
    except:

        with open('Train.csv') as file:
            lines = csv.reader(file)

            # Store the name of the menu items in this array. In Chroma, a "document" is a string i.e. name, sentence, paragraph, etc.
            documents = []

            # Store the corresponding menu item IDs in this array.
            metadatas = []

            # Each "document" needs a unique ID. This is like the primary key of a relational database. We'll start at 1 and increment from there.
            ids = []
            id = 1

            # Loop thru each line and populate the 3 arrays.
            for i, line in enumerate(lines):
                if i == 0:
                    # Skip the first row (the column headers)
                    continue

                documents.append(line[1])
                metadatas.append({"item_id": line[0]})
                ids.append(str(id))
                id += 1

        # Select the embedding model to use.
        # List of model names can be found here https://www.sbert.net/docs/pretrained_models.html
        # embedding_model = "all-MiniLM-L6-v2"

        # Create the collection, aka vector database. Or, if database already exist, then use it. Specify the model that we want to use to do the embedding.
        collection = chroma_client.get_or_create_collection(
            name="my_collection", embedding_function=sentence_transformer_ef)

        # Add all the data to the vector database. ChromaDB automatically converts and stores the text as vector embeddings. This may take a few minutes.
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
