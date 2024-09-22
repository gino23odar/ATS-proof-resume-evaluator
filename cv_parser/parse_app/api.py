from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from .validators import validate_file_extension, validate_file_size
from .utils import read_uploaded_file, extract_resume_info, extract_resume_insights

class APICHECK(APIView):
    def get(self, request):
        return JsonResponse({'message': 'API is working'}, status=200)

# Upload Resume View
class UploadResumeView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file was uploaded."}, status=400)
        
        try:
            ext = validate_file_extension(file)
            validate_file_size(file)
            file_content = read_uploaded_file(file, ext)
            data = extract_resume_info(file_content)
            return JsonResponse(data, status=200)
        except ValidationError as e:
            return JsonResponse({"error": e.message}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An error occurred while processing the file."}, status=500)

# Upload Ad View
class UploadAdView(APIView):
    def post(self, request):
        ad_description = request.data.get('ad-description', 'No ad-description')
        resume_data = request.data.get('resume-data', 'No resume-data')

        if not ad_description:
            return JsonResponse({'error': 'Missing ad description'}, status=400)
        if not resume_data:
            return JsonResponse({'error': 'Missing resume data'}, status=400)

        data = extract_resume_insights(resume_data, ad_description)
        return JsonResponse(data, status=200)
