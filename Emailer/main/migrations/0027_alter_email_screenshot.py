# Generated by Django 4.0.2 on 2022-03-25 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_email_screenshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='screenshot',
            field=models.URLField(),
        ),
    ]
