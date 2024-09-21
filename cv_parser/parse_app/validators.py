from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
import os

VALID_EXTENSIONS = ['.pdf', '.doc', '.docx']

def validate_file_extension(file_object: UploadedFile):
    ext: str = os.path.splitext(file_object.name)[1]
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValidationError(f"Unsupported file extension: {ext}")
    return ext

def validate_file_size(file_object: UploadedFile):
    MAX_UPLOAD_SIZE =  2 * 1024 * 1024
    if file_object.size > MAX_UPLOAD_SIZE:
        raise ValidationError(f"File size exceeds 2MB limit. You uploaded {(file_object.size/1_048_576):.2f} MB")

