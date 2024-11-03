from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
from core.models import Note, NoteComment, Author
from .serializers import AuthorSerializer

# Create your views here.

@api_view(['GET'])
def clicks(request):
    return Response({'clicks':random.randint(1,100)})

@api_view(['GET'])
def note_comments(request, note_id):
    note = Note.objects.get(id = note_id)
    comments = NoteComment.objects.filter(note=note)

    new_comments = []

    for comment in comments:
        new_comments.append({
                             'text' : comment.text,
                             'profile' : comment.profile.user.username,
                             'created_date': comment.created_date
                             })
    
    return JsonResponse({'comments' : new_comments}, safe=False)

@api_view(['GET'])
def author_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer( authors, many=True )

    return Response({ 'authors_serializer':serializer.data })