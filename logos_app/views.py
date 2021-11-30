from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse


# Create your views here.

def home_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # messages.success(request, "error: Login failed")
            return redirect('home')
    else:
        return render(request, "index.html", {})


def logout_user(request):
    # messages.success(request, "YOU WERE LOGOUT")
    logout(request)
    return redirect('home')


def article_request(request):
    # queryset = User.objects.all() #temp solution for testing
    # data = serializers.serialize('json', queryset)
    data = {
        "key": "data"
    }
    return JsonResponse(data, safe=False)
