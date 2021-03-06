import os.path

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from markdown import markdown
from markdownx.models import MarkdownxField


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/blog/tag/{self.slug}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/blog/category/{self.slug}"

    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    hook_msg = models.TextField(blank=True)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    attached_file = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # methods
    # 기본으로 있는 __str__ 메소드를 오버라이드
    def __str__(self):
        return f'[{self.pk}] [{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f"/blog/{self.pk}/"

    def get_file_name(self):
        return os.path.basename(self.attached_file.name)

    def get_markdown_content(self):
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'