from django.db import models

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
    
    title = models.CharField( max_length=255 )
    text = models.TextField( )
    author = models.CharField( max_length=255, default='Автор неизвестен' )
    created_date = models.DateTimeField( auto_now_add=True )
    category = models.ForeignKey(NoteCategory, blank=True, null=True,on_delete=models.SET_NULL,related_name='category_notes' )

