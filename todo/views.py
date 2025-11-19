from django.shortcuts import render
from .models import Todo
# Create your views here.


def todo_list(request):
    todos = Todo.objects.all().order_by('title')
    context = {'todos' : todos}
    return render(request, 'homepage.html')

# def todo_detail(request, pk):
