from django.contrib import admin
from .models import Author, Book, AuthorProfile

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'published_date', 'is_available']
    list_filter = ['is_available', 'published_date']
    search_fields = ['title', 'isbn']

@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ['author', 'total_books', 'total_revenue', 'is_verified']
    list_filter = ['is_verified']