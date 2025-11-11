from pymongo import MongoClient
from django.conf import settings
import os

class MongoDB:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            
            # MongoDB Atlas connection string with URL-encoded password
            # Password: Gani12@# → Gani12%40%23 (@ = %40, # = %23)
            connection_string = "mongodb+srv://engrmumtazali01:Gani12%40%23@cluster0.ie4s7.mongodb.net/?appName=Cluster0"
            
            cls._instance.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # FIXED: Use 'book_database' instead of 'bookstore_db'
            # This database already exists in your Atlas with 4 books
            cls._instance.db = cls._instance.client['book_database']
            
            # Test connection
            try:
                cls._instance.client.admin.command('ping')
                print("✅ Successfully connected to MongoDB Atlas!")
                
                # Show database info
                db_name = cls._instance.db.name
                collections = cls._instance.db.list_collection_names()
                
                print(f"📊 Active database: {db_name}")
                print(f"📚 Collections: {collections}")
                
                # Show document counts
                for collection_name in collections:
                    count = cls._instance.db[collection_name].count_documents({})
                    print(f"   📖 {collection_name}: {count} documents")
                
            except Exception as e:
                print(f"❌ MongoDB Atlas connection failed: {e}")
        
        return cls._instance
    
    @property
    def authors(self):
        """Access authors collection"""
        return self.db['authors']
    
    @property
    def books(self):
        """Access books collection"""
        return self.db['books']
    
    @property
    def profiles(self):
        """Access author_profiles collection"""
        return self.db['author_profiles']
    
    def get_stats(self):
        """Get database statistics"""
        stats = {
            'database': self.db.name,
            'collections': self.db.list_collection_names(),
            'counts': {
                'books': self.books.count_documents({}),
                'authors': self.authors.count_documents({}),
                'profiles': self.profiles.count_documents({})
            }
        }
        return stats

# Initialize
mongo_db = MongoDB()