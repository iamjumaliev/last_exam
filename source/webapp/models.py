from django.contrib.auth.models import User
from django.db import models

class File(models.Model):
    file = models.FileField(upload_to='uploads/files',null=False,blank=False,
                                verbose_name='Задание')
    name = models.CharField(max_length=2500, null=False, blank=False, verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='file_author',
                               null=True, blank=True, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

# Create your models here.
