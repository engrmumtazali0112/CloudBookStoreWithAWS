# 📚 Bookstore Management System

<div align="center">

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A powerful dual-database bookstore management system built with Django REST Framework, featuring both SQL and NoSQL architectures.

[Features](#-features) • [Installation](#-installation) • [API Documentation](#-api-documentation) • [Database Architecture](#-database-architecture)

</div>

---

## 🌟 Features

### 🎯 Core Functionality
- ✅ **Dual Database Support** - PostgreSQL for relational data + MongoDB for document storage
- 🔐 **RESTful API** - Complete CRUD operations with Django REST Framework
- 📊 **Real-time Statistics** - Author profiles with automatic book count and revenue tracking
- 🔍 **Advanced Filtering** - Search by title, ISBN, price range, availability
- 📝 **Signal-based Updates** - Automatic profile updates on book creation/deletion
- 🚀 **MongoDB Atlas Integration** - Cloud-based NoSQL database support

### 💡 Technical Highlights
- 🏗️ **Polyglot Persistence** - Leverage strengths of both SQL and NoSQL
- 🔄 **Django Signals** - Automated data synchronization
- 🛡️ **Data Validation** - Input validation with DRF serializers
- 📦 **Modular Architecture** - Clean separation of concerns
- 🎨 **Interactive CLI** - User-friendly data management interface

---

## 🏗️ Database Architecture

### 🐘 PostgreSQL (Relational Database)
```
┌─────────────┐         ┌──────────────┐         ┌─────────────────┐
│   Authors   │────────>│    Books     │<────────│ AuthorProfile   │
├─────────────┤         ├──────────────┤         ├─────────────────┤
│ id          │         │ id           │         │ id              │
│ name        │         │ title        │         │ author_id (FK)  │
│ email       │         │ author_id(FK)│         │ total_books     │
│ bio         │         │ price        │         │ total_revenue   │
│ created_at  │         │ isbn         │         │ is_verified     │
└─────────────┘         │ published_at │         └─────────────────┘
                        │ is_available │
                        └──────────────┘
```

### 🍃 MongoDB (Document Database)
```json
{
  "authors": {
    "_id": "ObjectId",
    "name": "string",
    "email": "string",
    "bio": "string",
    "created_at": "datetime"
  },
  "books": {
    "_id": "ObjectId",
    "title": "string",
    "author_id": "ObjectId",
    "price": "float",
    "isbn": "string",
    "published_date": "string",
    "is_available": "boolean"
  }
}
```

---

## 🚀 Installation

### Prerequisites
- 🐍 Python 3.8+
- 🐘 PostgreSQL 12+
- 🍃 MongoDB Atlas Account (or local MongoDB)
- 📦 pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/bookstore-api.git
cd bookstore-api
```

### Step 2: Create Virtual Environment
```bash
python -m venv env

# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: PostgreSQL Setup
```bash
# Open PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE bookstore_db;
\c bookstore_db

# Create tables (copy from terminal output or run migrations)
```

### Step 5: MongoDB Atlas Setup
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster named `Cluster0`
3. Whitelist your IP address (0.0.0.0/0 for testing)
4. Get connection string and update `db_mongo.py`

### Step 6: Configure Settings
Update `myproject/settings.py`:
```python
# PostgreSQL Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bookstore_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# MongoDB Configuration
MONGODB_SETTINGS = {
    'CONNECTION_STRING': 'mongodb+srv://username:password@cluster0...',
    'DATABASE_NAME': 'bookstore_db'
}
```

### Step 7: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 8: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 9: Start Server
```bash
python manage.py runserver
```

🎉 **Server running at:** `http://127.0.0.1:8000/`

---

## 📡 API Documentation

### 🐘 PostgreSQL Endpoints

#### Authors
| Method | Endpoint | Description |
|--------|----------|-------------|
| 📋 GET | `/api/authors/` | List all authors |
| ➕ POST | `/api/authors/` | Create new author |
| 🔍 GET | `/api/authors/{id}/` | Get author details |
| ✏️ PUT | `/api/authors/{id}/` | Update author |
| 🗑️ DELETE | `/api/authors/{id}/` | Delete author |
| 📚 GET | `/api/authors/{id}/books/` | Get author's books |
| 📊 GET | `/api/authors/{id}/statistics/` | Get author stats |

#### Books
| Method | Endpoint | Description |
|--------|----------|-------------|
| 📋 GET | `/api/books/` | List all books |
| ➕ POST | `/api/books/` | Create new book |
| 🔍 GET | `/api/books/{id}/` | Get book details |
| ✏️ PUT | `/api/books/{id}/` | Update book |
| 🗑️ DELETE | `/api/books/{id}/` | Delete book |
| ❌ POST | `/api/books/{id}/mark_unavailable/` | Mark unavailable |
| ✅ POST | `/api/books/{id}/mark_available/` | Mark available |

### 🍃 MongoDB Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| 📋 GET | `/api/mongo/authors/` | List all authors |
| ➕ POST | `/api/mongo/authors/` | Create new author |
| 🔍 GET | `/api/mongo/authors/{id}/` | Get author details |
| ✏️ PUT | `/api/mongo/authors/{id}/` | Update author |
| 🗑️ DELETE | `/api/mongo/authors/{id}/` | Delete author |
| 📋 GET | `/api/mongo/books/` | List all books |
| ➕ POST | `/api/mongo/books/` | Create new book |
| 🔍 GET | `/api/mongo/books/{id}/` | Get book details |
| ✏️ PUT | `/api/mongo/books/{id}/` | Update book |
| 🗑️ DELETE | `/api/mongo/books/{id}/` | Delete book |

---

## 📝 API Usage Examples

### Create Author (PostgreSQL)
```bash
curl -X POST http://127.0.0.1:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "J.K. Rowling",
    "email": "jk@example.com",
    "bio": "British author"
  }'
```

### Create Book (MongoDB)
```bash
curl -X POST http://127.0.0.1:8000/api/mongo/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter",
    "author_id": "690eb2e30e1630b0e518a039",
    "price": 19.99,
    "isbn": "978-1234567890",
    "published_date": "1997-06-26"
  }'
```

### Filter Books by Price
```bash
curl "http://127.0.0.1:8000/api/books/?min_price=10&max_price=30"
```

### Search Books
```bash
curl "http://127.0.0.1:8000/api/books/?search=Harry"
```

---

## 🛠️ Management Scripts

### 🔍 Verify Setup
```bash
python verify_setup.py
```
Checks Django server, PostgreSQL, MongoDB Atlas connectivity, and endpoints.

### 📊 Interactive Data Manager
```bash
python manage_data.py
```
User-friendly CLI for managing authors and books with MongoDB.

### 📥 Import Sample Data
```bash
python add_data.py
```
Populates database with sample authors and books.

---

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test Module
```bash
python manage.py test codegraphers.tests.AuthorAPITest
```

### Test Coverage
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## 📂 Project Structure

```
bookstore-api/
│
├── 📁 myproject/              # Main project directory
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI config
│
├── 📁 codegraphers/           # Main app
│   ├── models.py              # PostgreSQL models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # PostgreSQL views
│   ├── views_mongo.py         # MongoDB views
│   ├── urls.py                # PostgreSQL URLs
│   ├── urls_mongo.py          # MongoDB URLs
│   ├── db_mongo.py            # MongoDB connection
│   ├── signals.py             # Django signals
│   ├── admin.py               # Admin panel config
│   └── tests.py               # Test cases
│
├── 📁 scripts/                # Utility scripts
│   ├── verify_setup.py        # Setup verification
│   ├── manage_data.py         # Interactive CLI
│   └── add_data.py            # Sample data import
│
├── 📄 requirements.txt        # Python dependencies
├── 📄 README.md               # This file
└── 📄 manage.py               # Django management
```

---

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=bookstore_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
MONGODB_URI=mongodb+srv://user:pass@cluster0...
```

### Settings.py Configuration
```python
# Load environment variables
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

---

## 🚨 Troubleshooting

### PostgreSQL Connection Error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### MongoDB Atlas Connection Failed
1. ✅ Verify IP whitelist in Network Access
2. ✅ Check password encoding (@ = %40, # = %23)
3. ✅ Ensure cluster is active
4. ✅ Test connection with `verify_setup.py`

### 403 Forbidden Error
Add `permission_classes = [AllowAny]` to views:
```python
from rest_framework.permissions import AllowAny

class MongoAuthorListView(APIView):
    permission_classes = [AllowAny]
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. 🍴 Fork the repository
2. 🌿 Create feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push to branch (`git push origin feature/AmazingFeature`)
5. 🔃 Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mumtaz Ali**
- GitHub: [@engrmumtazali01](https://github.com/engrmumtazali01)
- Email: engrmumtazali01@gmail.com
- LinkedIn: [Mumtaz Ali](https://linkedin.com/in/mumtazali)

---

## 🙏 Acknowledgments

- 🎓 Django REST Framework documentation
- 📚 PostgreSQL community
- 🍃 MongoDB Atlas team
- 💡 Python community

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/bookstore-api?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/bookstore-api?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/bookstore-api)
![GitHub license](https://img.shields.io/github/license/yourusername/bookstore-api)

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Made with ❤️ and ☕ by Mumtaz Ali**

</div>
