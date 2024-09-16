# Generated by Django 5.1.1 on 2024-09-16 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dealer_name', models.CharField(max_length=255)),
                ('dealer_number', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Oem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oem_name', models.CharField(max_length=255)),
                ('oem_number', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='dealer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='books.dealer'),
        ),
        migrations.AddField(
            model_name='dealer',
            name='oem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dealers', to='books.oem'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='oem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='books.oem'),
        ),
    ]
