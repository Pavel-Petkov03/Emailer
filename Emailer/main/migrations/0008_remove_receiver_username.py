# Generated by Django 4.0.2 on 2022-03-05 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_name_preferences_hobby_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiver',
            name='username',
        ),
    ]