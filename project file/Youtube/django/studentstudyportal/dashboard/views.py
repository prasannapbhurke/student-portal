from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import csv
import requests
import urllib.parse
from .models import Note, Homework, Todo, Subtask, Book, DictionaryEntry, ConversionEntry, StudySession, Export
from .forms import NoteForm, HomeworkForm, TodoForm, SubtaskForm, StudySessionForm
from .tasks import generate_notes_export

def home(request):
    """Home page with feature overview"""
    user = request.user if request.user.is_authenticated else None
    context = {
        'notes_count': Note.objects.filter(user=user).count() if user else Note.objects.filter(user__isnull=True).count(),
        'homework_count': Homework.objects.filter(user=user, status='pending').count() if user else Homework.objects.filter(user__isnull=True, status='pending').count(),
        'todo_count': Todo.objects.filter(user=user, completed=False).count() if user else Todo.objects.filter(user__isnull=True, completed=False).count(),
        'books_count': Book.objects.count(),
        'dictionary_count': DictionaryEntry.objects.count(),
        'conversions_count': ConversionEntry.objects.count(),
        'sessions_count': StudySession.objects.filter(user=user).count() if user else StudySession.objects.filter(user__isnull=True).count(),
    }
    return render(request, 'dashboard/home.html', context)

def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Account created! You can now log in.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating account: {e}')
                return render(request, 'dashboard/signup.html', {'form': form})
        else:
            # Form has errors; render with errors
            return render(request, 'dashboard/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'dashboard/signup.html', {'form': form})


@login_required
def notes(request):
    """View all notes"""
    user = request.user
    notes = Note.objects.filter(user=user)
    q = request.GET.get('q')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if q:
        notes = notes.filter(models.Q(title__icontains=q) | models.Q(description__icontains=q))
    if date_from:
        notes = notes.filter(created_at__date__gte=date_from)
    if date_to:
        notes = notes.filter(created_at__date__lte=date_to)
    if request.method == 'POST' and 'bulk_delete' in request.POST:
        selected_ids = request.POST.getlist('selected_notes')
        if selected_ids:
            notes.filter(id__in=selected_ids).delete()
            messages.success(request, f'Deleted {len(selected_ids)} notes.')
            return redirect('notes')
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'query': q, 'date_from': date_from, 'date_to': date_to}
    return render(request, 'dashboard/notes.html', context)


@login_required
def export_notes(request):
    """Trigger export of notes to CSV (async if Celery available, else sync)"""
    export = Export.objects.create(user=request.user, status='pending')
    try:
        generate_notes_export.delay(export.id)
        messages.info(request, 'Your export is being processed. Visit the Exports page to download when ready.')
    except Exception as e:
        # Fallback to synchronous generation if Celery/Redis unavailable
        try:
            generate_notes_export(export.id)
            messages.success(request, 'Your export is ready. Visit Exports page to download.')
        except Exception as e2:
            export.status = 'failed'
            export.error_message = str(e2)
            export.save()
            messages.error(request, f'Export failed: {e2}')
    return redirect('notes')

@login_required
def dashboard(request):
    """Progress dashboard"""
    user = request.user
    total_notes = Note.objects.filter(user=user).count()
    total_homework = Homework.objects.filter(user=user).count()
    pending_homework = Homework.objects.filter(user=user, status='pending').count()
    total_todos = Todo.objects.filter(user=user).count()
    completed_todos = Todo.objects.filter(user=user, completed=True).count()
    total_sessions = StudySession.objects.filter(user=user).count()
    total_session_time = StudySession.objects.filter(user=user).aggregate(total=models.Sum('duration'))['total'] or 0
    context = {
        'total_notes': total_notes,
        'total_homework': total_homework,
        'pending_homework': pending_homework,
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'completion_rate': (completed_todos / total_todos * 100) if total_todos > 0 else 0,
        'total_sessions': total_sessions,
        'total_session_time': total_session_time,
    }
    return render(request, 'dashboard/dashboard.html', context)

def timer(request):
    """Study timer"""
    return render(request, 'dashboard/timer.html')

def flashcards(request):
    """Flashcard decks"""
    # Placeholder for now
    return render(request, 'dashboard/flashcards.html')

def quizzes(request):
    """Quiz builder"""
    # Placeholder
    return render(request, 'dashboard/quizzes.html')


