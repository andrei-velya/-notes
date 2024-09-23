"""
URL configuration for notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from.views import *

urlpatterns = [
    path('', main, name='main'),
    path( 'notes', notes, name='notes' ),
    path( 'notes/<int:note_id>', note_detail, name='note_detail' ),
    path('note_add', note_add, name='note_add'),
    path('feedback',feedback, name='feedback'),
    path('feedback/success',feedback_success, name='feedback_success')
]
