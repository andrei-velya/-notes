from django.db import models
from django import forms
from user.models import Profile

# Create your models here.
class Author(models.Model):
    name = models.CharField( max_length=255, unique=True )  

    class Meta:
        verbose_name = 'Автор цитат'
        verbose_name_plural = 'Авторы цитат'

    def __str__(self):
        return self.name

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
    author = models.ForeignKey(
                               Author,
                               blank=True,
                               null=True,
                               on_delete=models.SET_DEFAULT,
                               related_name='note_author',
                               default='Автор неизвестен',
                               to_field='name'                      
                               )
    created_date = models.DateTimeField( auto_now_add=True )
    category = models.ForeignKey(
                                 NoteCategory, 
                                 blank=True, 
                                 null=True,
                                 on_delete=models.SET_DEFAULT,
                                 related_name='category_notes',
                                 default='Разное'
                                 )
    profile = models.ForeignKey(Profile,
                                related_name='profile_notes',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
    profile = models.ForeignKey( Profile, on_delete=models.CASCADE )
    created_date = models.DateTimeField( auto_now_add=True )

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.name

class Subscription(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='profile_followers')
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                                related_name='profile_following')

    class Meta:
        verbose_name = 'Подписка на мудреца'
        verbose_name_plural = 'Подписки на мудреца'

    def __str__(self):
        return f'{self.profile.user.username} подписан на {self.author}'


class NoteLike(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note_likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_likes')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк цитаты'
        verbose_name_plural = 'Лайки цитат'

    def __str__(self):
        return f"{self.note}-{self.profile.user}"
    
class NoteFavorite(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note_favorites')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_favorites')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избраная цитата'
        verbose_name_plural = 'Избранные цитаты'

    def __str__(self):
        return f"{self.note}-{self.profile.user}"