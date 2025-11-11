#!/usr/bin/env python
"""
Clean MongoDB Database and Create Fresh Data
"""

import requests
import sys
from datetime import date, datetime

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
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def get_all_authors():
    """Get all authors"""
    try:
        response = requests.get(AUTHORS_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"{Colors.RED}Error getting authors: {e}{Colors.END}")
        return []

def get_all_books():
    """Get all books"""
    try:
        response = requests.get(BOOKS_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"{Colors.RED}Error getting books: {e}{Colors.END}")
        return []

def delete_all_books():
    """Delete all books"""
    print(f"{Colors.YELLOW}📚 Deleting all books...{Colors.END}")
    
    books = get_all_books()
    deleted_count = 0
    
    for book in books:
        book_id = book.get('_id')
        if book_id:
            try:
                response = requests.delete(f"{BOOKS_URL}{book_id}/", timeout=5)
                if response.status_code in [200, 204]:
                    deleted_count += 1
                    print(f"   ✓ Deleted: {book.get('title', 'Unknown')}")
            except Exception as e:
                print(f"   ✗ Failed to delete book {book_id}: {e}")
    
    print(f"{Colors.GREEN}✅ Deleted {deleted_count} book(s){Colors.END}\n")
    return deleted_count

def delete_all_authors():
    """Delete all authors"""
    print(f"{Colors.YELLOW}👥 Deleting all authors...{Colors.END}")
    
    authors = get_all_authors()
    deleted_count = 0
    
    for author in authors:
        author_id = author.get('_id')
        if author_id:
            try:
                response = requests.delete(f"{AUTHORS_URL}{author_id}/", timeout=5)
                if response.status_code in [200, 204]:
                    deleted_count += 1
                    print(f"   ✓ Deleted: {author.get('name', 'Unknown')}")
            except Exception as e:
                print(f"   ✗ Failed to delete author {author_id}: {e}")
    
    print(f"{Colors.GREEN}✅ Deleted {deleted_count} author(s){Colors.END}\n")
    return deleted_count

def create_sample_authors():
    """Create sample authors"""
    print(f"{Colors.CYAN}👥 Creating sample authors...{Colors.END}\n")
    
    authors_data = [
        {
            "name": "J.K. Rowling",
            "email": "jk.rowling@example.com",
            "bio": "British author, best known for the Harry Potter series"
        },
        {
            "name": "George R.R. Martin",
            "email": "george.martin@example.com",
            "bio": "American novelist and short story writer, author of A Song of Ice and Fire"
        },
        {
            "name": "Stephen King",
            "email": "stephen.king@example.com",
            "bio": "American author of horror, supernatural fiction, suspense, and fantasy novels"
        },
        {
            "name": "Agatha Christie",
            "email": "agatha.christie@example.com",
            "bio": "English writer known for her detective novels and short story collections"
        },
        {
            "name": "Isaac Asimov",
            "email": "isaac.asimov@example.com",
            "bio": "American writer and professor of biochemistry, prolific author of science fiction"
        }
    ]
    
    created_authors = []
    
    for author_data in authors_data:
        try:
            response = requests.post(AUTHORS_URL, json=author_data, timeout=5)
            if response.status_code == 201:
                result = response.json()
                author_id = result.get('id')
                created_authors.append({
                    'id': author_id,
                    'name': author_data['name']
                })
                print(f"{Colors.GREEN}✅ Created: {author_data['name']}{Colors.END}")
                print(f"   ID: {author_id}")
                print(f"   Email: {author_data['email']}\n")
            else:
                print(f"{Colors.RED}❌ Failed to create: {author_data['name']}{Colors.END}")
                print(f"   Response: {response.text}\n")
        except Exception as e:
            print(f"{Colors.RED}❌ Error creating {author_data['name']}: {e}{Colors.END}\n")
    
    return created_authors

