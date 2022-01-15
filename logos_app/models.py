# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    pk_article = models.AutoField(primary_key=True)
    id_autor = models.ForeignKey(User, models.DO_NOTHING, related_name="autor", db_column='id_autor')
    name = models.CharField(max_length=255)
    magazine_number = models.ForeignKey('Magazine', models.DO_NOTHING, db_column='magazine_number', blank=True, null=True)
    text = models.TextField()
    date_of_create = models.DateField()
    edited = models.IntegerField()
    status = models.CharField(max_length=9, blank=True, null=True)
    id_editor = models.ForeignKey(User, models.DO_NOTHING, related_name="editor", db_column='id_editor', blank=True, null=True)
    id_review = models.ForeignKey('Review', models.DO_NOTHING, db_column='id_review', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article'



class Magazine(models.Model):
    pk_magazine = models.AutoField(primary_key=True)
    magazine_number = models.IntegerField()
    release_date = models.DateField(blank=True, null=True)
    published = models.IntegerField()
    max_number_of_magazine = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'magazine'


class Review(models.Model):
    pk_review = models.AutoField(primary_key=True)
    id_reviewer = models.ForeignKey(User, models.DO_NOTHING, related_name="reviewer", db_column='id_reviewer')
    relevancy = models.IntegerField()
    interesting = models.IntegerField()
    usefulness = models.IntegerField()
    originality = models.IntegerField()
    proffesional_level = models.IntegerField()
    language_level = models.IntegerField()
    stylistic_level = models.IntegerField()
    commentary = models.TextField()

    class Meta:
        managed = False
        db_table = 'review'
