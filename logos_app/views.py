from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse
from .models import Article

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

def article_view(request, id):
    a_list = []
    for art in Article.objects.all():
        a_list.append(art.pk)
    if id not in a_list:
        raise Http404
    else:
        return render(request, "index.html", {})

def article_request(request, id):

    queryset = Article.objects.get(pk=id)
    data = serializers.serialize('json', [queryset])

    return JsonResponse(data, safe=False)


def article_list_request(request):

    data = []
    # queryset = Article.objects.all()
    for q in Article.objects.all():
        author = User.objects.get(pk=q.id_autor)
        data.append({
            "id": q.pk,
            "title": q.name,
            "author": author.first_name +' '+ author.last_name,
            "text": q.text[:100]

        })
    print(data)
    return JsonResponse(data, safe=False)
