# mainllm/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv
import logging
from .chromadb_client import get_collection


load_dotenv()


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
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=5,
        include=['documents', 'distances', 'metadatas']
    )


    return results['documents']




def generate_response(query):
    retrieved_info = handle_query(query)
    prompt = f"Question: {query.lower()}\n\nContext: {retrieved_info}"
    messages = [
        {"role": "system", "content": "You are this person whose information is given to you. Answer in first person always and keep your replies short up to 3-5 sentences. If you cannot find an appropriate answer, say, I cannot share this information with you!"},
        {"role": "user", "content": prompt}
    ]
    api_key = os.getenv('OPENAI_API_KEY')
    # print(api_key, "API KEY")  # Debug statement
    client = OpenAI(
        api_key=api_key,
    )
    completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo",
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
