# Generated by Django 3.2.9 on 2021-11-30 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('pk_article', models.AutoField(primary_key=True, serialize=False)),
                ('id_autor', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('magazine_number', models.IntegerField()),
                ('text', models.TextField()),
                ('date_of_create', models.DateField()),
                ('edited', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(max_length=9)),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('pk_magazine', models.AutoField(primary_key=True, serialize=False)),
                ('magazine_number', models.IntegerField()),
                ('release_date', models.DateField()),
                ('published', models.IntegerField()),
                ('max_number_of_magazine', models.IntegerField()),
            ],
            options={
                'db_table': 'magazine',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('pk_review', models.AutoField(primary_key=True, serialize=False)),
                ('pk_article', models.IntegerField()),
                ('id_reviewer', models.IntegerField()),
                ('id_editor', models.IntegerField()),
                ('relevancy', models.IntegerField()),
                ('interesting', models.IntegerField()),
                ('usefulness', models.IntegerField()),
                ('originality', models.IntegerField()),
                ('proffesional_level', models.IntegerField()),
                ('language_level', models.IntegerField()),
                ('stylistic_level', models.IntegerField()),
                ('commentary', models.TextField()),
                ('status', models.CharField(max_length=11)),
            ],
            options={
                'db_table': 'review',
            },
        ),
    ]
