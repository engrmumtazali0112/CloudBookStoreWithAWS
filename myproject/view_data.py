#!/usr/bin/env python
"""
Script to view all data in MongoDB
Safe to run - only reads data, doesn't modify anything
"""

import requests
from datetime import datetime

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
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'-'*50}{Colors.END}\n")

def get_all_authors():
    """Get all authors"""
    try:
        response = requests.get(AUTHORS_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return []

def get_all_books():
    """Get all books"""
    try:
        response = requests.get(BOOKS_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return []

def format_date(date_str):
    """Format date string"""
    if not date_str:
        return "N/A"
    try:
        # Try parsing ISO format
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y")
    except:
        return date_str

def display_authors(authors):
    """Display authors in a nice format"""
    if not authors:
        print(f"{Colors.YELLOW}No authors found in database.{Colors.END}")
        return
    
    print_section(f"📚 AUTHORS ({len(authors)})")
    
    for i, author in enumerate(authors, 1):
        name = author.get('name', 'Unknown')
        email = author.get('email', 'No email provided')
        bio = author.get('bio', 'No bio')
        author_id = author.get('_id', 'N/A')
        created = author.get('created_at', '')
        
        # Count books for this author
        books = get_all_books()
        author_books = [b for b in books if b.get('author_id') == author_id]
        book_count = len(author_books)
        
        print(f"{Colors.BOLD}{i}. {name}{Colors.END}")
        print(f"   📧 Email: {email}")
        print(f"   📝 Bio: {bio[:80]}{'...' if len(bio) > 80 else ''}")
        print(f"   📚 Books: {book_count}")
        print(f"   🆔 ID: {Colors.CYAN}{author_id}{Colors.END}")
        if created:
            print(f"   📅 Created: {format_date(created)}")
        print()

def display_books(books):
    """Display books in a nice format"""
    if not books:
        print(f"{Colors.YELLOW}No books found in database.{Colors.END}")
        return
    
    print_section(f"📖 BOOKS ({len(books)})")
    
    # Get all authors for lookup
    authors = get_all_authors()
    author_map = {a.get('_id'): a.get('name', 'Unknown') for a in authors}
    
    for i, book in enumerate(books, 1):
        title = book.get('title', 'Unknown')
        author_id = book.get('author_id', '')
        author_name = author_map.get(author_id, 'Unknown Author')
        price = book.get('price', 0)
        isbn = book.get('isbn', 'N/A')
        published = book.get('published_date', '')
        available = book.get('is_available', True)
        book_id = book.get('_id', 'N/A')
        
        status = f"{Colors.GREEN}✓ Available{Colors.END}" if available else f"{Colors.RED}✗ Unavailable{Colors.END}"
        
        print(f"{Colors.BOLD}{i}. {title}{Colors.END}")
        print(f"   ✍️  Author: {author_name}")
        print(f"   💰 Price: ${price:.2f}")
        print(f"   📚 ISBN: {isbn}")
        print(f"   📅 Published: {format_date(published)}")
        print(f"   📊 Status: {status}")
        print(f"   🆔 ID: {Colors.CYAN}{book_id}{Colors.END}")
        print()

def display_statistics(authors, books):
    """Display database statistics"""
    print_section("📊 STATISTICS")
    
    total_authors = len(authors)
    total_books = len(books)
    
    # Calculate total revenue
    total_revenue = sum(book.get('price', 0) for book in books)
    
    # Available books
    available_books = sum(1 for book in books if book.get('is_available', True))
    unavailable_books = total_books - available_books
    
    # Average price
    avg_price = total_revenue / total_books if total_books > 0 else 0
    
    print(f"👥 Total Authors:      {Colors.BOLD}{total_authors}{Colors.END}")
    print(f"📚 Total Books:        {Colors.BOLD}{total_books}{Colors.END}")
    print(f"✅ Available Books:    {Colors.GREEN}{available_books}{Colors.END}")
    print(f"❌ Unavailable Books:  {Colors.RED}{unavailable_books}{Colors.END}")
    print(f"💰 Total Value:        {Colors.BOLD}${total_revenue:.2f}{Colors.END}")
    print(f"📊 Average Price:      ${avg_price:.2f}")
    
    if total_authors > 0:
        avg_books_per_author = total_books / total_authors
        print(f"📖 Avg Books/Author:   {avg_books_per_author:.1f}")
    
    print()

def display_top_authors(authors, books):
    """Display top authors by book count"""
    if not authors or not books:
        return
    
    print_section("🏆 TOP AUTHORS")
    
    # Count books per author
    author_book_counts = {}
    for author in authors:
        author_id = author.get('_id')
        author_name = author.get('name', 'Unknown')
        book_count = sum(1 for book in books if book.get('author_id') == author_id)
        if book_count > 0:
            author_book_counts[author_name] = book_count
    
    # Sort by book count
    sorted_authors = sorted(author_book_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (name, count) in enumerate(sorted_authors[:5], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"{medal} {Colors.BOLD}{name}{Colors.END}: {count} book{'s' if count != 1 else ''}")
    
    print()

def main():
    """Main function"""
    print_header("📚 MongoDB Database Viewer")
    
    print(f"{Colors.CYAN}Fetching data...{Colors.END}")
    
    # Fetch all data
    authors = get_all_authors()
    books = get_all_books()
    
    # Display everything
    display_statistics(authors, books)
    display_top_authors(authors, books)
    display_authors(authors)
    display_books(books)
    
    print_header("✨ Data Display Complete!")

if __name__ == "__main__":
    main()