# Generated by Django 4.0.2 on 2022-03-10 15:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_email_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='subject',
            field=models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]
