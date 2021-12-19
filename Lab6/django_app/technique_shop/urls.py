from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('technique/', views.get_technique_list, name="technique_list"),
    path('technique/<int:technique_id>', views.get_technique_by_id, name="technique_get_id"),
    path('about/', views.get_about_info, name='about_info'),
]
