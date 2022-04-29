from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Post, Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

# Register your models here.

# admin 사이트에 Post를 등록
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)