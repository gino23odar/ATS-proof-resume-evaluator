from . import views
from django.urls import path
from .api import UploadResumeView, UploadAdView, APICHECK

urlpatterns = [
    path('', views.home, name='home_page'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('upload-ad/', views.upload_ad, name='upload_ad'),
    path('api/upload-resume/', UploadResumeView.as_view(), name='api_upload_resume'),
    path('api/upload-ad/', UploadAdView.as_view(), name='api_upload_ad'),
    path('api/check/', APICHECK.as_view(), name='api_check'),
]