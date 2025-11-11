#!/usr/bin/env python
"""
Script to add authors and books to MongoDB
Run this script while Django server is running
"""

import requests
import json
from datetime import date

# API endpoints
BASE_URL = "http://localhost:8000/api/mongo"
AUTHORS_URL = f"{BASE_URL}/authors/"
BOOKS_URL = f"{BASE_URL}/books/"

# Console colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def add_author(name, email, bio=""):
    """Add an author to MongoDB"""
    author_data = {
        "name": name,
        "email": email,
        "bio": bio
    }
    
    try:
        response = requests.post(
            AUTHORS_URL,
            json=author_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success(f"Author '{name}' created successfully!")
            print_info(f"Author ID: {data.get('id')}")
            return data.get('id')
        else:
            print_error(f"Failed to create author: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to Django server.")
        print_warning("Make sure Django server is running: python manage.py runserver")
        return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def add_book(title, author_id, price, isbn, published_date=None, is_available=True):
    """Add a book to MongoDB"""
    if published_date is None:
        published_date = str(date.today())
    
    book_data = {
        "title": title,
        "author_id": author_id,
        "price": price,
        "isbn": isbn,
        "published_date": published_date,
        "is_available": is_available
    }
    
    try:
        response = requests.post(
            BOOKS_URL,
            json=book_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success(f"Book '{title}' created successfully!")
            print_info(f"Book ID: {data.get('id')}")
            return data.get('id')
        else:
            print_error(f"Failed to create book: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to Django server.")
        print_warning("Make sure Django server is running: python manage.py runserver")
        return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def get_all_authors():
    """Fetch all authors from MongoDB"""
    try:
        response = requests.get(AUTHORS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print_error(f"Failed to fetch authors: {response.status_code}")
            return []
    except Exception as e:
        print_error(f"Error fetching authors: {e}")
        return []

def get_all_books():
    """Fetch all books from MongoDB"""
    try:
        response = requests.get(BOOKS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print_error(f"Failed to fetch books: {response.status_code}")
            return []
    except Exception as e:
        print_error(f"Error fetching books: {e}")
        return []

def main():
    """Main function to add sample data"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}📚 MongoDB Data Import Script{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    # Add Authors
    print(f"{Colors.BOLD}Adding Authors...{Colors.END}\n")
    
    authors = [
        {
            "name": "Haseeb Jan",
            "email": "haseeb@example.com",
            "bio": "Expert Django developer specializing in MongoDB integration"
        },
        {
            "name": "Sarah Ahmed",
            "email": "sarah@example.com",
            "bio": "Full-stack developer with expertise in Python and JavaScript"
        },
        {
            "name": "Ali Khan",
            "email": "ali@example.com",
            "bio": "Backend specialist focusing on scalable architectures"
        }
    ]
    
    author_ids = []
    for author in authors:
        author_id = add_author(author["name"], author["email"], author["bio"])
        if author_id:
            author_ids.append(author_id)
        print()
    
    # Check if we have authors
    if not author_ids:
        print_error("No authors were created. Exiting...")
        return
    
    # Add Books
    print(f"\n{Colors.BOLD}Adding Books...{Colors.END}\n")
    
    books = [
        {
            "title": "Django for Beginners",
            "price": 29.99,
            "isbn": "9781234567890",
            "published_date": "2024-01-15"
        },
        {
            "title": "MongoDB Essentials",
            "price": 39.99,
            "isbn": "9781234567891",
            "published_date": "2024-02-20"
        },
        {
            "title": "Full Stack Development",
            "price": 49.99,
            "isbn": "9781234567892",
            "published_date": "2024-03-10"
        },
        {
            "title": "Python Best Practices",
            "price": 34.99,
            "isbn": "9781234567893",
            "published_date": "2024-04-05"
        },
        {
            "title": "REST API Design",
            "price": 44.99,
            "isbn": "9781234567894",
            "published_date": "2024-05-12"
        }
    ]
    
    # Distribute books among authors
    for i, book in enumerate(books):
        author_id = author_ids[i % len(author_ids)]
        add_book(
            book["title"],
            author_id,
            book["price"],
            book["isbn"],
            book["published_date"]
        )
        print()
    
    # Display summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}📊 Summary{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    all_authors = get_all_authors()
    all_books = get_all_books()
    
    print_info(f"Total Authors: {len(all_authors)}")
    print_info(f"Total Books: {len(all_books)}")
    
    print(f"\n{Colors.BOLD}Authors in Database:{Colors.END}")
    for author in all_authors:
        name = author.get('name', 'Unknown')
        email = author.get('email', 'No email')
        author_id = author.get('_id', 'No ID')
        print(f"  📝 {name} ({email})")
        print(f"     ID: {author_id}")
    
    print(f"\n{Colors.BOLD}Books in Database:{Colors.END}")
    for book in all_books:
        title = book.get('title', 'Unknown')
        price = book.get('price', 0)
        isbn = book.get('isbn', 'No ISBN')
        book_id = book.get('_id', 'No ID')
        print(f"  📚 {title} - ${price}")
        print(f"     ISBN: {isbn} | ID: {book_id}")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Data import completed successfully!{Colors.END}\n")

if __name__ == "__main__":
    main()