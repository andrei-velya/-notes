from django.shortcuts import render, redirect
from .models import Note, NoteCategory, NoteComment
from .forms import CommentAddForm
from django.http import Http404

# Create your views here.

def main(request):
    return render(request,'main.html')

def notes(request):
    notes = Note.objects.all()

    categories = NoteCategory.objects.all()
    active_category = None
    category = request.GET.get('category')
    if category:
        notes = Note.objects.filter( category__id = category )
        active_category = NoteCategory.objects.get( id = category )
    context = {
        'notes':notes,
        'categories':categories,
        'notes':notes,
        'active_category':active_category
    }

    return render(request, 'notes.html', context)

def note_add(request):
    categories = NoteCategory.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        author = request.POST.get('author')
        category_id = request.POST.get('category')

        if title == '' or text == '':
            blankFieldErrorMessage = 'У вас пустое поле'
            return render(request, 'note_add.html', {'error':blankFieldErrorMessage})
        
        category = NoteCategory.objects.get(id=category_id)
        Note.objects.create(title=title,text=text,category=category,author=author)
        return redirect(notes)
    return render(request,'note_add.html',{'categories':categories})

def note_detail( request, note_id ):
    note = Note.objects.get( id = note_id )
    comments_of_the_post = NoteComment.objects.filter( note = note )
    comment_add_form = CommentAddForm()
    if request.method == 'POST':
        comment_form = CommentAddForm( request.POST )
        note = Note.objects.get( id = note_id )
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            NoteComment.objects.create(
                note = note,
                text = data['text']
            )
            return redirect('note_detail',note_id) 
        else:
            raise Http404
    context ={
        'note':note,
        'comments':comments_of_the_post,
        'comment_add_form':comment_add_form
        }
    return render(request,'note_detail.html',context)