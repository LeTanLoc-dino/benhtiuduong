# Generated by Django 2.1.15 on 2024-04-03 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ungdung_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='password',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='username',
        ),
    ]