#!/usr/bin/env python
"""
Interactive MongoDB Data Management Script
Provides a menu-driven interface for managing authors and books
"""

import requests
import sys
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
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    """Clear the console screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header"""
    clear_screen()
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'🗄️  MongoDB DATA MANAGER':^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_menu():
    """Print the main menu"""
    print(f"{Colors.BOLD}{Colors.BLUE}MAIN MENU{Colors.END}")
    print(f"{Colors.BLUE}{'-'*70}{Colors.END}\n")
    print(f"  {Colors.GREEN}1.{Colors.END} View All Data")
    print(f"  {Colors.GREEN}2.{Colors.END} Add New Author")
    print(f"  {Colors.GREEN}3.{Colors.END} Add New Book")
    print(f"  {Colors.GREEN}4.{Colors.END} Search Books")
    print(f"  {Colors.GREEN}5.{Colors.END} List All Authors")
    print(f"  {Colors.GREEN}6.{Colors.END} List All Books")
    print(f"  {Colors.GREEN}7.{Colors.END} Delete Author")
    print(f"  {Colors.GREEN}8.{Colors.END} Delete Book")
    print(f"  {Colors.GREEN}9.{Colors.END} Import Sample Data")
    print(f"  {Colors.RED}0.{Colors.END} Exit")
    print(f"\n{Colors.BLUE}{'-'*70}{Colors.END}")

def get_choice():
    """Get user menu choice"""
    try:
        choice = input(f"\n{Colors.YELLOW}Enter your choice: {Colors.END}").strip()
        return choice
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Exiting...{Colors.END}")
        sys.exit(0)

