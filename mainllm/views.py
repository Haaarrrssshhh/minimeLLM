# mainllm/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .singleton import EmbeddingManager
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()

# Function to get log file path
def get_log_file_path():
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, datetime.now().strftime("%m-%d-%Y") + '.log')

# Configure logging
logging.basicConfig(
    filename=get_log_file_path(),
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def handle_query(query):
    embedding_manager = EmbeddingManager.get_instance()
    query_embedding = embedding_manager.model.encode([query])[0].tolist()

    results = embedding_manager.query_embedding(query_embedding)

    if results["metadatas"]:
        most_similar_paragraph = results["metadatas"][0][0]["paragraph"]
        return most_similar_paragraph
    else:
        return "No similar paragraph found."

def generate_response(query):
    retrieved_info = handle_query(query)
    print(retrieved_info,"retrieved_info")
    prompt = (
        "You are an expert assistant. Use the provided context to answer the question accurately and in detail.\n\n"
        f"Context: {retrieved_info}\n\n"
        f"Question: {query}\n\n"
        "Answer in a clear and concise manner, keeping the response relevant to the context."
    )
    
    messages = [
        {"role": "system", "content": "You are an expert assistant. Provide accurate and detailed responses based on the given context."},
        {"role": "user", "content": prompt}
    ]
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(
        api_key=api_key,
    )
    completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=150
    )
    response = completion.choices[0].message.content

    # Log the query and response
    logging.info(f"Query: {query}")
    logging.info(f"Response: {response}")

    return response

class QueryView(APIView):
    def post(self, request, format=None):
        user_query = request.data.get('query')
        if user_query:
            response = generate_response(user_query)
            return Response({'response': response}, status=status.HTTP_200_OK)
        return Response({'error': 'Query not provided'}, status=status.HTTP_400_BAD_REQUEST)
