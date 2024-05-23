# mainllm/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .singleton import EmbeddingManager
from openai import OpenAI
import os
from dotenv import load_dotenv



load_dotenv()
    

def handle_query(query):
    embedding_manager = EmbeddingManager.get_instance()
    query_embedding = embedding_manager.model.encode([query])[0].tolist()
    # print(query_embedding, "Query embedding")  # Debug statement

    results = embedding_manager.query_embedding(query_embedding)
    # print(results, "Query results")  # Debug statement

    if results["metadatas"]:
        most_similar_paragraph = results["metadatas"][0][0]["paragraph"]
        return most_similar_paragraph
    else:
        return "No similar paragraph found."

def generate_response(query):
    retrieved_info = handle_query(query)
    print(retrieved_info,"retrieved_info")
    prompt = f"Question: {query.lower()}\n\nContext: {retrieved_info.lower()}"
    messages = [
        {"role": "system", "content": "You are this person whose information is given to you. Answer in first person always and keep your replies short up to 3-5 sentences. If you cannot find an appropriate answer, say, I cannot share this information with you!"},
        {"role": "user", "content": prompt}
    ]
    api_key = os.getenv('OPENAI_API_KEY')
    print(api_key, "API KEY")  # Debug statement
    client = OpenAI(
        api_key=api_key,
    )
    completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo",
)
    return (completion.choices[0].message.content)

class QueryView(APIView):
    def post(self, request, format=None):
        user_query = request.data.get('query')
        if user_query:
            response = generate_response(user_query)
            return Response({'response': response}, status=status.HTTP_200_OK)
        return Response({'error': 'Query not provided'}, status=status.HTTP_400_BAD_REQUEST)
