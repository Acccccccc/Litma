# Generated by Django 5.0.6 on 2024-05-31 08:16

import django.db.models.deletion
import django.utils.timezone
import literature.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal_fullname', models.CharField(max_length=200)),
                ('journal_abbr', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Literature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('journal_abbr', models.CharField(blank=True, max_length=100)),
                ('publication_year', models.CharField(blank=True, max_length=10, null=True)),
                ('doi', models.CharField(max_length=200, unique=True)),
                ('journal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='literature.journal')),
                ('projects', models.ManyToManyField(blank=True, null=True, related_name='literatures', to='literature.project')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=literature.models.attachment_upload_path)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('literature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='literature.literature')),
            ],
        ),
    ]
