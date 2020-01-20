from django.urls import path
from . import views

urlpatterns = [
    path('', views.sprint_list),
    path('sprint_list', views.sprint_list, name='sprint_list'),
    path('sprint_update', views.sprint_update, name='sprint_update'),
    path('week_list', views.week_list, name='week_list'),
    path('week_update', views.week_update, name='week_update'),
    path('day_list', views.day_list, name='day_list'),
    path('day_add_task', views.day_add_task, name='day_add_task'),
    path('day_update', views.day_update, name='day_update'),
    path('sprint_data', views.sprint_data, name='sprint_data'),
]