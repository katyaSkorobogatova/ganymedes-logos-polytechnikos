from django.contrib import admin


from .models import (Article, Magazine, Review)


# Register your models here.
admin.site.register(Article)
admin.site.register(Magazine)
admin.site.register(Review)
