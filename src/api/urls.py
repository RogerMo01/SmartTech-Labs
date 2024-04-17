from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('test-query/', views.test_query, name='test_query'),
]