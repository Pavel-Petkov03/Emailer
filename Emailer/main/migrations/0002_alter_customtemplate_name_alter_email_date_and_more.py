# Generated by Django 4.0.2 on 2022-03-25 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_squashed_0028_alter_receiver_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customtemplate',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='email',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.customtemplate'),
        ),
    ]
