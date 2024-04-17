from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.gemini import Gemini

# Instanciate gemini llm
gemini = Gemini()

@api_view(['GET'])
def test(request):
    return Response({'message': 'Hello World!'})

@api_view(['GET'])
def test_query(request):
    query = request.GET.get('query', '')
    if not query:
        raise Exception("Query is empty")
    else:
        print(f"Query: {query}")
    
    response = gemini(query)
    return Response({'response': response})