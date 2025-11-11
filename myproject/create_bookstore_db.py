#!/usr/bin/env python
"""
Create bookstore_db database in MongoDB Atlas
This will initialize an empty bookstore_db that your Django app can use
"""

from pymongo import MongoClient

def create_bookstore_db():
    # MongoDB Atlas connection
    connection_string = "mongodb+srv://engrmumtazali01:Gani12%40%23@cluster0.ie4s7.mongodb.net/?appName=Cluster0"
    
    print("=" * 70)
    print("🏗️  Creating bookstore_db in MongoDB Atlas")
    print("=" * 70)
    
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        print()
        
        # Access bookstore_db (will be created when we insert first document)
        bookstore_db = client['bookstore_db']
        
        # Create collections by inserting a dummy document and removing it
        # This forces MongoDB to create the database and collections
        
        print("📚 Creating 'authors' collection...")
        bookstore_db['authors'].insert_one({"_temp": True})
        bookstore_db['authors'].delete_one({"_temp": True})
        print("✅ 'authors' collection created")
        
        print("📖 Creating 'books' collection...")
        bookstore_db['books'].insert_one({"_temp": True})
        bookstore_db['books'].delete_one({"_temp": True})
        print("✅ 'books' collection created")
        
        print("👤 Creating 'author_profiles' collection...")
        bookstore_db['author_profiles'].insert_one({"_temp": True})
        bookstore_db['author_profiles'].delete_one({"_temp": True})
        print("✅ 'author_profiles' collection created")
        
        print()
        print("=" * 70)
        print("📊 Verification")
        print("=" * 70)
        
        # List all databases
        databases = client.list_database_names()
        
        if 'bookstore_db' in databases:
            print("✅ 'bookstore_db' exists in Atlas!")
            
            collections = bookstore_db.list_collection_names()
            print(f"📚 Collections: {collections}")
            
            for coll_name in collections:
                count = bookstore_db[coll_name].count_documents({})
                print(f"   📋 {coll_name}: {count} documents")
        else:
            print("❌ 'bookstore_db' was not created")
        
        print()
        print("=" * 70)
        print("🎉 Database Setup Complete!")
        print("=" * 70)
        print()
        print("📝 Next steps:")
        print("1. Make sure db_mongo.py uses 'bookstore_db'")
        print("2. Restart Django server: python manage.py runserver")
        print("3. Add data: python add_data.py")
        print("4. Verify: python verify_setup.py")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_bookstore_db()