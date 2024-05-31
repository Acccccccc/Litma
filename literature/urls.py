# literature/urls.py

from django.urls import path
from . import views


app_name = 'literature'
urlpatterns = [
    path('', views.literature_list, name='literature_list'),
    path('literature/<int:pk>/', views.literature_detail, name='literature_detail'),
    path('literature/create/', views.literature_create, name='literature_create'),
    path('literature/<int:pk>/update/', views.literature_update, name='literature_update'),
    path('literature/<int:pk>/delete/', views.literature_delete, name='literature_delete'),
    path('literature/<int:pk>/upload_attachment/', views.upload_attachment, name='upload_attachment'),
    path('import/', views.literature_import, name='literature_import'),
    
]
