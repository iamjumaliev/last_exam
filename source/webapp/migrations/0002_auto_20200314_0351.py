# Generated by Django 2.2 on 2020-03-14 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='uploads/files', verbose_name='Задание'),
        ),
    ]
