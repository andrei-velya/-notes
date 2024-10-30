# Задача сделать форму обработки добавления поста
from django import forms
from django.core.exceptions import ValidationError
from .models import NoteCategory, Feedback, Note, Author

class CommentAddForm(forms.Form):
    text = forms.CharField( max_length = 250, widget=forms.Textarea )

    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.profile.user:
            comment.profile = self.profile
        return comment


class NoteAddForm(forms.ModelForm):
    author = forms.ModelChoiceField(
                                    queryset=Author.objects.all(),
                                    required=False,
                                    empty_label="Выберите автора"
                                    )
    
    new_author = forms.CharField(
                                 max_length=100,
                                 required=False,
                                 label="Имя нового автора",
                                 help_text="(введите если нет в основном списке)"
                                )

    class Meta:
        model = Note
        fields = [ 'title', 'text', 'author','new_author', 'category' ]
    
    def __init__(self, *args, **kwargs):
        super(NoteAddForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

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
    