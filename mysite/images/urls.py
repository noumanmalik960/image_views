from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    path('', views.list, name='list'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('ranking/', views.image_ranking, name='create'),

]