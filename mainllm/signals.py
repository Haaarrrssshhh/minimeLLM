# mainllm/signals.py
import os
from django.conf import settings
from .singleton import EmbeddingManager
import openai

def initialize_embeddings():
    # Initialize OpenAI API
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Step 1: Load and preprocess the text file
    def preprocess_text(file_path):
        try:
            print(f"Attempting to read file at: {file_path}")  # Debug statement
            with open(file_path, 'r') as file:
                text = file.read()
            print("File read successfully")  # Debug statement
            # Segment the text into paragraphs
            paragraphs = text.split('\n\n')
            # print(paragraphs, "Loaded paragraphs")  # Debug statement
            return paragraphs
        except Exception as e:
            print(f"Error reading file: {e}")  # Debug statement
            return []

    # Resolve the file path
    file_path = os.path.join(settings.BASE_DIR, 'HarshInfo.txt')
    print(f"Resolved file path: {file_path}")  # Debug statement

    # Load the text data
    paragraphs = preprocess_text(file_path)
    if not paragraphs:
        print("No paragraphs loaded, skipping embedding creation.")  # Debug statement
        return

    # Step 2: Create embeddings using Sentence-BERT
    embedding_manager = EmbeddingManager.get_instance()
    embeddings = embedding_manager.model.encode(paragraphs)
    # print(embeddings, "Generated embeddings")  # Debug statement

    # Step 3: Add embeddings to ChromaDB
    embedding_manager.add_embeddings(embeddings, paragraphs)
    print("Embeddings added to ChromaDB.")
