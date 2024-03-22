# Generated by Django 4.2.10 on 2024-03-19 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0007_emailtracking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sent', models.IntegerField()),
                ('email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emails.email')),
            ],
        ),
    ]
