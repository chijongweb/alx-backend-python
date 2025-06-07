from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from messaging_app import views

def home(request):
    return HttpResponse("Welcome to the Django Middleware Project!")

urlpatterns = [
    path('', home),  # Root URL
    path('messages/', views.sample_view, name='sample'),
    path('api/', include('messaging_app.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]