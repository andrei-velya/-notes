from django.urls import path

from .views import *
from .views_rest import *

urlpatterns = [
   path('rest/clicks', clicks, name='clicks'),
   path('notes/<int:note_id>/comments', note_comments, name='api_note_comments'),
   path('notes/authors', author_list, name='api_author_list')

]
