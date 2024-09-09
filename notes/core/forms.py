# Задача сделать форму обработки добавления поста
from django import forms
# from .models import PostCategory

class CommentAddForm(forms.Form):
    text = forms.CharField( max_length = 250, widget=forms.Textarea )