from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, AuthorProfileViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'profiles', AuthorProfileViewSet, basename='authorprofile')

app_name = 'codegraphers'

urlpatterns = [
    path('', include(router.urls)),
]

# Generated URLs:
# GET    /authors/                    - List all authors
# POST   /authors/                    - Create new author
# GET    /authors/{id}/               - Retrieve author details
# PUT    /authors/{id}/               - Update author
# PATCH  /authors/{id}/               - Partial update author
# DELETE /authors/{id}/               - Delete author
# GET    /authors/{id}/books/         - Get author's books
# GET    /authors/{id}/statistics/    - Get author statistics
# GET    /authors/top_authors/        - Get top authors

# GET    /books/                      - List all books (with filters)
# POST   /books/                      - Create new book
# GET    /books/{id}/                 - Retrieve book details
# PUT    /books/{id}/                 - Update book
# PATCH  /books/{id}/                 - Partial update book
# DELETE /books/{id}/                 - Delete book
# POST   /books/{id}/mark_unavailable/ - Mark book unavailable
# POST   /books/{id}/mark_available/   - Mark book available
# GET    /books/recent/               - Get recent books

# GET    /profiles/                   - List all profiles
# GET    /profiles/{id}/              - Retrieve profile details
# GET    /profiles/verified/          - Get verified profiles
# GET    /profiles/top_earners/       - Get top earning authors