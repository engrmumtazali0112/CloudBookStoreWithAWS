# codegraphers/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from codegraphers.models import Book, Author, Publisher

@pytest.mark.django_db
class TestBookModel:
    """Test cases for Book model"""
    
    def test_create_book_success(self):
        """Test creating a book with valid data"""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            price=29.99,
            stock=10
        )
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.price == 29.99
        assert str(book) == "Test Book by Test Author"
    
    def test_book_str_method(self):
        """Test book string representation"""
        book = Book.objects.create(
            title="Python Crash Course",
            author="Eric Matthes",
            isbn="9781593279288",
            price=39.99
        )
        expected = "Python Crash Course by Eric Matthes"
        assert str(book) == expected
    
    def test_book_price_validation(self):
        """Test book price must be positive"""
        with pytest.raises(ValidationError):
            book = Book(
                title="Invalid Book",
                author="Test Author",
                isbn="1234567890123",
                price=-10.00  # Negative price
            )
            book.full_clean()
    
    def test_book_isbn_unique(self):
        """Test ISBN must be unique"""
        Book.objects.create(
            title="Book 1",
            author="Author 1",
            isbn="1234567890123",
            price=20.00
        )
        
        with pytest.raises(Exception):
            Book.objects.create(
                title="Book 2",
                author="Author 2",
                isbn="1234567890123",  # Duplicate ISBN
                price=25.00
            )
    
    def test_book_stock_default(self):
        """Test book stock defaults to 0"""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            price=29.99
        )
        assert book.stock == 0
    
    def test_book_update(self):
        """Test updating book information"""
        book = Book.objects.create(
            title="Original Title",
            author="Original Author",
            isbn="1234567890123",
            price=29.99,
            stock=5
        )
        
        book.title = "Updated Title"
        book.stock = 10
        book.save()
        
        updated_book = Book.objects.get(isbn="1234567890123")
        assert updated_book.title == "Updated Title"
        assert updated_book.stock == 10
    
    def test_book_delete(self):
        """Test deleting a book"""
        book = Book.objects.create(
            title="To Delete",
            author="Test Author",
            isbn="1234567890123",
            price=29.99
        )
        book_id = book.id
        book.delete()
        
        assert not Book.objects.filter(id=book_id).exists()
    
    def test_book_query_by_author(self):
        """Test querying books by author"""
        Book.objects.create(
            title="Book 1",
            author="John Doe",
            isbn="1111111111111",
            price=20.00
        )
        Book.objects.create(
            title="Book 2",
            author="John Doe",
            isbn="2222222222222",
            price=25.00
        )
        Book.objects.create(
            title="Book 3",
            author="Jane Smith",
            isbn="3333333333333",
            price=30.00
        )
        
        john_books = Book.objects.filter(author="John Doe")
        assert john_books.count() == 2
    
    def test_book_price_range_query(self):
        """Test querying books by price range"""
        Book.objects.create(title="Cheap Book", author="A1", isbn="1111111111111", price=10.00)
        Book.objects.create(title="Mid Book", author="A2", isbn="2222222222222", price=25.00)
        Book.objects.create(title="Expensive Book", author="A3", isbn="3333333333333", price=50.00)
        
        affordable_books = Book.objects.filter(price__lte=30.00)
        assert affordable_books.count() == 2


@pytest.mark.django_db
class TestAuthorModel:
    """Test cases for Author model if exists"""
    
    def test_author_creation(self):
        """Test creating an author"""
        # Adjust based on your actual Author model
        pass


@pytest.mark.django_db  
class TestBookQuerySets:
    """Test complex queries and aggregations"""
    
    def test_book_count(self):
        """Test counting total books"""
        Book.objects.create(title="B1", author="A1", isbn="1111111111111", price=10)
        Book.objects.create(title="B2", author="A2", isbn="2222222222222", price=20)
        
        assert Book.objects.count() == 2
    
    def test_book_ordering(self):
        """Test ordering books"""
        Book.objects.create(title="Zebra Book", author="A1", isbn="1111111111111", price=10)
        Book.objects.create(title="Alpha Book", author="A2", isbn="2222222222222", price=20)
        
        books = Book.objects.order_by('title')
        assert books.first().title == "Alpha Book"
        assert books.last().title == "Zebra Book"