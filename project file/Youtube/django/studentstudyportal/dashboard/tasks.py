from celery import shared_task
import csv
from io import StringIO
from django.core.files.base import ContentFile
from .models import Note, Export

@shared_task
def generate_notes_export(export_id):
    try:
        export = Export.objects.get(id=export_id)
        notes = Note.objects.filter(user=export.user)
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Title', 'Description', 'Created At'])
        for note in notes:
            writer.writerow([note.title, note.description, note.created_at])
        export.csv_data = output.getvalue()
        export.status = 'ready'
        export.save()
    except Exception as e:
        export = Export.objects.get(id=export_id)
        export.status = 'failed'
        export.error_message = str(e)
        export.save()