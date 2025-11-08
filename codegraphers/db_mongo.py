from pymongo import MongoClient
from django.conf import settings
import certifi
import ssl

class MongoDB:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            
            # MongoDB Atlas connection string (URL-encoded password)
            connection_string = "mongodb+srv://engrmumtazali01:Gani12%40%23@cluster0.ie4s7.mongodb.net/?appName=Cluster0"
            
            try:
                # Create client with SSL certificate fix
                cls._instance.client = MongoClient(
                    connection_string,
                    serverSelectionTimeoutMS=10000,
                    connectTimeoutMS=10000,
                    tlsCAFile=certifi.where(),  # Use certifi certificates
                    tls=True,
                    tlsAllowInvalidCertificates=False
                )
                
                # Use bookstore_db database
                cls._instance.db = cls._instance.client['bookstore_db']
                
                # Test connection
                cls._instance.client.admin.command('ping')
                print("✅ Successfully connected to MongoDB Atlas!")
                
                # Show database info
                db_name_actual = cls._instance.db.name
                collections = cls._instance.db.list_collection_names()
                
                print(f"📊 Active database: {db_name_actual}")
                
                if collections:
                    print(f"📚 Collections: {collections}")
                    
                    # Show document counts
                    for collection_name in collections:
                        try:
                            count = cls._instance.db[collection_name].count_documents({})
                            print(f"   📖 {collection_name}: {count} documents")
                        except:
                            pass
                else:
                    print(f"📚 No collections yet (database is empty)")
                
            except Exception as e:
                print(f"❌ MongoDB Atlas connection failed: {e}")
                print(f"⚠️  Falling back to localhost MongoDB...")
                
                # Fallback to localhost
                try:
                    cls._instance.client = MongoClient('mongodb://localhost:27017/')
                    cls._instance.db = cls._instance.client['bookstore_db']
                    print("✅ Connected to local MongoDB")
                except:
                    print("❌ Local MongoDB also unavailable")
                    raise
        
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
        try:
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
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}

# Initialize MongoDB connection
mongo_db = MongoDB()