@login_required
def add_note(request):
    """Add a new note"""
    form = NoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        messages.success(request, 'Note added successfully!')
        return redirect('notes')
    return render(request, 'dashboard/add_note.html', {'form': form})


@login_required
def edit_note(request, id):
    """Edit a note"""
    note = get_object_or_404(Note, id=id, user=request.user)
    form = NoteForm(request.POST or None, instance=note)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Note updated successfully!')
        return redirect('notes')
    return render(request, 'dashboard/edit_note.html', {'form': form, 'note': note})


@login_required
def delete_note(request, id):
    """Delete a note"""
    note = get_object_or_404(Note, id=id, user=request.user)
    note.delete()
    messages.success(request, 'Note deleted successfully!')
    return redirect('notes')


@login_required
def homework(request):
    """View all homework"""
    user = request.user
    homeworks = Homework.objects.filter(user=user).order_by('deadline')
    q = request.GET.get('q')
    status = request.GET.get('status')
    if q:
        homeworks = homeworks.filter(models.Q(title__icontains=q) | models.Q(description__icontains=q))
    if status:
        homeworks = homeworks.filter(status=status)
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(homeworks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/homework.html', {'page_obj': page_obj, 'query': q, 'status': status})


@login_required
def add_homework(request):
    """Add a new homework"""
    form = HomeworkForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        homework = form.save(commit=False)
        homework.user = request.user
        homework.save()
        messages.success(request, 'Homework added successfully!')
        return redirect('homework')
    return render(request, 'dashboard/add_homework.html', {'form': form})


@login_required
def edit_homework(request, id):
    """Edit a homework"""
    homework = get_object_or_404(Homework, id=id, user=request.user)
    form = HomeworkForm(request.POST or None, instance=homework)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Homework updated successfully!')
        return redirect('homework')
    return render(request, 'dashboard/edit_homework.html', {'form': form, 'homework': homework})


@login_required
def delete_homework(request, id):
    """Delete a homework"""
    homework = get_object_or_404(Homework, id=id, user=request.user)
    homework.delete()
    messages.success(request, 'Homework deleted successfully!')
    return redirect('homework')


@login_required
def todo(request):
    """View all todos"""
    user = request.user
    todos = Todo.objects.filter(user=user).prefetch_related('subtasks').order_by('due_date')
    q = request.GET.get('q')
    if q:
        todos = todos.filter(models.Q(title__icontains=q) | models.Q(description__icontains=q))
    today = timezone.now().date()
    overdue_count = todos.filter(due_date__lt=today, completed=False).count()
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(todos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/todo.html', {'page_obj': page_obj, 'today': today, 'query': q, 'overdue_count': overdue_count})


@login_required
def add_todo(request):
    """Add a todo"""
    form = TodoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        messages.success(request, 'Todo added successfully!')
        return redirect('todo')
    return render(request, 'dashboard/add_todo.html', {'form': form})


@login_required
def edit_todo(request, id):
    """Edit a todo"""
    todo = get_object_or_404(Todo, id=id, user=request.user)
    form = TodoForm(request.POST or None, instance=todo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Todo updated successfully!')
        return redirect('todo')
    return render(request, 'dashboard/edit_todo.html', {'form': form, 'todo': todo})


@login_required
def mark_todo_complete(request, id):
    """Mark todo as complete"""
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.completed = True
    todo.progress = 100
    todo.save()
    messages.success(request, 'Todo marked as complete!')
    return redirect('todo')


@login_required
def add_subtask(request, todo_id):
    """Add a subtask to a todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    form = SubtaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        subtask = form.save(commit=False)
        subtask.todo = todo
        subtask.save()
        messages.success(request, 'Subtask added!')
    return redirect('todo')


@login_required
def toggle_subtask(request, id):
    """Toggle subtask completion"""
    subtask = get_object_or_404(Subtask, id=id, todo__user=request.user)
    subtask.completed = not subtask.completed
    subtask.save()
    # Update todo progress based on subtasks
    todo = subtask.todo
    total_subtasks = todo.subtasks.count()
    if total_subtasks > 0:
        completed = todo.subtasks.filter(completed=True).count()
        todo.progress = int((completed / total_subtasks) * 100)
        if completed == total_subtasks:
            todo.completed = True
        todo.save()
    return redirect('todo')

def books(request):
    """View books list"""
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'dashboard/books.html', context)

def dictionary(request):
    """Dictionary search view"""
    word = request.GET.get('word', '')
    result = None
    if word:
        try:
            result = DictionaryEntry.objects.get(word__iexact=word)
        except DictionaryEntry.DoesNotExist:
            messages.info(request, 'Word not found in dictionary')
    
    context = {'result': result, 'word': word}
    return render(request, 'dashboard/dictionary.html', context)

def conversion(request):
    """Unit conversion view"""
    conversions = ConversionEntry.objects.all()
    context = {'conversions': conversions}
    return render(request, 'dashboard/conversion.html', context)


def youtube_search(request):
    """YouTube search view"""
    query = request.GET.get('query')
    videos = []
    error_message = None
    if query:
        if not settings.YOUTUBE_API_KEY:
            error_message = "YouTube API key not configured."
        else:
            try:
                response = requests.get('https://www.googleapis.com/youtube/v3/search', 
                    params={'part': 'snippet', 'q': query, 'type': 'video', 'key': settings.YOUTUBE_API_KEY, 'maxResults': 5},
                    timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    videos = data.get('items', [])
                else:
                    error_message = f"YouTube API error: {response.status_code}"
            except Exception as e:
                error_message = f"Error: {str(e)}"
    context = {'query': query, 'videos': videos, 'error_message': error_message}
    return render(request, 'dashboard/youtube.html', context)

def wiki_search(request):
    """Wikipedia search view"""
    query = request.GET.get('query')
    summary = None
    error_message = None
    if query:
        try:
            encoded = urllib.parse.quote(query)
            headers = {
                'User-Agent': 'StudentStudyPortal/1.0 (https://github.com/your-repo; contact@example.com)'
            }
            response = requests.get(
                f'https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}',
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                summary = data.get('extract')
            elif response.status_code == 404:
                summary = None  # No article found
            elif response.status_code == 403:
                error_message = "Wikipedia API access denied. This may be due to rate limiting. Please try again later."
            else:
                error_message = f"Wikipedia API error: {response.status_code}"
        except Exception as e:
            error_message = f"Error: {str(e)}"
    context = {'query': query, 'summary': summary, 'error_message': error_message}
    return render(request, 'dashboard/wiki.html', context)

@login_required
def calendar_view(request):
    """Calendar view for homework and todos"""
    user = request.user
    today = timezone.now().date()
    upcoming_homework = Homework.objects.filter(user=user, deadline__gte=today).order_by('deadline')
    upcoming_todos = Todo.objects.filter(user=user, due_date__gte=today, completed=False).order_by('due_date')
    events = []
    for h in upcoming_homework:
        events.append({'title': f'Homework: {h.title}', 'start': h.deadline.isoformat(), 'color': '#dc3545'})
    for t in upcoming_todos:
        events.append({'title': f'Todo: {t.title}', 'start': t.due_date.isoformat(), 'color': '#007bff'})
    context = {
        'today': today,
        'upcoming_homework': upcoming_homework,
        'upcoming_todos': upcoming_todos,
        'events': events,
    }
    return render(request, 'dashboard/calendar.html', context)


@login_required
def study_sessions(request):
    """View study sessions"""
    sessions_qs = StudySession.objects.filter(user=request.user).order_by('-date')
    q = request.GET.get('q')
    if q:
        sessions_qs = sessions_qs.filter(notes__icontains=q)
    total_time = sessions_qs.aggregate(total=models.Sum('duration'))['total'] or 0
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(sessions_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/study_sessions.html', {'page_obj': page_obj, 'query': q, 'total_time': total_time})


@login_required
def add_study_session(request):
    """Add a study session"""
    form = StudySessionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        session = form.save(commit=False)
        session.user = request.user
        session.save()
        messages.success(request, 'Study session added!')
        return redirect('study_sessions')
    return render(request, 'dashboard/add_study_session.html', {'form': form})

@login_required
def export_list(request):
    """List all exports for the user"""
    exports = Export.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/exports.html', {'exports': exports})

@login_required
def download_export(request, id):
    """Download a completed export"""
    export = get_object_or_404(Export, id=id, user=request.user)
    if export.status != 'ready':
        messages.warning(request, 'Export not ready yet.')
        return redirect('export_list')
    response = HttpResponse(export.csv_data, content_type='text/csv')
    filename = f'notes_{request.user.username}_{export.id}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response