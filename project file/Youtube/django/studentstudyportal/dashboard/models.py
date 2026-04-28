from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    """Model for storing student notes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return self.title


class Homework(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('submitted', 'Submitted'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100, default='General')
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['deadline']
        indexes = [
            models.Index(fields=['user', 'deadline']),
            models.Index(fields=['status', 'deadline']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.subject}"


class Subtask(models.Model):
    """Model for subtasks under todos"""
    todo = models.ForeignKey('Todo', on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('study', 'Study'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    progress = models.PositiveIntegerField(default=0, help_text="Progress percentage (0-100)")
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'due_date']),
            models.Index(fields=['completed']),
        ]
    
    def __str__(self):
        return self.title


class Book(models.Model):
    """Model for storing book references"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    added_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title


class DictionaryEntry(models.Model):
    """Model for dictionary entries"""
    word = models.CharField(max_length=200, unique=True)
    meaning = models.TextField()
    pronunciation = models.CharField(max_length=200, blank=True, help_text="Pronunciation guide, e.g., /ˈwɜːrd/")
    example = models.TextField(blank=True)
    added_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['word']
        verbose_name_plural = 'Dictionary Entries'
    
    def __str__(self):
        return self.word


class ConversionEntry(models.Model):
    """Model for unit conversion references"""
    CONVERSION_TYPES = [
        ('length', 'Length'),
        ('weight', 'Weight'),
        ('temperature', 'Temperature'),
        ('volume', 'Volume'),
        ('area', 'Area'),
    ]

    name = models.CharField(max_length=200)
    conversion_type = models.CharField(max_length=50, choices=CONVERSION_TYPES)
    from_unit = models.CharField(max_length=50)
    to_unit = models.CharField(max_length=50)
    formula = models.CharField(max_length=200)

    class Meta:
        ordering = ['conversion_type', 'name']

    def __str__(self):
        return f"{self.name}: {self.from_unit} to {self.to_unit}"

class StudySession(models.Model):
    """Model for tracking study sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.subject} - {self.duration} min"