def pause():
    """Pause and wait for user input"""
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def get_all_authors():
    """Get all authors from API"""
    try:
        response = requests.get(AUTHORS_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return []

def get_all_books():
    """Get all books from API"""
    try:
        response = requests.get(BOOKS_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return []

def view_all_data():
    """View all data - Option 1"""
    print_header()
    print(f"{Colors.BOLD}📊 DATABASE OVERVIEW{Colors.END}\n")
    
    authors = get_all_authors()
    books = get_all_books()
    
    print(f"👥 Total Authors: {Colors.BOLD}{len(authors)}{Colors.END}")
    print(f"📚 Total Books: {Colors.BOLD}{len(books)}{Colors.END}")
    
    if authors:
        print(f"\n{Colors.BOLD}Authors:{Colors.END}")
        for author in authors:
            name = author.get('name', 'Unknown')
            email = author.get('email', 'No email')
            print(f"  • {name} ({email})")
    
    if books:
        print(f"\n{Colors.BOLD}Books:{Colors.END}")
        for book in books:
            title = book.get('title', 'Unknown')
            price = book.get('price', 0)
            print(f"  • {title} - ${price:.2f}")
    
    pause()

def add_author():
    """Add new author - Option 2"""
    print_header()
    print(f"{Colors.BOLD}➕ ADD NEW AUTHOR{Colors.END}\n")
    
    name = input("Enter author name: ").strip()
    if not name:
        print(f"{Colors.RED}Name cannot be empty!{Colors.END}")
        pause()
        return
    
    email = input("Enter email: ").strip()
    if not email:
        print(f"{Colors.RED}Email cannot be empty!{Colors.END}")
        pause()
        return
    
    bio = input("Enter bio (optional): ").strip()
    
    data = {
        "name": name,
        "email": email,
        "bio": bio
    }
    
    try:
        response = requests.post(AUTHORS_URL, json=data)
        if response.status_code == 201:
            result = response.json()
            print(f"\n{Colors.GREEN}✅ Author created successfully!{Colors.END}")
            print(f"ID: {result.get('id')}")
        else:
            print(f"\n{Colors.RED}❌ Error: {response.text}{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
    
    pause()

def add_book():
    """Add new book - Option 3"""
    print_header()
    print(f"{Colors.BOLD}➕ ADD NEW BOOK{Colors.END}\n")
    
    # Get and display authors
    authors = get_all_authors()
    if not authors:
        print(f"{Colors.RED}No authors available. Please add an author first!{Colors.END}")
        pause()
        return
    
    print(f"{Colors.BOLD}Available Authors:{Colors.END}")
    for i, author in enumerate(authors, 1):
        print(f"  {i}. {author.get('name', 'Unknown')} ({author.get('_id', 'N/A')})")
    
    author_choice = input(f"\n{Colors.YELLOW}Select author number: {Colors.END}").strip()
    try:
        author_idx = int(author_choice) - 1
        if author_idx < 0 or author_idx >= len(authors):
            print(f"{Colors.RED}Invalid selection!{Colors.END}")
            pause()
            return
        selected_author = authors[author_idx]
        author_id = selected_author.get('_id')
    except ValueError:
        print(f"{Colors.RED}Invalid input!{Colors.END}")
        pause()
        return
    
    title = input("\nEnter book title: ").strip()
    if not title:
        print(f"{Colors.RED}Title cannot be empty!{Colors.END}")
        pause()
        return
    
    price = input("Enter price: ").strip()
    try:
        price = float(price)
    except ValueError:
        print(f"{Colors.RED}Invalid price!{Colors.END}")
        pause()
        return
    
    isbn = input("Enter ISBN: ").strip()
    if not isbn:
        print(f"{Colors.RED}ISBN cannot be empty!{Colors.END}")
        pause()
        return
    
    pub_date = input(f"Enter published date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not pub_date:
        pub_date = str(date.today())
    
    available = input("Is available? (y/n, default: y): ").strip().lower()
    is_available = available != 'n'
    
    data = {
        "title": title,
        "author_id": author_id,
        "price": price,
        "isbn": isbn,
        "published_date": pub_date,
        "is_available": is_available
    }
    
    try:
        response = requests.post(BOOKS_URL, json=data)
        if response.status_code == 201:
            result = response.json()
            print(f"\n{Colors.GREEN}✅ Book created successfully!{Colors.END}")
            print(f"ID: {result.get('id')}")
        else:
            print(f"\n{Colors.RED}❌ Error: {response.text}{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
    
    pause()

def search_books():
    """Search books - Option 4"""
    print_header()
    print(f"{Colors.BOLD}🔍 SEARCH BOOKS{Colors.END}\n")
    
    search_term = input("Enter search term (title or ISBN): ").strip()
    if not search_term:
        print(f"{Colors.RED}Search term cannot be empty!{Colors.END}")
        pause()
        return
    
    try:
        response = requests.get(f"{BOOKS_URL}?search={search_term}")
        if response.status_code == 200:
            books = response.json()
            if books:
                print(f"\n{Colors.GREEN}Found {len(books)} book(s):{Colors.END}\n")
                for book in books:
                    title = book.get('title', 'Unknown')
                    price = book.get('price', 0)
                    isbn = book.get('isbn', 'N/A')
                    print(f"  • {title}")
                    print(f"    Price: ${price:.2f} | ISBN: {isbn}")
                    print()
            else:
                print(f"{Colors.YELLOW}No books found matching '{search_term}'{Colors.END}")
        else:
            print(f"{Colors.RED}Error searching books{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
    
    pause()

def list_authors():
    """List all authors - Option 5"""
    print_header()
    print(f"{Colors.BOLD}👥 ALL AUTHORS{Colors.END}\n")
    
    authors = get_all_authors()
    if authors:
        for i, author in enumerate(authors, 1):
            name = author.get('name', 'Unknown')
            email = author.get('email', 'No email')
            bio = author.get('bio', 'No bio')
            author_id = author.get('_id', 'N/A')
            
            print(f"{Colors.BOLD}{i}. {name}{Colors.END}")
            print(f"   Email: {email}")
            print(f"   Bio: {bio[:60]}{'...' if len(bio) > 60 else ''}")
            print(f"   ID: {author_id}")
            print()
    else:
        print(f"{Colors.YELLOW}No authors found.{Colors.END}")
    
    pause()

def list_books():
    """List all books - Option 6"""
    print_header()
    print(f"{Colors.BOLD}📚 ALL BOOKS{Colors.END}\n")
    
    books = get_all_books()
    if books:
        for i, book in enumerate(books, 1):
            title = book.get('title', 'Unknown')
            price = book.get('price', 0)
            isbn = book.get('isbn', 'N/A')
            available = book.get('is_available', True)
            status = f"{Colors.GREEN}✓{Colors.END}" if available else f"{Colors.RED}✗{Colors.END}"
            
            print(f"{Colors.BOLD}{i}. {title}{Colors.END} {status}")
            print(f"   Price: ${price:.2f} | ISBN: {isbn}")
            print()
    else:
        print(f"{Colors.YELLOW}No books found.{Colors.END}")
    
    pause()

def delete_author():
    """Delete author - Option 7"""
    print_header()
    print(f"{Colors.BOLD}🗑️  DELETE AUTHOR{Colors.END}\n")
    
    authors = get_all_authors()
    if not authors:
        print(f"{Colors.YELLOW}No authors to delete.{Colors.END}")
        pause()
        return
    
    print(f"{Colors.BOLD}Available Authors:{Colors.END}")
    for i, author in enumerate(authors, 1):
        print(f"  {i}. {author.get('name', 'Unknown')} (ID: {author.get('_id', 'N/A')})")
    
    choice = input(f"\n{Colors.YELLOW}Select author number to delete (0 to cancel): {Colors.END}").strip()
    try:
        idx = int(choice) - 1
        if idx < 0:
            return
        if idx >= len(authors):
            print(f"{Colors.RED}Invalid selection!{Colors.END}")
            pause()
            return
        
        author = authors[idx]
        confirm = input(f"\n{Colors.RED}Are you sure you want to delete '{author.get('name')}'? (yes/no): {Colors.END}").strip().lower()
        if confirm == 'yes':
            response = requests.delete(f"{AUTHORS_URL}{author.get('_id')}/")
            if response.status_code in [200, 204]:
                print(f"\n{Colors.GREEN}✅ Author deleted successfully!{Colors.END}")
            else:
                print(f"\n{Colors.RED}❌ Error deleting author{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}Deletion cancelled.{Colors.END}")
    except ValueError:
        print(f"{Colors.RED}Invalid input!{Colors.END}")
    
    pause()

def delete_book():
    """Delete book - Option 8"""
    print_header()
    print(f"{Colors.BOLD}🗑️  DELETE BOOK{Colors.END}\n")
    
    books = get_all_books()
    if not books:
        print(f"{Colors.YELLOW}No books to delete.{Colors.END}")
        pause()
        return
    
    print(f"{Colors.BOLD}Available Books:{Colors.END}")
    for i, book in enumerate(books, 1):
        print(f"  {i}. {book.get('title', 'Unknown')} (ID: {book.get('_id', 'N/A')})")
    
    choice = input(f"\n{Colors.YELLOW}Select book number to delete (0 to cancel): {Colors.END}").strip()
    try:
        idx = int(choice) - 1
        if idx < 0:
            return
        if idx >= len(books):
            print(f"{Colors.RED}Invalid selection!{Colors.END}")
            pause()
            return
        
        book = books[idx]
        confirm = input(f"\n{Colors.RED}Are you sure you want to delete '{book.get('title')}'? (yes/no): {Colors.END}").strip().lower()
        if confirm == 'yes':
            response = requests.delete(f"{BOOKS_URL}{book.get('_id')}/")
            if response.status_code in [200, 204]:
                print(f"\n{Colors.GREEN}✅ Book deleted successfully!{Colors.END}")
            else:
                print(f"\n{Colors.RED}❌ Error deleting book{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}Deletion cancelled.{Colors.END}")
    except ValueError:
        print(f"{Colors.RED}Invalid input!{Colors.END}")
    
    pause()

def import_sample_data():
    """Import sample data - Option 9"""
    print_header()
    print(f"{Colors.BOLD}📥 IMPORT SAMPLE DATA{Colors.END}\n")
    print(f"{Colors.YELLOW}This will add sample authors and books to the database.{Colors.END}")
    
    confirm = input(f"\nContinue? (y/n): ").strip().lower()
    if confirm != 'y':
        return
    
    print(f"\n{Colors.CYAN}Importing data...{Colors.END}\n")
    
    # Run add_data.py equivalent
    import subprocess
    try:
        result = subprocess.run(['python', 'add_data.py'], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print(f"\n{Colors.GREEN}✅ Sample data imported successfully!{Colors.END}")
        else:
            print(f"\n{Colors.RED}❌ Error importing data{Colors.END}")
            if result.stderr:
                print(result.stderr)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
        print(f"\n{Colors.YELLOW}Tip: Make sure add_data.py exists in the current directory{Colors.END}")
    
    pause()

def main():
    """Main application loop"""
    while True:
        print_header()
        print_menu()
        choice = get_choice()
        
        if choice == '1':
            view_all_data()
        elif choice == '2':
            add_author()
        elif choice == '3':
            add_book()
        elif choice == '4':
            search_books()
        elif choice == '5':
            list_authors()
        elif choice == '6':
            list_books()
        elif choice == '7':
            delete_author()
        elif choice == '8':
            delete_book()
        elif choice == '9':
            import_sample_data()
        elif choice == '0':
            print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.END}\n")
            break
        else:
            print(f"\n{Colors.RED}Invalid choice! Please try again.{Colors.END}")
            pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program interrupted. Exiting...{Colors.END}\n")
        sys.exit(0)