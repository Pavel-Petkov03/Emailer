# Generated by Django 4.0.2 on 2022-03-30 14:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_preferences_hobby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='hobby',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]
