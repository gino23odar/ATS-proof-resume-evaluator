from parse_app.utils import read_uploaded_file
from .conftest import FILE_CONTENT

def test_read_uploaded_pdf_file(generate_pdf_file):
    file_path = generate_pdf_file
    with open(file_path, "rb") as file:
        content = read_uploaded_file(file, "pdf")
        assert content == FILE_CONTENT+'\n'


def test_read_uploaded_doc_file(generate_doc_file):
    file_path = generate_doc_file
    with open(file_path, "rb") as file:
        content = read_uploaded_file(file, "docx")
        assert content == FILE_CONTENT+'\n'