# apps.app3/admin.py
from django.contrib import admin
from .models import Book
from django.contrib.auth.models import Permission


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_year', 'classification')
    search_fields = ('title', 'author', 'isbn', 'subjects')
    list_filter = ('publication_year', 'language', 'classification')



@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename", "content_type")
    search_fields = ("name", "codename")
    list_filter = ("content_type",)
