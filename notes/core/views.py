from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import TemplateView, CreateView, ListView
from .models import Note,NoteComment,Subscription, NoteLike, Author
from .forms import *
from django.http import Http404
from user.models import Profile

# Create your views here.

def main(request):
    return render(request,'main.html')

def notes(request):
    notes = Note.objects.all()
    categories = NoteCategory.objects.all()
    active_category = None
    category = request.GET.get('category')
    authors = Author.objects.all()
    active_author = None
    author = request.GET.get('author')

    if category:
        notes = Note.objects.filter( category__id = category )
        active_category = NoteCategory.objects.get( id = category )
    
    if author:
        notes = Note.objects.filter( author__id = author )
        active_author = Author.objects.get( id = author )
                                           
    context = {
        'notes':notes,
        'categories':categories,
        'notes':notes,
        'active_category':active_category,
        'authors':authors,
        'active_author':active_author
    }

    return render(request, 'notes.html', context)

@login_required
def note_add(request):
    categories = NoteCategory.objects.all()
    note_add_form = NoteAddForm()

    if request.method == 'POST':
        note_add_form = NoteAddForm( request.POST )

        if note_add_form.is_valid():
            note = note_add_form.save(commit=False)
            author = note_add_form.cleaned_data['author']
            new_author = note_add_form.cleaned_data['new_author']
            
            if author is None and new_author:
                author, already_in_list = Author.objects.get_or_create(name=new_author)
            
            Note.objects.create(
                                title = note_add_form.cleaned_data['title'],
                                text = note_add_form.cleaned_data['text'],
                                author = author,
                                category = note_add_form.cleaned_data['category'],
                                profile=request.user.profile
                                )
            return redirect('notes')
        
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
    context.update({"note": note, "comments": comments_of_the_note, "comment_add_form":comment_add_form})

    if request.user.is_authenticated:
        # проверка текущего пользователя на подписку
        is_subscribed = Subscription.objects.filter(profile=request.user.profile,
                                                    author=note.author)

        # проверка текущего пользователя на лайк
        is_liked = NoteLike.objects.filter(profile=request.user.profile, note=note)

        # дополнение контекста новой инфой
        context.update({"is_subscribed": is_subscribed, "is_liked": is_liked})

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
def subscribe(request, author_id):
    redirect_url = request.GET.get('next')
    profile = request.user.profile
    author = Author.objects.get( id=author_id )

    Subscription.objects.get_or_create(author=author, profile=profile)

    return redirect(redirect_url)


@login_required
def unsubscribe(request, author_id):
    redirect_url = request.GET.get('next')
    profile = request.user.profile
    author = Author.objects.get(id=author_id)
    
    Subscription.objects.filter(author=author, profile=profile).delete()

    return redirect(redirect_url)


@login_required
def note_like(request, note_id):
    redirect_url = request.GET.get('next')
    note = Note.objects.get(id=note_id)
    profile = request.user.profile

    NoteLike.objects.get_or_create(note=note, profile=profile)

    return redirect(redirect_url)


@login_required
def note_unlike(request, note_id):
    redirect_url = request.GET.get('next')
    # удаляем текущие лайки
    note = Note.objects.get(id=note_id)
    profile = request.user.profile

    NoteLike.objects.filter(note=note, profile=profile).delete()

    return redirect(redirect_url)

@login_required
def note_edit(request, note_id):
    note = Note.objects.get( id = note_id )
    
    if note.profile != request.user.profile:
        raise Http404
    
    form = NoteAddForm( instance = note )

    if request.method == 'POST':
        form = NoteAddForm( request.POST, instance = note )
        if form.is_valid:
            form.save()

            return redirect('note_detail', note.id)
          
    return render(request, 'note_edit.html', {'form':form})