# Generated by Django 4.2.10 on 2024-03-14 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Email',
        ),
    ]
