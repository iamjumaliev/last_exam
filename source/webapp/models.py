from django.contrib.auth.models import User
from django.db import models


ACCESS_CHOICES = [
    ('shared', 'общий'),
    ('secured', 'скрытый'),
    ('private', 'приватный')
]

class File(models.Model):
    file = models.FileField(upload_to='uploads/files',null=False,blank=False,
                                verbose_name='Задание')
    name = models.CharField(max_length=2500, null=False, blank=False, verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='file_author',
                               null=True, blank=True, verbose_name='Автор')
    access = models.CharField(max_length=25,choices=ACCESS_CHOICES, default=ACCESS_CHOICES[0][0], verbose_name='Доступ',
                            null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

# Create your models here.
