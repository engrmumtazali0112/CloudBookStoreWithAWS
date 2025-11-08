from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book, AuthorProfile
from datetime import date
from decimal import Decimal


class AuthorModelTest(TestCase):
    """Test cases for Author model"""
    
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            email="john@example.com",
            bio="A great author"
        )
    
    def test_author_creation(self):
        """Test author is created correctly"""
        self.assertEqual(self.author.name, "John Doe")
        self.assertEqual(self.author.email, "john@example.com")
        self.assertTrue(AuthorProfile.objects.filter(author=self.author).exists())
    
    def test_author_str(self):
        """Test author string representation"""
        self.assertEqual(str(self.author), "John Doe")


class BookModelTest(TestCase):
    """Test cases for Book model"""
    
    def setUp(self):
        self.author = Author.objects.create(
            name="Jane Smith",
            email="jane@example.com"
        )
        self.book = Book.objects.create(
            title="Django for Beginners",
            author=self.author,
            price=Decimal('29.99'),
            published_date=date(2024, 1, 1),
            isbn="1234567890123",
            is_available=True
        )
    
    def test_book_creation(self):
        """Test book is created correctly"""
        self.assertEqual(self.book.title, "Django for Beginners")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.price, Decimal('29.99'))
    
    def test_book_str(self):
        """Test book string representation"""
        self.assertEqual(str(self.book), "Django for Beginners")
    
    def test_author_stats_updated(self):
        """Test that author stats are updated when book is created"""
        profile = self.author.profile
        self.assertEqual(profile.total_books, 1)
        self.assertEqual(profile.total_revenue, Decimal('29.99'))


class AuthorAPITest(APITestCase):
    """Test cases for Author API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author_data = {
            'name': 'Test Author',
            'email': 'test@example.com',
            'bio': 'Test bio'
        }
        self.author = Author.objects.create(**self.author_data)
    
    def test_get_authors_list(self):
        """Test retrieving list of authors"""
        url = reverse('codegraphers:author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_author_detail(self):
        """Test retrieving a single author"""
        url = reverse('codegraphers:author-detail', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
    
    def test_create_author_authenticated(self):
        """Test creating an author with authentication"""
        self.client.force_authenticate(user=self.user)
        url = reverse('codegraphers:author-list')
        new_author = {
            'name': 'New Author',
            'email': 'new@example.com',
            'bio': 'New bio'
        }
        response = self.client.post(url, new_author)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
    
    def test_create_author_unauthenticated(self):
        """Test that unauthenticated users cannot create authors"""
        url = reverse('codegraphers:author-list')
        new_author = {
            'name': 'New Author',
            'email': 'new2@example.com'
        }
        response = self.client.post(url, new_author)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_author_books(self):
        """Test getting books by author"""
        Book.objects.create(
            title="Test Book",
            author=self.author,
            price=Decimal('19.99'),
            published_date=date.today(),
            isbn="9876543210123"
        )
        url = reverse('codegraphers:author-books', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class BookAPITest(APITestCase):
    """Test cases for Book API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(
            name='Test Author',
            email='author@example.com'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            price=Decimal('29.99'),
            published_date=date(2024, 1, 1),
            isbn='1234567890123',
            is_available=True
        )
    
    def test_get_books_list(self):
        """Test retrieving list of books"""
        url = reverse('codegraphers:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_books_by_availability(self):
        """Test filtering books by availability"""
        url = reverse('codegraphers:book-list')
        response = self.client.get(url, {'available': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        url = reverse('codegraphers:book-list')
        response = self.client.get(url, {'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_mark_book_unavailable(self):
        """Test marking book as unavailable"""
        self.client.force_authenticate(user=self.user)
        url = reverse('codegraphers:book-mark-unavailable', args=[self.book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_available)
    
    def test_search_books(self):
        """Test searching books by title"""
        url = reverse('codegraphers:book-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)


class SignalsTest(TestCase):
    """Test cases for Django signals"""
    
    def test_author_profile_created_on_author_creation(self):
        """Test that profile is automatically created when author is created"""
        author = Author.objects.create(
            name="Signal Test Author",
            email="signal@example.com"
        )
        self.assertTrue(AuthorProfile.objects.filter(author=author).exists())
    
    def test_author_stats_updated_on_book_creation(self):
        """Test that author stats are updated when book is created"""
        author = Author.objects.create(
            name="Stats Test Author",
            email="stats@example.com"
        )
        Book.objects.create(
            title="Book 1",
            author=author,
            price=Decimal('10.00'),
            published_date=date.today(),
            isbn="1111111111111"
        )
        profile = author.profile
        self.assertEqual(profile.total_books, 1)
        self.assertEqual(profile.total_revenue, Decimal('10.00'))
        
        Book.objects.create(
            title="Book 2",
            author=author,
            price=Decimal('20.00'),
            published_date=date.today(),
            isbn="2222222222222"
        )
        profile.refresh_from_db()
        self.assertEqual(profile.total_books, 2)
        self.assertEqual(profile.total_revenue, Decimal('30.00'))
    
    def test_author_stats_updated_on_book_deletion(self):
        """Test that author stats are updated when book is deleted"""
        author = Author.objects.create(
            name="Delete Test Author",
            email="delete@example.com"
        )
        book = Book.objects.create(
            title="Book to Delete",
            author=author,
            price=Decimal('15.00'),
            published_date=date.today(),
            isbn="3333333333333"
        )
        profile = author.profile
        self.assertEqual(profile.total_revenue, Decimal('15.00'))
        
        book.delete()
        profile.refresh_from_db()
        self.assertEqual(profile.total_books, 0)
        self.assertEqual(profile.total_revenue, Decimal('0.00'))