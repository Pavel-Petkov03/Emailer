# Generated by Django 4.0.2 on 2022-03-10 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_email_context_email_is_deleted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='subject',
        ),
    ]
