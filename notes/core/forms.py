# Задача сделать форму обработки добавления поста
from django import forms
from django.core.exceptions import ValidationError
from .models import NoteCategory, Feedback

class CommentAddForm(forms.Form):
    text = forms.CharField( max_length = 250, widget=forms.Textarea )

class NoteAddForm(forms.Form):
    title = forms.CharField( label='Заголовок цитаты', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}) )
    text = forms.CharField( label='Введите цитату', max_length=1024, widget=forms.Textarea )
    author = forms.CharField( label='Автор', max_length=100 )
    category = forms.ModelChoiceField( label='Категория', queryset=NoteCategory.objects.all() )

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name','text']
    
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.split()) < 2:
            raise ValidationError('Введите хотя бы два слова!')
        return name
    