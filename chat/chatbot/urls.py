from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_document, name='upload_pdf'),
    path('ask/', views.chat_ask, name='chat_ask'),
    path('clear/', views.clear_db, name='clear_db'),
]