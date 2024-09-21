from parse_app.validators import validate_file_extension, validate_file_size
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
import pytest

@pytest.mark.parametrize(
    'extension, is_exception_raised',
    [
        ('pdf', False),
        ('doc', False),
        ('docx', False),
        ('txt', True),
        ('ppt', True),
        ('mp3', True),
        ('mp4', True),
    ]
)
def test_validate_file_extension(extension, is_exception_raised):
    file = SimpleUploadedFile(name=f"sample-file.{extension}", content=b"Note")
    if is_exception_raised:
        with pytest.raises(ValidationError, match="Unsupported file extension"):
            validate_file_extension(file)
    else:
        assert validate_file_extension(file)


@pytest.mark.parametrize("file_size, is_exception_raised", [
    (2_000_000, False),
    (3_097_152, True),
    (6_097_152, True)
    ]
)

def test_validate_file_size(file_size, is_exception_raised):
    file = SimpleUploadedFile(name="sample-file.pdf", content=b"Note")
    file.size = file_size
    if is_exception_raised:
        with pytest.raises(ValidationError, match="File size exceeds 2MB limit"):
            validate_file_size(file)
    else:
        assert not validate_file_size(file)
    