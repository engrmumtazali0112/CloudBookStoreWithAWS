#!/usr/bin/env python
"""
List all databases and collections in MongoDB Atlas
"""

from pymongo import MongoClient

def list_all_data():
    # MongoDB Atlas connection
    connection_string = "mongodb+srv://engrmumtazali01:Gani12%40%23@cluster0.ie4s7.mongodb.net/?appName=Cluster0"
    
    print("=" * 70)
    print("📊 MongoDB Atlas - Complete Database Inventory")
    print("=" * 70)
    
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        print()
        
        # List all databases
        databases = client.list_database_names()
        
        # Filter out system databases
        user_databases = [db for db in databases if db not in ['admin', 'local', 'config']]
        
        print(f"📚 Found {len(user_databases)} user databases:")
        print()
        
        # Show details for each database
        for db_name in sorted(user_databases):
            db = client[db_name]
            collections = db.list_collection_names()
            
            print(f"🗄️  {db_name}")
            print(f"   Collections: {len(collections)}")
            
            if collections:
                for coll_name in collections:
                    count = db[coll_name].count_documents({})
                    print(f"      📋 {coll_name}: {count} documents")
            else:
                print("      (empty)")
            
            print()
        
        # Specifically check for bookstore_db
        print("=" * 70)
        print("🔍 Checking for 'bookstore_db':")
        print("=" * 70)
        
        if 'bookstore_db' in databases:
            print("✅ 'bookstore_db' EXISTS in Atlas!")
            print()
            
            bookstore_db = client['bookstore_db']
            collections = bookstore_db.list_collection_names()
            
            print(f"Collections in bookstore_db: {collections}")
            print()
            
            if 'authors' in collections:
                author_count = bookstore_db['authors'].count_documents({})
                print(f"   👥 Authors: {author_count}")
                
                # Show first 3 authors
                authors = list(bookstore_db['authors'].find().limit(3))
                for i, author in enumerate(authors, 1):
                    print(f"      {i}. {author.get('name', 'N/A')} ({author.get('email', 'N/A')})")
            
            if 'books' in collections:
                book_count = bookstore_db['books'].count_documents({})
                print(f"   📚 Books: {book_count}")
                
                # Show first 3 books
                books = list(bookstore_db['books'].find().limit(3))
                for i, book in enumerate(books, 1):
                    print(f"      {i}. {book.get('title', 'N/A')} - ${book.get('price', 0)}")
        else:
            print("❌ 'bookstore_db' NOT FOUND in Atlas!")
            print()
            print("📝 Available databases:")
            for db in user_databases:
                print(f"   - {db}")
            print()
            print("💡 Your data might be in a different database name")
        
        print()
        print("=" * 70)
        print("✨ Inventory Complete!")
        print("=" * 70)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error connecting to Atlas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_all_data()