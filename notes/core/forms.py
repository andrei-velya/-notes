# Задача сделать форму обработки добавления поста
from django import forms
from .models import NoteCategory

class CommentAddForm(forms.Form):
    text = forms.CharField( max_length = 250, widget=forms.Textarea )

class NoteAddForm(forms.Form):
    title = forms.CharField( label='Заголовок цитаты', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}) )
    text = forms.CharField( label='Введите цитату', max_length=1024, widget=forms.Textarea )
    author = forms.CharField( label='Автор', max_length=100 )
    category = forms.ModelChoiceField( label='Категория', queryset=NoteCategory.objects.all() )

class FeedbackForm(forms.Form):
    name = forms.CharField( label='Имя' )
    text = forms.CharField(label='Текст',widget=forms.Textarea )
    