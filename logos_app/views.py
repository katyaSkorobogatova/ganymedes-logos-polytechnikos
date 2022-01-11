from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from .models import Article, Magazine
import re
from util import is_author
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

def home_view(request):
    return render(request, "index.html", {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            # messages.success(request, "error: Login failed")
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        return HttpResponseForbidden()


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
        return render(request, "article.html", {})


def magazine_view(request, id):
    a_list = []
    for art in Magazine.objects.all():
        a_list.append(art.pk)
    if id not in a_list:
        raise Http404
    else:
        return render(request, "magazine.html", {})


def magazine_list_request(request):
    data = []

    for q in Magazine.objects.all():
        if q.published == 1:
            data.append({
                "id": q.pk,
                "release_date": q.release_date.strftime("%d-%m-%Y")
            })

    return JsonResponse(data, safe=False)


def article_request(request, id):
    queryset = Article.objects.get(pk=id)
    author = User.objects.get(pk=queryset.id_autor)
    data = serializers.serialize('json', [queryset])
    data = data.replace('"id_autor": {}'.format(author.pk), '"autor": "{} {}"'.format(author.first_name,
                                                                                      author.last_name))
    data = re.sub(r"(\d{4})-(\d{1,2})-(\d{1,2})", r'\3-\2-\1', data)
    return JsonResponse(data, safe=False)


def article_list_request(request, id):
    data = []

    for q in Article.objects.all():
        if q.magazine_number == id:
            author = User.objects.get(pk=q.id_autor)
            data.append({
                "id": q.pk,
                "title": q.name,
                "author": author.first_name + ' ' + author.last_name,
                "text": q.text[:100] + "...",
                "date_of_create": q.date_of_create.strftime("%d-%m-%Y")
            })

    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_author)
def article_new(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, "new.html", {})


@login_required
@user_passes_test(is_author)
def articles_my(request):
    return render(request, "my.html", {})


@login_required
@user_passes_test(is_author)
def author_article_list_request(request):
    data = []

    for q in Article.objects.all():
        if q.id_autor == request.user.id:

            data.append({
                "id": q.pk,
                "title": q.name,
                "text": q.text[:100] + "...",
                "date_of_create": q.date_of_create.strftime("%d-%m-%Y"),
                "status": q.status
            })

    return JsonResponse(data, safe=False)
