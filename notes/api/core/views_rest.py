from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import random

# Create your views here.

@api_view(['GET'])
def clicks(request):
    return Response({'clicks':random.randint(1,100)})