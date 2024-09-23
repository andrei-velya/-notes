from django.db import models
from django import forms

# Create your models here.

class NoteCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length = 255, verbose_name = 'Название')
    
    def __str__(self) -> str:
        return self.title   

class Note(models.Model):
    
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
    
    title = models.CharField( max_length=255, null=False )
    text = models.TextField( null=False )
    author = models.CharField( max_length=255, default='Автор неизвестен', null=False )
    created_date = models.DateTimeField( auto_now_add=True )
    category = models.ForeignKey(
                                 NoteCategory, 
                                 blank=True, 
                                 null=True,
                                 on_delete=models.SET_DEFAULT,
                                 related_name='category_notes',
                                 default='Разное'
                                 )

class NoteComment(models.Model):

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    note = models.ForeignKey(
                             Note, 
                             blank=False, 
                             on_delete=models.CASCADE, 
                             null=False, 
                             related_name='comment_note', 
                             default=1 
                             )
    text = models.CharField( max_length=280 )
    author = models.CharField( max_length=255, default='Анонимус' )
    created_date = models.DateTimeField( auto_now_add=True )

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.name