from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.http import HttpResponse
from django.conf import settings
import csv
import requests
from .models import Note, Homework, Todo, Subtask, Book, DictionaryEntry, ConversionEntry, StudySession

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

def notes(request):
    """View all notes"""
    user = request.user if request.user.is_authenticated else None
    notes = Note.objects.filter(user=user) if user else Note.objects.filter(user__isnull=True)
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
    context = {'notes': notes, 'query': q, 'date_from': date_from, 'date_to': date_to}
    return render(request, 'dashboard/notes.html', context)

def export_notes(request):
    """Export notes to CSV"""
    user = request.user if request.user.is_authenticated else None
    notes = Note.objects.filter(user=user) if user else Note.objects.filter(user__isnull=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notes.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Created At'])
    for note in notes:
        writer.writerow([note.title, note.description, note.created_at])
    return response

def dashboard(request):
    """Progress dashboard"""
    user = request.user if request.user.is_authenticated else None
    if not user:
        return redirect('account_login')
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

def add_note(request):
    """Add a new note"""
    user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Note.objects.create(user=user, title=title, description=description)
        messages.success(request, 'Note added successfully!')
        return redirect('notes')
    return render(request, 'dashboard/add_note.html')

def edit_note(request, id):
    """Edit a note"""
    user = request.user if request.user.is_authenticated else None
    note = get_object_or_404(Note, id=id, user=user) if user else get_object_or_404(Note, id=id, user__isnull=True)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.description = request.POST.get('description')
        note.save()
        messages.success(request, 'Note updated successfully!')
        return redirect('notes')
    context = {'note': note}
    return render(request, 'dashboard/edit_note.html', context)

def delete_note(request, id):
    """Delete a note"""
    user = request.user if request.user.is_authenticated else None
    note = get_object_or_404(Note, id=id, user=user) if user else get_object_or_404(Note, id=id, user__isnull=True)
    note.delete()
    messages.success(request, 'Note deleted!')
    return redirect('notes')

def homework(request):
    """View all homework"""
    user = request.user if request.user.is_authenticated else None
    homework = Homework.objects.filter(user=user) if user else Homework.objects.filter(user__isnull=True)
    q = request.GET.get('q')
    if q:
        homework = homework.filter(title__icontains=q) | homework.filter(description__icontains=q)
    context = {'homework': homework, 'query': q}
    return render(request, 'dashboard/homework.html', context)

def edit_homework(request, id):
    """Edit homework"""
    user = request.user if request.user.is_authenticated else None
    homework = get_object_or_404(Homework, id=id, user=user) if user else get_object_or_404(Homework, id=id, user__isnull=True)
    if request.method == 'POST':
        homework.title = request.POST.get('title')
        homework.description = request.POST.get('description')
        homework.subject = request.POST.get('subject')
        homework.deadline = request.POST.get('deadline')
        homework.save()
        messages.success(request, 'Homework updated!')
        return redirect('homework')
    context = {'homework': homework}
    return render(request, 'dashboard/edit_homework.html', context)

def add_homework(request):
    """Add homework"""
    user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        subject = request.POST.get('subject')
        deadline = request.POST.get('deadline')
        Homework.objects.create(
            user=user,
            title=title,
            description=description,
            subject=subject,
            deadline=deadline
        )
        messages.success(request, 'Homework added!')
        return redirect('homework')
    return render(request, 'dashboard/add_homework.html')

def todo(request):
    """View all todos"""
    user = request.user if request.user.is_authenticated else None
    todos = Todo.objects.filter(user=user) if user else Todo.objects.filter(user__isnull=True)
    q = request.GET.get('q')
    if q:
        todos = todos.filter(title__icontains=q) | todos.filter(description__icontains=q)
    today = timezone.now().date()
    overdue_count = todos.filter(due_date__lt=today, completed=False).count()
    context = {'todos': todos, 'today': today, 'query': q, 'overdue_count': overdue_count}
    return render(request, 'dashboard/todo.html', context)

def edit_todo(request, id):
    """Edit a todo"""
    user = request.user if request.user.is_authenticated else None
    todo = get_object_or_404(Todo, id=id, user=user) if user else get_object_or_404(Todo, id=id, user__isnull=True)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.priority = request.POST.get('priority', 'medium')
        todo.category = request.POST.get('category', 'personal')
        todo.progress = int(request.POST.get('progress', 0))
        due_date = request.POST.get('due_date')
        todo.due_date = due_date if due_date else None
        todo.save()
        messages.success(request, 'Todo updated!')
        return redirect('todo')
    context = {'todo': todo}
    return render(request, 'dashboard/edit_todo.html', context)

def add_todo(request):
    """Add a todo"""
    user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')
        category = request.POST.get('category', 'personal')
        progress = int(request.POST.get('progress', 0))
        due_date = request.POST.get('due_date')
        Todo.objects.create(
            user=user,
            title=title,
            description=description,
            priority=priority,
            category=category,
            progress=progress,
            due_date=due_date if due_date else None
        )
        messages.success(request, 'Todo added!')
        return redirect('todo')
    return render(request, 'dashboard/add_todo.html')

def mark_todo_complete(request, id):
    """Mark todo as complete"""
    user = request.user if request.user.is_authenticated else None
    todo = get_object_or_404(Todo, id=id, user=user) if user else get_object_or_404(Todo, id=id, user__isnull=True)
    todo.completed = True
    todo.progress = 100
    todo.save()
    messages.success(request, 'Todo marked as complete!')
    return redirect('todo')

def add_subtask(request, todo_id):
    """Add a subtask to a todo"""
    user = request.user if request.user.is_authenticated else None
    todo = get_object_or_404(Todo, id=todo_id, user=user) if user else get_object_or_404(Todo, id=todo_id, user__isnull=True)
    if request.method == 'POST':
        title = request.POST.get('title')
        Subtask.objects.create(todo=todo, title=title)
        messages.success(request, 'Subtask added!')
    return redirect('todo')

def toggle_subtask(request, id):
    """Toggle subtask completion"""
    subtask = get_object_or_404(Subtask, id=id)
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
    if query and settings.YOUTUBE_API_KEY:
        try:
            response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={settings.YOUTUBE_API_KEY}&maxResults=5', timeout=5)
            if response.status_code == 200:
                data = response.json()
                videos = data.get('items', [])
        except:
            pass
    context = {'query': query, 'videos': videos}
    return render(request, 'dashboard/youtube.html', context)

def wiki_search(request):
    """Wikipedia search view"""
    query = request.GET.get('query')
    summary = None
    if query:
        try:
            response = requests.get(f'https://en.wikipedia.org/api/rest_v1/page/summary/{query}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                summary = data.get('extract')
        except:
            summary = "Error fetching data."
    context = {'query': query, 'summary': summary}
    return render(request, 'dashboard/wiki.html', context)

def calendar_view(request):
    """Calendar view for homework and todos"""
    user = request.user if request.user.is_authenticated else None
    today = timezone.now().date()
    upcoming_homework = Homework.objects.filter(user=user, due_date__gte=today).order_by('due_date') if user else Homework.objects.filter(user__isnull=True, due_date__gte=today).order_by('due_date')
    upcoming_todos = Todo.objects.filter(user=user, due_date__gte=today, completed=False).order_by('due_date') if user else Todo.objects.filter(user__isnull=True, due_date__gte=today, completed=False).order_by('due_date')
    context = {
        'today': today,
        'upcoming_homework': upcoming_homework,
        'upcoming_todos': upcoming_todos,
    }
    return render(request, 'dashboard/calendar.html', context)

def study_sessions(request):
    """View study sessions"""
    user = request.user if request.user.is_authenticated else None
    sessions = StudySession.objects.filter(user=user) if user else StudySession.objects.filter(user__isnull=True)
    q = request.GET.get('q')
    if q:
        sessions = sessions.filter(subject__icontains=q)
    total_time = sessions.aggregate(total=models.Sum('duration'))['total'] or 0
    context = {'sessions': sessions, 'query': q, 'total_time': total_time}
    return render(request, 'dashboard/study_sessions.html', context)

def add_study_session(request):
    """Add study session"""
    user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        subject = request.POST.get('subject')
        duration = int(request.POST.get('duration'))
        date = request.POST.get('date')
        notes = request.POST.get('notes')
        StudySession.objects.create(
            user=user,
            subject=subject,
            duration=duration,
            date=date or timezone.now().date(),
            notes=notes
        )
        messages.success(request, 'Study session added!')
        return redirect('study_sessions')
    return render(request, 'dashboard/add_study_session.html')