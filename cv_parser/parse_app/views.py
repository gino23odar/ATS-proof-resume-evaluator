from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from .validators import validate_file_extension, validate_file_size
from .utils import read_uploaded_file, extract_resume_info, extract_resume_insights

# Create your views here.

def home(request: HttpRequest):
    return render(request, 'home.html')

def upload_resume(request: HttpRequest):
    if request.method == "POST" and request.FILES.get("file"):
        file: UploadedFile = request.FILES["file"]
        try:
            ext: str = validate_file_extension(file)
            validate_file_size(file)
            file_content = read_uploaded_file(file, ext)
            #print(file_content)
            data = extract_resume_info(file_content)
            return JsonResponse(data, status=200)
        except ValidationError as e:
            return JsonResponse({"error": e.message}, status=400)
    return JsonResponse ({"error": "Invalid Request"}, status=400)


def upload_ad(request: HttpRequest):
    if request.method == 'POST':
        # Handle form data
        ad_description = request.POST.get('ad-description', 'No ad-description')
        resume_data = request.POST.get('resume-data', 'No resume-data')
        #print(request)

        print("Form data - ad-description:", ad_description)
        print(type(ad_description))
        print(type(resume_data))
        print("Form data - resume-data:", resume_data)
        #print("Request headers:", dict(request.headers))

        data = extract_resume_insights(resume_data, ad_description)

        # Handle the form data here as needed
        # Example response based on data presence
        if not ad_description:
            return JsonResponse({'error': 'Missing ad description'}, status=400)
        if not resume_data:
            return JsonResponse({'error': 'Missing resume data'}, status=400)
        
        return JsonResponse(data, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)