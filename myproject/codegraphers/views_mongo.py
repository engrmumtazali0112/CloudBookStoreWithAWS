"""
MongoDB Views - Complete Working Version
Replace your entire views_mongo.py with this file
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from bson import ObjectId
from .db_mongo import mongo_db
from datetime import datetime


def serialize_mongo_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    
    # Convert all ObjectIds to strings
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, list):
            doc[key] = [serialize_mongo_doc(item) if isinstance(item, dict) else 
                       str(item) if isinstance(item, ObjectId) else item 
                       for item in value]
        elif isinstance(value, dict):
            doc[key] = serialize_mongo_doc(value)
    
    return doc


class MongoAuthorListView(APIView):
    """
    MongoDB Author List Operations
    GET: List all authors
    POST: Create new author
    """
    permission_classes = [AllowAny]  # No authentication required
    
    def get(self, request):
        """Get all authors from MongoDB"""
        try:
            authors = list(mongo_db.authors.find())
            authors = [serialize_mongo_doc(author) for author in authors]
            return Response(authors, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Create author in MongoDB"""
        try:
            data = request.data.copy()
            
            # Validate required fields
            if not data.get('name'):
                return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not data.get('email'):
                return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Add timestamp
            data['created_at'] = datetime.now()
            
            # Insert into MongoDB
            result = mongo_db.authors.insert_one(data)
            
            return Response({
                'id': str(result.inserted_id),
                'message': 'Author created successfully',
                'name': data.get('name')
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MongoAuthorDetailView(APIView):
    """
    MongoDB Author Detail Operations
    GET: Get single author
    PUT: Update author
    DELETE: Delete author
    """
    permission_classes = [AllowAny]
    
    def get(self, request, author_id):
        """Get single author by ID"""
        try:
            author = mongo_db.authors.find_one({'_id': ObjectId(author_id)})
            if author:
                author = serialize_mongo_doc(author)
                return Response(author, status=status.HTTP_200_OK)
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, author_id):
        """Update author"""
        try:
            data = request.data.copy()
            # Remove _id if present to avoid conflicts
            data.pop('_id', None)
            data.pop('created_at', None)  # Don't update created_at
            
            # Add updated timestamp
            data['updated_at'] = datetime.now()
            
            result = mongo_db.authors.update_one(
                {'_id': ObjectId(author_id)},
                {'$set': data}
            )
            
            if result.modified_count or result.matched_count:
                return Response({'message': 'Author updated successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, author_id):
        """Delete author"""
        try:
            result = mongo_db.authors.delete_one({'_id': ObjectId(author_id)})
            if result.deleted_count:
                return Response({'message': 'Author deleted successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MongoBookListView(APIView):
    """
    MongoDB Book List Operations
    GET: List all books (with filters)
    POST: Create new book
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get all books with optional filters"""
        try:
            query = {}
            
            # Filter by availability
            if request.query_params.get('available'):
                query['is_available'] = request.query_params.get('available').lower() == 'true'
            
            # Filter by author
            if request.query_params.get('author'):
                try:
                    query['author_id'] = ObjectId(request.query_params.get('author'))
                except:
                    query['author_id'] = request.query_params.get('author')
            
            # Price range filters
            price_filter = {}
            if request.query_params.get('min_price'):
                price_filter['$gte'] = float(request.query_params.get('min_price'))
            if request.query_params.get('max_price'):
                price_filter['$lte'] = float(request.query_params.get('max_price'))
            if price_filter:
                query['price'] = price_filter
            
            # Search by title or ISBN
            search = request.query_params.get('search')
            if search:
                query['$or'] = [
                    {'title': {'$regex': search, '$options': 'i'}},
                    {'isbn': {'$regex': search, '$options': 'i'}}
                ]
            
            books = list(mongo_db.books.find(query))
            books = [serialize_mongo_doc(book) for book in books]
            return Response(books, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Create book in MongoDB"""
        try:
            data = request.data.copy()
            
            # Validate required fields
            required_fields = ['title', 'author_id', 'price', 'isbn']
            for field in required_fields:
                if field not in data:
                    return Response(
                        {'error': f'{field} is required'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Add timestamp
            data['created_at'] = datetime.now()
            
            # Convert author_id to ObjectId if it's a string
            if 'author_id' in data and isinstance(data['author_id'], str):
                try:
                    data['author_id'] = ObjectId(data['author_id'])
                except:
                    pass
            
            # Ensure price is float
            if 'price' in data:
                data['price'] = float(data['price'])
            
            # Set default availability
            if 'is_available' not in data:
                data['is_available'] = True
            
            # Insert book
            result = mongo_db.books.insert_one(data)
            
            # Update author stats
            author_id = data.get('author_id')
            if author_id:
                mongo_db.authors.update_one(
                    {'_id': author_id if isinstance(author_id, ObjectId) else ObjectId(author_id)},
                    {
                        '$inc': {
                            'total_books': 1,
                            'total_revenue': float(data.get('price', 0))
                        }
                    }
                )
            
            return Response({
                'id': str(result.inserted_id),
                'message': 'Book created successfully',
                'title': data.get('title')
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MongoBookDetailView(APIView):
    """
    MongoDB Book Detail Operations
    GET: Get single book
    PUT: Update book
    DELETE: Delete book
    PATCH: Mark available/unavailable
    """
    permission_classes = [AllowAny]
    
    def get(self, request, book_id):
        """Get single book by ID"""
        try:
            book = mongo_db.books.find_one({'_id': ObjectId(book_id)})
            if book:
                book = serialize_mongo_doc(book)
                return Response(book, status=status.HTTP_200_OK)
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, book_id):
        """Update book"""
        try:
            data = request.data.copy()
            data.pop('_id', None)
            data.pop('created_at', None)
            
            # Convert author_id if needed
            if 'author_id' in data and isinstance(data['author_id'], str):
                try:
                    data['author_id'] = ObjectId(data['author_id'])
                except:
                    pass
            
            # Ensure price is float
            if 'price' in data:
                data['price'] = float(data['price'])
            
            data['updated_at'] = datetime.now()
            
            result = mongo_db.books.update_one(
                {'_id': ObjectId(book_id)},
                {'$set': data}
            )
            
            if result.modified_count or result.matched_count:
                return Response({'message': 'Book updated successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, book_id):
        """Delete book and update author stats"""
        try:
            # Get book first to update author stats
            book = mongo_db.books.find_one({'_id': ObjectId(book_id)})
            
            if book:
                # Delete book
                result = mongo_db.books.delete_one({'_id': ObjectId(book_id)})
                
                if result.deleted_count:
                    # Update author stats
                    author_id = book.get('author_id')
                    if author_id:
                        mongo_db.authors.update_one(
                            {'_id': author_id if isinstance(author_id, ObjectId) else ObjectId(author_id)},
                            {
                                '$inc': {
                                    'total_books': -1,
                                    'total_revenue': -float(book.get('price', 0))
                                }
                            }
                        )
                    
                    return Response({'message': 'Book deleted successfully'}, status=status.HTTP_200_OK)
            
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, book_id):
        """Mark book as available or unavailable"""
        try:
            action = request.data.get('action')
            
            if action == 'mark_available':
                update_data = {'is_available': True}
            elif action == 'mark_unavailable':
                update_data = {'is_available': False}
            else:
                return Response(
                    {'error': 'Invalid action. Use "mark_available" or "mark_unavailable"'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            update_data['updated_at'] = datetime.now()
            
            result = mongo_db.books.update_one(
                {'_id': ObjectId(book_id)},
                {'$set': update_data}
            )
            
            if result.modified_count or result.matched_count:
                book = mongo_db.books.find_one({'_id': ObjectId(book_id)})
                book = serialize_mongo_doc(book)
                return Response(book, status=status.HTTP_200_OK)
                
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)