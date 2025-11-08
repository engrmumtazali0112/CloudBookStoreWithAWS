#!/usr/bin/env python
"""
Migrate data from bookstore_db to book_database in MongoDB Atlas
"""

from pymongo import MongoClient

def migrate_data():
    # Connection string
    connection_string = "mongodb+srv://engrmumtazali01:Gani12%40%23@cluster0.ie4s7.mongodb.net/?appName=Cluster0"
    
    client = MongoClient(connection_string)
    
    # Source and destination databases
    source_db = client['bookstore_db']
    dest_db = client['book_database']
    
    print("=" * 70)
    print("📦 MongoDB Atlas Data Migration")
    print("=" * 70)
    print(f"Source: bookstore_db")
    print(f"Destination: book_database")
    print()
    
    # Get collections from source
    collections = source_db.list_collection_names()
    print(f"📚 Collections to migrate: {collections}")
    print()
    
    for collection_name in collections:
        source_collection = source_db[collection_name]
        dest_collection = dest_db[collection_name]
        
        # Count documents
        doc_count = source_collection.count_documents({})
        
        if doc_count == 0:
            print(f"⏭️  Skipping {collection_name} (empty)")
            continue
        
        print(f"📋 Migrating {collection_name}...")
        print(f"   Documents to copy: {doc_count}")
        
        # Get all documents
        documents = list(source_collection.find())
        
        if documents:
            # Clear destination collection (optional - comment out if you want to keep existing data)
            existing_count = dest_collection.count_documents({})
            if existing_count > 0:
                print(f"   ⚠️  Destination has {existing_count} existing documents")
                response = input(f"   Delete existing data in book_database.{collection_name}? (yes/no): ")
                if response.lower() == 'yes':
                    result = dest_collection.delete_many({})
                    print(f"   🗑️  Deleted {result.deleted_count} existing documents")
            
            # Insert documents
            result = dest_collection.insert_many(documents)
            print(f"   ✅ Copied {len(result.inserted_ids)} documents")
        
        print()
    
    print("=" * 70)
    print("📊 Migration Summary")
    print("=" * 70)
    
    # Show final counts
    for collection_name in collections:
        source_count = source_db[collection_name].count_documents({})
        dest_count = dest_db[collection_name].count_documents({})
        
        status = "✅" if source_count == dest_count else "⚠️"
        print(f"{status} {collection_name}:")
        print(f"   bookstore_db: {source_count}")
        print(f"   book_database: {dest_count}")
    
    print()
    print("🎉 Migration complete!")
    print()
    print("📝 Next steps:")
    print("1. Update db_mongo.py to use 'book_database':")
    print("   cls._instance.db = cls._instance.client['book_database']")
    print("2. Restart Django server")
    print("3. Test with: python verify_setup.py")
    
    client.close()

if __name__ == "__main__":
    try:
        migrate_data()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()