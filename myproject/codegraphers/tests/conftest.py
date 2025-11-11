# codegraphers/tests/conftest.py
import pytest
from django.test import Client

@pytest.fixture(scope='function')
def api_client():
    """
    Fixture to provide a Django test client for API testing
    """
    return Client()

@pytest.fixture(scope='function')
def sample_book(db):
    """
    Fixture to create a sample book for testing
    Import Book model inside fixture to avoid settings issues
    """
    from codegraphers.models import Book
    return Book.objects.create(
        title="Sample Book",
        author="Sample Author",
        isbn="1234567890123",
        price=29.99,
        stock=10
    )

@pytest.fixture(scope='function')
def multiple_books(db):
    """
    Fixture to create multiple books for testing
    Import Book model inside fixture to avoid settings issues
    """
    from codegraphers.models import Book
    books = []
    for i in range(5):
        book = Book.objects.create(
            title=f"Book {i+1}",
            author=f"Author {i+1}",
            isbn=f"111111111111{i}",
            price=10.00 + (i * 5),
            stock=10 + i
        )
        books.append(book)
    return books

@pytest.fixture(scope='function')
def book_data():
    """
    Fixture to provide valid book data for form/API testing
    """
    return {
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '9876543210123',
        'price': 39.99,
        'stock': 15
    }

@pytest.fixture(scope='session')
def django_db_setup():
    """
    Custom database setup for test session
    """
    pass

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enable database access for all tests
    """
    pass