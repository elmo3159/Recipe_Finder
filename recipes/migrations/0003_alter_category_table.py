# Generated by Django 5.0.6 on 2024-06-05 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_category'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='categories',
        ),
    ]