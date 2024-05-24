from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.llm.gemini import Gemini
from House import *

# Instanciate gemini llm
gemini = Gemini()

# Instanciate house with our map
house = House()

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