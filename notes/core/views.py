from django.shortcuts import render, redirect
from .models import Note, NoteCategory

# Create your views here.

def main(request):
    return render(request,'main.html')

def notes(request):
    notes = Note.objects.all()
    return render(request, 'notes.html', {'notes':notes})

def note_add(request):
    categories = NoteCategory.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        category_id = request.POST.get('category')

        if title == '' or text == '':
            blankFieldErrorMessage = 'У вас пустое поле'
            return render(request, 'note_add.html', {'error':blankFieldErrorMessage})
        
        category = NoteCategory.objects.get(id=category_id)
        Note.objects.create(title=title,text=text,category=category)
        return redirect(notes)
    
    return render(request,'note_add.html',{'categories':categories})