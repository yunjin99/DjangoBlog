import os.path

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    hook_msg = models.TextField(blank=True)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    attached_file = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # methods
    # 기본으로 있는 __str__ 메소드를 오버라이드
    def __str__(self):
        return f'[{self.pk}] [{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f"/blog/{self.pk}"

    def get_file_name(self):
        return os.path.basename(self.attached_file.name)