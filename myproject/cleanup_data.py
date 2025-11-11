#!/usr/bin/env python
"""
Cleanup script to remove all data from MongoDB
Use this to start fresh
"""

import requests
import json

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

def get_all_authors():
    """Get all authors"""
    try:
        response = requests.get(AUTHORS_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print_error(f"Error fetching authors: {e}")
        return []

def get_all_books():
    """Get all books"""
    try:
        response = requests.get(BOOKS_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print_error(f"Error fetching books: {e}")
        return []

def delete_author(author_id):
    """Delete an author"""
    try:
        response = requests.delete(f"{AUTHORS_URL}{author_id}/")
        return response.status_code in [200, 204]
    except Exception as e:
        print_error(f"Error deleting author: {e}")
        return False

def delete_book(book_id):
    """Delete a book"""
    try:
        response = requests.delete(f"{BOOKS_URL}{book_id}/")
        return response.status_code in [200, 204]
    except Exception as e:
        print_error(f"Error deleting book: {e}")
        return False

def main():
    """Main cleanup function"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.RED}🗑️  MongoDB Data Cleanup{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    # Get current data
    authors = get_all_authors()
    books = get_all_books()
    
    print_info(f"Found {len(authors)} authors")
    print_info(f"Found {len(books)} books")
    
    if len(authors) == 0 and len(books) == 0:
        print_success("Database is already empty!")
        return
    
    # Ask for confirmation
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print_warning("This will DELETE ALL data from MongoDB!")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}")
    
    confirmation = input("\nType 'DELETE' to confirm: ")
    
    if confirmation != 'DELETE':
        print_info("Cleanup cancelled.")
        return
    
    print(f"\n{Colors.BOLD}Deleting data...{Colors.END}\n")
    
    # Delete all books first
    book_deleted = 0
    for book in books:
        book_id = book.get('_id')
        if book_id:
            if delete_book(book_id):
                book_deleted += 1
                title = book.get('title', 'Unknown')
                print(f"  🗑️  Deleted book: {title}")
    
    print(f"\n{Colors.GREEN}Deleted {book_deleted} books{Colors.END}\n")
    
    # Delete all authors
    author_deleted = 0
    for author in authors:
        author_id = author.get('_id')
        if author_id:
            if delete_author(author_id):
                author_deleted += 1
                name = author.get('name', 'Unknown')
                print(f"  🗑️  Deleted author: {name}")
    
    print(f"\n{Colors.GREEN}Deleted {author_deleted} authors{Colors.END}")
    
    # Verify cleanup
    print(f"\n{Colors.BOLD}Verifying cleanup...{Colors.END}")
    remaining_authors = get_all_authors()
    remaining_books = get_all_books()
    
    if len(remaining_authors) == 0 and len(remaining_books) == 0:
        print_success("\n✨ Database cleaned successfully!")
        print_info("You can now run 'python add_data.py' to add fresh data")
    else:
        print_warning(f"\nWarning: {len(remaining_authors)} authors and {len(remaining_books)} books still remain")
    
    print()

if __name__ == "__main__":
    main()