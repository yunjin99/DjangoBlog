from django.contrib import admin
from .models import Post


# Register your models here.

# admin 사이트에 Post를 등록
admin.site.register(Post)