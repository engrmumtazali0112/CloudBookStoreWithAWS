#!/usr/bin/env python
"""
Quick fix script to update db_mongo.py to use existing book_database
"""

import os

def fix_db_mongo():
    print("=" * 70)
    print("🔧 Quick Fix - Updating db_mongo.py")
    print("=" * 70)
    print()
    
    # Path to db_mongo.py
    db_mongo_path = "codegraphers/db_mongo.py"
    
    if not os.path.exists(db_mongo_path):
        print(f"❌ File not found: {db_mongo_path}")
        print("Please make sure you're in the correct directory")
        return
    
    print(f"📄 Reading {db_mongo_path}...")
    
    try:
        with open(db_mongo_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already using book_database
        if "'book_database']" in content or '"book_database"]' in content:
            print("✅ Already using 'book_database'!")
            print("No changes needed.")
            return
        
        # Replace bookstore_db with book_database
        old_line = "cls._instance.db = cls._instance.client['bookstore_db']"
        new_line = "cls._instance.db = cls._instance.client['book_database']"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            # Write back
            with open(db_mongo_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Successfully updated db_mongo.py!")
            print(f"   Changed: 'bookstore_db' → 'book_database'")
        else:
            print("⚠️  Could not find the line to replace")
            print("Please manually change:")
            print("   FROM: cls._instance.db = cls._instance.client['bookstore_db']")
            print("   TO:   cls._instance.db = cls._instance.client['book_database']")
        
        print()
        print("=" * 70)
        print("📝 Next Steps:")
        print("=" * 70)
        print("1. Restart Django server:")
        print("   - Stop current server (Ctrl+C)")
        print("   - Start: python manage.py runserver")
        print()
        print("2. Test the connection:")
        print("   python verify_setup.py")
        print()
        print("3. View your data:")
        print("   python view_data.py")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_db_mongo()