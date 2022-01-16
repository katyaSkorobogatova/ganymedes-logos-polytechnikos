from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from .models import Article, Magazine, Review
import re
from .util import *
from django.contrib.auth.decorators import login_required, user_passes_test

from datetime import datetime

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
    try:
        article_instance = Article.objects.get(pk=id)
        if article_instance.status == "published" or article_instance.id_autor.pk == request.user.id:
            return render(request, "article.html", {})
        elif article_instance.status == "in review" and is_reviewer(request.user):
            return render(request, "article_review.html", {})
        elif article_instance.status == "reviewed" and (is_reviewer(request.user) or is_editor(request.user)):
            return render(request, "article.html", {})
        else:
            raise Http404

    except Article.DoesNotExist:
        raise Http404



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
    try:
        article_instance = Article.objects.get(pk=id)
        if article_instance.status == "published" or article_instance.id_autor.pk == request.user.id or \
                (article_instance.status == "in review" and is_reviewer(request.user) or is_editor(request.user)) or \
                (article_instance.status == "reviewed" and (is_reviewer(request.user) or is_editor(request.user))):

            data = serializers.serialize('json', [article_instance])
            data = data.replace('"id_autor": {}'.format(article_instance.id_autor.pk), '"autor": "{} {}"'.format(article_instance.id_autor.first_name,
                                                                                              article_instance.id_autor.last_name))
            data = re.sub(r"(\d{4})-(\d{1,2})-(\d{1,2})", r'\3-\2-\1', data)
            return JsonResponse(data, safe=False)
        else:
            raise Http404
    except Article.DoesNotExist:
        raise Http404

def review_request(request, id):
    try:
        review_instance = Review.objects.get(pk=id)

        data = serializers.serialize('json', [review_instance])
        data = data.replace('"id_reviewer": {}'.format(review_instance.id_reviewer.pk),
                            '"reviewer": "{} {}"'.format(review_instance.id_reviewer.first_name,
                                                      review_instance.id_reviewer.last_name))

        return JsonResponse(data, safe=False)

    except Article.DoesNotExist:
        raise Http404

def article_list_request(request, id):
    data = []

    for q in Article.objects.all():
        
        if q.magazine_number is not None:
            if q.magazine_number.pk_magazine == id and q.status == "published":

                data.append({
                    "id": q.pk,
                    "title": q.name,
                    "author": q.id_autor.first_name + ' ' + q.id_autor.last_name,
                    "text": q.text[:100] + "...",
                    "date_of_create": q.date_of_create.strftime("%d-%m-%Y")
                })

    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_author)
def article_new(request):

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        article_instance = Article(id_autor=user, name=request.POST['name'],
                                   text=request.POST['text'], status="draft",
                                    date_of_create=datetime.now(), edited=0)
        article_instance.save()
        return redirect('/article/{}/'.format(article_instance.pk_article))

    else:
        return render(request, "new.html", {})


@login_required
@user_passes_test(is_author)
def article_delete(request, id):
    try:
        article_instance = Article.objects.get(pk=id)
        if article_instance.id_autor.pk == request.user.id and article_instance.status == "draft":
            article_instance.delete()
            return redirect('articles_my')
        else:
            raise Http404
    except Article.DoesNotExist:
        raise Http404


@login_required
@user_passes_test(is_author)
def articles_my(request):
    return render(request, "my.html", {})


@login_required
@user_passes_test(is_author)
def author_article_list_request(request):
    data = []

    for q in Article.objects.all():
        if q.id_autor.pk == request.user.id:
            status = "None"
            if q.status == "published":
                status = "Zveřejněno"
            elif q.status == "draft":
                status = "Návrh"
            elif q.status == "in review":
                status = "V recenzi"
            elif q.status == "reviewed":
                status = "Recenzovaný"
            data.append({
                "id": q.pk,
                "title": q.name,
                "text": q.text[:100] + "...",
                "date_of_create": q.date_of_create.strftime("%d-%m-%Y"),
                "status": status
            })

    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_author)
def to_review(request, id):
    try:
        article_instance = Article.objects.get(pk=id)
        if article_instance.id_autor.pk == request.user.id:
            article_instance.status = "in review"
            article_instance.date_of_create = datetime.now()
            article_instance.save()
            return redirect('articles_my')
        else:
            raise Http404
    except Article.DoesNotExist:
        raise Http404


