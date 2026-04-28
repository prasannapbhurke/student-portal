from django import forms
from .models import Note, Homework, Todo, Subtask, Book, DictionaryEntry, ConversionEntry, StudySession

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Note content'}),
        }

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'description', 'deadline', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Homework title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'priority', 'category', 'progress']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category (e.g., Work, Personal)'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }

class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['title', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtask title'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['duration', 'notes']
        widgets = {
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Minutes'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What did you study?'}),
        }
