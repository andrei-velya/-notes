from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Note)
admin.site.register(NoteCategory)
admin.site.register(Feedback)
admin.site.register(NoteFavorite)