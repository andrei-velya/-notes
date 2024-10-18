from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import TemplateView, CreateView, ListView
from .models import Note,NoteComment,NoteFavorite
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

@login_required
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
    context = {}

    note = Note.objects.get( id = note_id )
    comments_of_the_note = NoteComment.objects.filter( note = note )
    comment_add_form = CommentAddForm()

    if request.user.is_authenticated:
        # проверка текущего пользователя является ли цитата любимой
        is_favorite = NoteFavorite.objects.filter(note=note, profile=request.user.profile).exists()
        print( is_favorite )
        # дополнение контекста новой инфой
        context.update({ "is_favorite" : is_favorite })

    if request.method == 'POST':
        comment_form = CommentAddForm( request.POST )

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
        'comments':comments_of_the_note,
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
    
def notes_search(request):
    notes = Note.objects.all()

    text = request.GET.get('text')
    
    if text:
        notes = notes.filter(Q(title__icontains=text)|Q(text__icontains=text))
 
    #    пагинация
    page = request.GET.get('page', 1)
    p = Paginator(notes, 5)
    page_objects = p.get_page(page)

    categories = NoteCategory.objects.all()

    context = {
        'page_obj': page_objects,
        'categories': categories,
        'search_text': text
    }

    return render(request, 'notes.html', context)


@login_required
def add_to_favorite(request, note_id):
    redirect_url = request.GET.get('next')
    note = Note.objects.get(id=note_id)
    profile = request.user.profile
    NoteFavorite.objects.get_or_create(note=note, profile=profile)
    
    return redirect(redirect_url)

@login_required
def remove_from_favorite(request, note_id):
    redirect_url = request.GET.get('next')
    note = Note.objects.get(id=note_id)
    profile = request.user.profile
    NoteFavorite.objects.filter(note=note, profile=profile).delete()
    
    return redirect(redirect_url)