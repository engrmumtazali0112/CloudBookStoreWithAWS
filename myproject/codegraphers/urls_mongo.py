from django.urls import path
from .views_mongo import (
    MongoAuthorListView,
    MongoAuthorDetailView,
    MongoBookListView,
    MongoBookDetailView
)

urlpatterns = [
    # Author endpoints
    path('mongo/authors/', MongoAuthorListView.as_view(), name='mongo-author-list'),
    path('mongo/authors/<str:author_id>/', MongoAuthorDetailView.as_view(), name='mongo-author-detail'),
    
    # Book endpoints
    path('mongo/books/', MongoBookListView.as_view(), name='mongo-book-list'),
    path('mongo/books/<str:book_id>/', MongoBookDetailView.as_view(), name='mongo-book-detail'),
]