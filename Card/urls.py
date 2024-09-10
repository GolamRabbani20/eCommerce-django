from django.urls import path
from . import views

urlpatterns = [
    path('', views.cardSummery, name='card_summery'),
    path('add/', views.cardAdd, name='card_add'),
    path('update/', views.cardUpdate, name='card_update'),
    path('delete/', views.cardDelete, name='card_delete'),
]
