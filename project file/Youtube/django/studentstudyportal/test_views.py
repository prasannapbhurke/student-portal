import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentstudyportal.settings')
os.chdir(r'C:\Users\PRASANNA\Desktop\student portal\project file\Youtube\django\studentstudyportal')
import django
django.setup()

from dashboard.models import Homework, Todo
print('Homework fields:', [f.name for f in Homework._meta.fields])
print('Todo fields:', [f.name for f in Todo._meta.fields])

with open(r'dashboard/views.py') as f:
    lines = f.readlines()
    
for i, line in enumerate(lines, 1):
    if 'def homework' in line or 'def todo' in line or 'def calendar_view' in line:
        print('Line %d: %s' % (i, line.strip()))
    if 'due_date' in line:
        print('  Line %d uses due_date: %s' % (i, line.strip()))
    if i > 170 and i < 190 and 'due_date' in line:
        print('  BUG - homework uses due_date here!')
    if i > 379 and i < 397 and 'due_date' in line:
        print('  calendar_view uses due_date (correct for Todo)')
        