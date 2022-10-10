from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
# Create your views here
# from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo
from .forms import TodoForm
from django.contrib import messages
from django.shortcuts import render, redirect
from users.models import UserProfile
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
class HomeView(TemplateView):
    template_name= "todo/home.html"

def home(request):
    todos = []
    p_data = []
    # todos = Todo.objects.all()
    if request.user.is_authenticated: 
        p_data = get_object_or_404(UserProfile, id=request.user.userprofile.id)
        # print(p_form, 'pic var mı ', bool(p_form.profile_pic))
        todos = Todo.objects.filter(user=request.user) 
 #kim veri girdiyse onun verisis gelecek
#eğer user authenticated ise ve user bizim  verileri giriğimiz user ise verileri getirecek.
    form = TodoForm()
    context = {
        "todos": todos,
        "form": form,
        "p_data": p_data,
    }
    return render(request, "todo/home.html", context)


@login_required(login_url='user_login')
def todo_create(request):
    form = TodoForm()

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo= form.save(commit=False)
            todo.user = request.user
            todo.save()
            # form.save()
            messages.success(request, "Todo created successfully")
            return redirect("home")

    context = {
        "form": form
    }
    return render(request, "todo/todo_add.html", context)


@login_required(login_url='user_login')
def todo_update(request, id):
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.warning(request, "Todo updated!")
            return redirect("home")

    context = {
        "todo": todo,
        "form": form
    }
    return render(request, "todo/todo_update.html", context)


@login_required(login_url='user_login')
def todo_delete(request, id):
    todo = Todo.objects.get(id=id)

    if request.method == "POST":
        todo.delete()
        messages.warning(request, "Todo deleted!")
        return redirect("home")

    context = {
        "todo": todo
    }
    return render(request, "todo/todo_delete.html", context)
