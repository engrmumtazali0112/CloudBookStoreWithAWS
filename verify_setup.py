#!/usr/bin/env python
"""
Script to verify Django and MongoDB Atlas setup
"""

import requests
import sys

def check_server():
    """Check if Django server is running"""
    try:
        response = requests.get("http://localhost:8000", timeout=2)
        print("✅ Django server is running")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Django server is NOT running")
        print("   Start it with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

def check_mongodb_atlas():
    """Check if MongoDB Atlas is accessible"""
    try:
        from pymongo import MongoClient
        import certifi
        
        # MongoDB Atlas connection string (URL-encoded password)
        connection_string = "mongodb+srv://engrmumtazali01:Gani12%40%23@cluster0.ie4s7.mongodb.net/?appName=Cluster0"
        
        print("   Connecting to MongoDB Atlas...")
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
        
        # Test connection
        client.admin.command('ping')
        
        # Get server info
        server_info = client.server_info()
        version = server_info.get('version', 'Unknown')
        
        print(f"✅ MongoDB Atlas is connected successfully!")
        print(f"   MongoDB Version: {version}")
        print(f"   Cluster: cluster0.ie4s7.mongodb.net")
        
        # List databases
        databases = client.list_database_names()
        print(f"   Available Databases: {', '.join(databases)}")
        
        # Check bookstore_db
        db = client['bookstore_db']
        collections = db.list_collection_names()
        if collections:
            print(f"   Collections in bookstore_db: {', '.join(collections)}")
        else:
            print(f"   bookstore_db exists but has no collections yet")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check password in db_mongo.py (Gani12%40%23)")
        print("   2. Whitelist your IP in MongoDB Atlas:")
        print("      - Go to Network Access in Atlas")
        print("      - Add your IP or 0.0.0.0/0 for testing")
        print("   3. Verify cluster is running in Atlas dashboard")
        print("   4. Check your internet connection")
        return False

def check_django_mongodb_connection():
    """Check Django's MongoDB connection"""
    try:
        print("   Testing Django MongoDB integration...")
        from codegraphers.db_mongo import mongo_db
        
        # Test connection through Django
        mongo_db.client.admin.command('ping')
        
        # Count documents
        author_count = mongo_db.authors.count_documents({})
        book_count = mongo_db.books.count_documents({})
        
        print(f"✅ Django MongoDB integration working!")
        print(f"   Authors in database: {author_count}")
        print(f"   Books in database: {book_count}")
        
        return True
    except Exception as e:
        print(f"❌ Django MongoDB integration failed: {e}")
        print("   Make sure db_mongo.py has correct connection string")
        return False

def check_authors_endpoint():
    """Check if authors endpoint is accessible"""
    try:
        response = requests.get("http://localhost:8000/api/mongo/authors/", timeout=5)
        print(f"\n📡 Testing: GET /api/mongo/authors/")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Authors endpoint is accessible (no auth required)")
            authors = response.json()
            print(f"   Current authors in MongoDB: {len(authors)}")
            return True
        elif response.status_code == 403:
            print("❌ 403 Forbidden - Authentication required")
            print("   This means permission_classes = [AllowAny] is NOT set")
            print("\n🔧 FIX:")
            print("   1. Open views_mongo.py")
            print("   2. Add to imports: from rest_framework.permissions import AllowAny")
            print("   3. Add to each view class: permission_classes = [AllowAny]")
            return False
        elif response.status_code == 404:
            print("❌ 404 Not Found - URL routing issue")
            print("   Check that urls_mongo.py is included in main urls.py")
            return False
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_post_author():
    """Try to POST a test author"""
    try:
        import time
        test_data = {
            "name": "Test Author Atlas",
            "email": f"test_atlas_{int(time.time())}@example.com",
            "bio": "Testing MongoDB Atlas connection"
        }
        
        print(f"\n📡 Testing: POST /api/mongo/authors/")
        response = requests.post(
            "http://localhost:8000/api/mongo/authors/",
            json=test_data,
            timeout=5
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ POST works! Author created in MongoDB Atlas")
            data = response.json()
            author_id = data.get('id')
            print(f"   Author ID: {author_id}")
            
            # Clean up test data
            if author_id:
                try:
                    delete_response = requests.delete(
                        f"http://localhost:8000/api/mongo/authors/{author_id}/",
                        timeout=5
                    )
                    if delete_response.status_code in [200, 204]:
                        print(f"   ✓ Test data cleaned up")
                except:
                    pass
            
            return True
        elif response.status_code == 403:
            print("❌ 403 Forbidden - Cannot POST (authentication required)")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_crud_operations():
    """Test complete CRUD operations on MongoDB Atlas"""
    print("\n📋 Testing CRUD Operations on MongoDB Atlas...")
    
    try:
        import time
        
        # CREATE
        print("   1. CREATE - Adding test author...")
        author_data = {
            "name": "CRUD Test Author",
            "email": f"crud_test_{int(time.time())}@example.com",
            "bio": "Testing CRUD operations"
        }
        response = requests.post("http://localhost:8000/api/mongo/authors/", json=author_data)
        if response.status_code == 201:
            author_id = response.json().get('id')
            print(f"      ✅ Created author with ID: {author_id}")
        else:
            print(f"      ❌ Failed to create author")
            return False
        
        # READ
        print("   2. READ - Fetching author...")
        response = requests.get(f"http://localhost:8000/api/mongo/authors/{author_id}/")
        if response.status_code == 200:
            author = response.json()
            print(f"      ✅ Read author: {author.get('name')}")
        else:
            print(f"      ❌ Failed to read author")
            return False
        
        # UPDATE
        print("   3. UPDATE - Updating author...")
        update_data = {"name": "CRUD Test Updated", "email": author_data['email'], "bio": "Updated bio"}
        response = requests.put(f"http://localhost:8000/api/mongo/authors/{author_id}/", json=update_data)
        if response.status_code == 200:
            print(f"      ✅ Updated author successfully")
        else:
            print(f"      ❌ Failed to update author")
            return False
        
        # DELETE
        print("   4. DELETE - Removing author...")
        response = requests.delete(f"http://localhost:8000/api/mongo/authors/{author_id}/")
        if response.status_code == 200:
            print(f"      ✅ Deleted author successfully")
        else:
            print(f"      ❌ Failed to delete author")
            return False
        
        print("\n✅ All CRUD operations successful on MongoDB Atlas!")
        return True
        
    except Exception as e:
        print(f"\n❌ CRUD operations failed: {e}")
        return False

def main():
    print("="*70)
    print("🔍 Django + MongoDB Atlas Setup Verification")
    print("="*70)
    
    print("\n1️⃣  Checking Django Server...")
    server_ok = check_server()
    
    if not server_ok:
        print("\n❌ Cannot proceed without Django server running")
        sys.exit(1)
    
    print("\n2️⃣  Checking MongoDB Atlas Connection...")
    mongo_ok = check_mongodb_atlas()
    
    print("\n3️⃣  Checking Django MongoDB Integration...")
    django_mongo_ok = check_django_mongodb_connection()
    
    print("\n4️⃣  Checking Authors Endpoint (GET)...")
    get_ok = check_authors_endpoint()
    
    print("\n5️⃣  Checking Authors Endpoint (POST)...")
    post_ok = check_post_author()
    
    # Optional: Test CRUD operations
    crud_ok = test_crud_operations()
    
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"Django Server:           {'✅' if server_ok else '❌'}")
    print(f"MongoDB Atlas:           {'✅' if mongo_ok else '❌'}")
    print(f"Django MongoDB:          {'✅' if django_mongo_ok else '❌'}")
    print(f"GET Endpoint:            {'✅' if get_ok else '❌'}")
    print(f"POST Endpoint:           {'✅' if post_ok else '❌'}")
    print(f"CRUD Operations:         {'✅' if crud_ok else '❌'}")
    
    if all([server_ok, mongo_ok, django_mongo_ok, get_ok, post_ok, crud_ok]):
        print("\n" + "="*70)
        print("🎉 ALL CHECKS PASSED!")
        print("="*70)
        print("✨ Your setup is working perfectly!")
        print("📊 MongoDB Atlas is connected and operational")
        print("🚀 You can now run: python add_data.py")
        print("📝 Or use: python manage_data.py for interactive management")
    else:
        print("\n⚠️  SOME CHECKS FAILED. Please fix the issues above.")
        
        if not mongo_ok:
            print("\n" + "="*70)
            print("🔧 MONGODB ATLAS CONNECTION FIX:")
            print("="*70)
            print("1. Verify password in db_mongo.py:")
            print("   connection_string = 'mongodb+srv://engrmumtazali01:Gani12%40%23@cluster0...'")
            print("\n2. Whitelist your IP in MongoDB Atlas:")
            print("   - Login to https://cloud.mongodb.com")
            print("   - Go to Network Access")
            print("   - Click 'Add IP Address'")
            print("   - Select 'Allow Access from Anywhere' (0.0.0.0/0) for testing")
            print("\n3. Verify cluster status:")
            print("   - Check that Cluster0 is running in Atlas dashboard")
            print("="*70)
        
        if not get_ok or not post_ok:
            print("\n" + "="*70)
            print("🔧 QUICK FIX FOR 403 ERROR:")
            print("="*70)
            print("1. Open: codegraphers/views_mongo.py")
            print("2. Add this import at the top:")
            print("   from rest_framework.permissions import AllowAny")
            print("\n3. Add this to EACH view class:")
            print("   permission_classes = [AllowAny]")
            print("\n4. Example:")
            print("   class MongoAuthorListView(APIView):")
            print("       permission_classes = [AllowAny]  # ← ADD THIS")
            print("       def get(self, request):")
            print("           ...")
            print("\n5. Restart Django server:")
            print("   - Stop server (Ctrl+C)")
            print("   - Start again: python manage.py runserver")
            print("="*70)

if __name__ == "__main__":
    main()