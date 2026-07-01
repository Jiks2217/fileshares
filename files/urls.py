from django.urls import path
from . import views

app_name = 'documents'  # for reverse URL namespacing

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('retrieve/', views.retrieve, name='retrieve'),
    path('download/<str:access_code>/', views.download, name='download'),
    # Optionally, a home redirect
    path('', views.upload, name='home'),
]