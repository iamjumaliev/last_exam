# Generated by Django 2.2 on 2020-03-14 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20200314_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='access',
            field=models.CharField(choices=[('shared', 'общий'), ('secured', 'скрытый'), ('private', 'приватный')], default='shared', max_length=25, verbose_name='Доступ'),
        ),
    ]
