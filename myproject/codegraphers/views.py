from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import models
from django.db.models import Sum, Count

from .models import Author, Book, AuthorProfile
from .serializers import (
    AuthorSerializer, 
    AuthorDetailSerializer,
    BookSerializer, 
    BookDetailSerializer,
    AuthorProfileSerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Author model with CRUD operations
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = []  # Removed authentication requirement
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return AuthorDetailSerializer
        return AuthorSerializer
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Get all books by this author"""
        author = self.get_object()
        books = author.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get author statistics"""
        author = self.get_object()
        stats = author.books.aggregate(
            total_books=Count('id'),
            total_revenue=Sum('price'),
            available_books=Count('id', filter=models.Q(is_available=True))
        )
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def top_authors(self, request):
        """Get top authors by book count"""
        authors = Author.objects.annotate(
            book_count=Count('books')
        ).order_by('-book_count')[:10]
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model with filtering and search
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = []  # Removed authentication requirement
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer
    
    def get_queryset(self):
        """Filter books based on query parameters"""
        queryset = Book.objects.select_related('author')
        
        # Filter by availability
        is_available = self.request.query_params.get('available')
        if is_available is not None:
            queryset = queryset.filter(is_available=is_available.lower() == 'true')
        
        # Filter by author
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Search by title or ISBN
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | 
                models.Q(isbn__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_unavailable(self, request, pk=None):
        """Mark a book as unavailable"""
        book = self.get_object()
        book.is_available = False
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_available(self, request, pk=None):
        """Mark a book as available"""
        book = self.get_object()
        book.is_available = True
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recently published books"""
        books = self.get_queryset().order_by('-published_date')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet for AuthorProfile
    """
    queryset = AuthorProfile.objects.select_related('author')
    serializer_class = AuthorProfileSerializer
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get all verified author profiles"""
        profiles = self.get_queryset().filter(is_verified=True)
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_earners(self, request):
        """Get top earning authors"""
        profiles = self.get_queryset().order_by('-total_revenue')[:10]
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)