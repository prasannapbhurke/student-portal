from django.contrib import admin
from .models import Note, Homework, Todo, Book, DictionaryEntry, ConversionEntry

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'description')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'user', 'deadline', 'status')
    list_filter = ('status', 'subject', 'deadline')
    search_fields = ('title', 'subject')

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'completed', 'due_date')
    list_filter = ('priority', 'completed', 'due_date')
    search_fields = ('title',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subject')
    list_filter = ('subject',)
    search_fields = ('title', 'author')

@admin.register(DictionaryEntry)
class DictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ('word', 'added_at')
    search_fields = ('word',)

@admin.register(ConversionEntry)
class ConversionEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'conversion_type', 'from_unit', 'to_unit')
    list_filter = ('conversion_type',)
    search_fields = ('name',)
