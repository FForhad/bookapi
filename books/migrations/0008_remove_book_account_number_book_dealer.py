# Generated by Django 5.1.1 on 2024-09-16 12:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_book_account_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='account_number',
        ),
        migrations.AddField(
            model_name='book',
            name='dealer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to=settings.AUTH_USER_MODEL),
        ),
    ]
