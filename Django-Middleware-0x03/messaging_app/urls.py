from django.urls import path
from . import views

urlpatterns = [
    path('sample/', views.sample_view, name='sample_view'),
]