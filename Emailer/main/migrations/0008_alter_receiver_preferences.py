# Generated by Django 4.0.2 on 2022-03-31 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_preferences_hobby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiver',
            name='preferences',
            field=models.ManyToManyField(blank=True, null=True, to='main.Preferences'),
        ),
    ]
