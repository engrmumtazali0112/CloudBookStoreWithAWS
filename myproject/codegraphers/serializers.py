from rest_framework import serializers
from .models import Author, Book, AuthorProfile

class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'created_at', 'books_count']
        read_only_fields = ['created_at']

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'price', 
                  'published_date', 'isbn', 'is_available']
        
    def validate_price(self, value):
        """Additional validation for price"""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        if value > 10000:
            raise serializers.ValidationError("Price cannot exceed $10,000")
        return value

class BookDetailSerializer(BookSerializer):
    """Extended serializer with author details"""
    author_details = AuthorSerializer(source='author', read_only=True)
    
    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['author_details']
        
class AuthorProfileSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    
    class Meta:
        model = AuthorProfile
        fields = ['id', 'author', 'author_name', 'author_email', 
                  'total_books', 'total_revenue', 'is_verified']
        read_only_fields = ['total_books', 'total_revenue']

class AuthorDetailSerializer(AuthorSerializer):
    """Extended serializer with profile and books"""
    profile = AuthorProfileSerializer(read_only=True)
    books = BookSerializer(many=True, read_only=True)
    
    class Meta(AuthorSerializer.Meta):
        fields = AuthorSerializer.Meta.fields + ['profile', 'books']