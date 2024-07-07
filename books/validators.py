import os
from django.core.exceptions import ValidationError

def validate_is_pdf(file):
    valid_file_extensions = ['.pdf']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Only PDF files are allowed.')
