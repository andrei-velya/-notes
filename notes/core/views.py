from django.shortcuts import render, redirect
from .models import *
from .forms import *
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
    note_add_form = NoteAddForm()

    if request.method == 'POST':
        note_add_form = NoteAddForm( request.POST )

        if note_add_form.is_valid():
            data = note_add_form.cleaned_data
            Note.objects.create(
                                title = data['title'],
                                text = data['text'],
                                author = data['author'],
                                category = data['category']
                                )

        return redirect(notes)
    
    context = {
               'categories':categories,
               'note_add_form':note_add_form
               }
    
    return render( request, 'note_add.html', context)

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

def feedback( request ):
    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Feedback.objects.create(
                                    name = data['name'],
                                    text = data['text']
                                    )
            return redirect('feedback_success')
    context = { 'feedback_add_form':form }
    return render(request, 'feedback.html',context)

def feedback_success(request):
    return render(request, 'feedback_success.html')
    