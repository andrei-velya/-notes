from django.urls import path

from .views import *
from .views_rest import *

urlpatterns = [
   path('rest/clicks', clicks, name='clicks')
]