def create_sample_books(authors):
    """Create sample books for the authors"""
    print(f"\n{Colors.CYAN}📚 Creating sample books...{Colors.END}\n")
    
    if not authors:
        print(f"{Colors.RED}❌ No authors available to create books{Colors.END}")
        return []
    
    # Books data organized by author
    books_data = {
        "J.K. Rowling": [
            {
                "title": "Harry Potter and the Philosopher's Stone",
                "price": 19.99,
                "isbn": "9780747532699",
                "published_date": "1997-06-26",
                "is_available": True
            },
            {
                "title": "Harry Potter and the Chamber of Secrets",
                "price": 19.99,
                "isbn": "9780747538493",
                "published_date": "1998-07-02",
                "is_available": True
            },
            {
                "title": "Harry Potter and the Prisoner of Azkaban",
                "price": 21.99,
                "isbn": "9780747542155",
                "published_date": "1999-07-08",
                "is_available": True
            }
        ],
        "George R.R. Martin": [
            {
                "title": "A Game of Thrones",
                "price": 24.99,
                "isbn": "9780553103540",
                "published_date": "1996-08-01",
                "is_available": True
            },
            {
                "title": "A Clash of Kings",
                "price": 24.99,
                "isbn": "9780553108033",
                "published_date": "1998-11-16",
                "is_available": True
            }
        ],
        "Stephen King": [
            {
                "title": "The Shining",
                "price": 18.99,
                "isbn": "9780385121675",
                "published_date": "1977-01-28",
                "is_available": True
            },
            {
                "title": "It",
                "price": 22.99,
                "isbn": "9780670813025",
                "published_date": "1986-09-15",
                "is_available": True
            },
            {
                "title": "The Stand",
                "price": 25.99,
                "isbn": "9780385121682",
                "published_date": "1978-10-03",
                "is_available": False
            }
        ],
        "Agatha Christie": [
            {
                "title": "Murder on the Orient Express",
                "price": 15.99,
                "isbn": "9780062693662",
                "published_date": "1934-01-01",
                "is_available": True
            },
            {
                "title": "And Then There Were None",
                "price": 14.99,
                "isbn": "9780062073488",
                "published_date": "1939-11-06",
                "is_available": True
            }
        ],
        "Isaac Asimov": [
            {
                "title": "Foundation",
                "price": 16.99,
                "isbn": "9780553293357",
                "published_date": "1951-06-01",
                "is_available": True
            },
            {
                "title": "I, Robot",
                "price": 17.99,
                "isbn": "9780553382563",
                "published_date": "1950-12-02",
                "is_available": True
            }
        ]
    }
    
    created_books = []
    
    for author in authors:
        author_name = author['name']
        author_id = author['id']
        
        if author_name in books_data:
            print(f"{Colors.BOLD}Books for {author_name}:{Colors.END}")
            
            for book_data in books_data[author_name]:
                book_data['author_id'] = author_id
                
                try:
                    response = requests.post(BOOKS_URL, json=book_data, timeout=5)
                    if response.status_code == 201:
                        result = response.json()
                        created_books.append(result)
                        status = "✓ Available" if book_data['is_available'] else "✗ Unavailable"
                        print(f"   {Colors.GREEN}✅ {book_data['title']}{Colors.END}")
                        print(f"      Price: ${book_data['price']} | {status}")
                    else:
                        print(f"   {Colors.RED}❌ Failed: {book_data['title']}{Colors.END}")
                        print(f"      Response: {response.text}")
                except Exception as e:
                    print(f"   {Colors.RED}❌ Error: {book_data['title']} - {e}{Colors.END}")
            
            print()
    
    return created_books

def show_summary():
    """Show final summary of data"""
    print_header("📊 Database Summary")
    
    authors = get_all_authors()
    books = get_all_books()
    
    print(f"{Colors.BOLD}Total Authors:{Colors.END} {len(authors)}")
    print(f"{Colors.BOLD}Total Books:{Colors.END} {len(books)}")
    
    if books:
        total_value = sum(book.get('price', 0) for book in books)
        available = sum(1 for book in books if book.get('is_available', True))
        print(f"{Colors.BOLD}Available Books:{Colors.END} {available}")
        print(f"{Colors.BOLD}Total Inventory Value:{Colors.END} ${total_value:.2f}")
    
    print(f"\n{Colors.CYAN}📋 Authors:{Colors.END}")
    for i, author in enumerate(authors, 1):
        author_books = [b for b in books if b.get('author_id') == author.get('_id')]
        print(f"   {i}. {author.get('name', 'Unknown')} ({len(author_books)} books)")
    
    print(f"\n{Colors.GREEN}✨ Database is ready to use!{Colors.END}\n")

def main():
    print_header("🧹 Clean MongoDB & Create Fresh Data")
    
    print(f"{Colors.YELLOW}This will DELETE all existing data and create sample data.{Colors.END}")
    confirm = input(f"\n{Colors.BOLD}Continue? (yes/no): {Colors.END}").strip().lower()
    
    if confirm != 'yes':
        print(f"\n{Colors.CYAN}Operation cancelled.{Colors.END}\n")
        return
    
    print()
    print_header("Step 1: Cleaning Existing Data")
    
    # Delete all books first (to avoid foreign key issues)
    books_deleted = delete_all_books()
    
    # Delete all authors
    authors_deleted = delete_all_authors()
    
    print(f"{Colors.GREEN}✅ Cleanup complete!{Colors.END}")
    print(f"   Deleted {books_deleted} books and {authors_deleted} authors\n")
    
    # Create new data
    print_header("Step 2: Creating Fresh Data")
    
    authors = create_sample_authors()
    
    if authors:
        books = create_sample_books(authors)
        
        print(f"{Colors.GREEN}✅ Sample data created!{Colors.END}")
        print(f"   Created {len(authors)} authors and {len(books)} books\n")
    else:
        print(f"{Colors.RED}❌ Failed to create authors{Colors.END}\n")
        return
    
    # Show summary
    show_summary()
    
    # Next steps
    print_header("🚀 Next Steps")
    print(f"1. {Colors.CYAN}View all data:{Colors.END}")
    print(f"   python view_data.py")
    print()
    print(f"2. {Colors.CYAN}Manage data interactively:{Colors.END}")
    print(f"   python manage_data.py")
    print()
    print(f"3. {Colors.CYAN}Access API endpoints:{Colors.END}")
    print(f"   GET  http://localhost:8000/api/mongo/authors/")
    print(f"   GET  http://localhost:8000/api/mongo/books/")
    print()
    print(f"4. {Colors.CYAN}Search books:{Colors.END}")
    print(f"   http://localhost:8000/api/mongo/books/?search=Harry")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()