@login_required
@user_passes_test(is_author)
def article_edit(request, id):
    try:

        article_instance = Article.objects.get(pk=id)
        if (article_instance.id_autor.pk == request.user.id and article_instance.status == "draft") and\
                (is_editor(request.user) and article_instance.status == "in review"):
            if request.method == 'POST':
                article_instance.name = request.POST.get('name')
                article_instance.text = request.POST.get('text')
                if is_editor(request.user):
                    article_instance.id_editor = request.user
                article_instance.save()
                return redirect('/article/{}/'.format(article_instance.pk_article))
            else:
                return render(request, "edit.html", {})
        else:
            raise Http404
    except Article.DoesNotExist:
        raise Http404


@login_required
@user_passes_test(is_reviewer)
def reviewer_article_list_request(request):
    data = []

    for q in Article.objects.all():
        if q.status == "in review" and q.id_reviewer.pk == request.user.id :

            data.append({
                "id": q.pk,
                "title": q.name,
                "text": q.text[:100] + "...",
                "date_of_create": q.date_of_create.strftime("%d-%m-%Y"),
                "author": q.id_autor.first_name + ' ' + q.id_autor.last_name,
            })

    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_reviewer)
def new_review_view(request, id):
    try:

        article_instance = Article.objects.get(pk=id)
        if article_instance.status != "to review":
            if request.method == 'POST':
                user = User.objects.get(id=request.user.id)
                review_instance = Review(pk_article=id,  id_reviewer=user,
                                         relevancy=request.POST['relevancy'],
                                         interesting=request.POST['interesting'], usefulness=request.POST['usefulness'],
                                         originality=request.POST['originality'],
                                         proffesional_level=request.POST['proffesional_level'],
                                         language_level=request.POST['language_level'],
                                         stylistic_level=request.POST['stylistic_level'],
                                         commentary=request.POST['commentary']
                                         )
                review_instance.save()
                article_instance.id_review = review_instance
                article_instance.status = "reviewed"
                article_instance.save()
                return redirect('/article/{}/'.format(article_instance.pk_article))

            else:
                return render(request, "new_review.html", {})
        else:
            raise Http404
    except Article.DoesNotExist:
        raise Http404


@login_required
@user_passes_test(is_editor)
def set_reviewer(request):
    try:
        if request.method == 'POST':
            user = User.objects.get(id=request.POST['reviewer'])
            article = Article.objects.get(pk=request.POST['article'])
            article.id_reviewer = user
            article.id_editor = request.user
            article.save()
    except Article.DoesNotExist:
        raise Http404
    except User.DoesNotExist:
        raise Http404


@login_required
@user_passes_test(is_editor)
def editor_article_inreview_list_request(request):
    data = []
    for q in Article.objects.all():
        if q.status == "in review":
            data.append({
                "id": q.pk,
                "title": q.name,
                "text": q.text[:100] + "...",
                "date_of_create": q.date_of_create.strftime("%d-%m-%Y"),
                "author": q.id_autor.first_name + ' ' + q.id_autor.last_name

            })

    return JsonResponse(data, safe=False)

@login_required
@user_passes_test(is_editor)
def editor_article_inreview_list_view(request):
    return render(request, "inreview.html", {})



@login_required
@user_passes_test(is_editor)
def editor_article_reviewed_list_request(request):
    data = []
    for q in Article.objects.all():
        if q.status == "reviewed":
            data.append({
                "id": q.pk,
                "title": q.name,
                "text": q.text[:100] + "...",
                "date_of_create": q.date_of_create.strftime("%d-%m-%Y"),
                "author": q.id_autor.first_name + ' ' + q.id_autor.last_name,
                "reviewer": q.id_reviewer.first_name + ' ' + q.id_reviewer.last_name
            })

    return JsonResponse(data, safe=False)

@login_required
@user_passes_test(is_editor)
def editor_article_reviewed_list_view(request):
    return render(request, "reviewed.html", {})

@login_required
@user_passes_test(is_editor)
def editor_rewiewer_list_request(request):
    data = []

    for q in User.objects.all():
        if is_reviewer(q):
            data.append({
                "id": q.pk,
                "name":  q.first_name + ' ' + q.last_name

            })

    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_editor)
def to_draft(request, id):
    try:
        article_instance = Article.objects.get(pk=id)
        article_instance.status = "draft"
        article_instance.save()
        return redirect('pending')

    except Article.DoesNotExist:
        raise Http404

