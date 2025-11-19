from django.urls import path, include
from .views import todo_list


app_name = 'todo'

urlpatterns = [
    path('', todo_list, name= 'homepage.html')

]