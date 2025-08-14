# FastAPI Social Media API

A robust, production-ready REST API built with FastAPI, featuring user authentication, post management, and voting system. This project demonstrates modern Python web development practices with SQLAlchemy ORM, Alembic migrations, and JWT authentication.

## 🚀 Features

- **User Authentication & Authorization**: JWT-based authentication with secure password hashing
- **Post Management**: Create, read, update, and delete posts with user ownership
- **Voting System**: Like/unlike posts with vote tracking
- **Database Management**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **CORS Support**: Cross-origin resource sharing enabled
- **Production Ready**: Heroku deployment configuration included

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI 0.116.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.41
- **Authentication**: JWT with python-jose and passlib
- **Password Hashing**: bcrypt
- **Database Migrations**: Alembic 1.16.4
- **ASGI Server**: Uvicorn 0.35.0
- **Data Validation**: Pydantic 2.11.7
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fastapi_3
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Set up database**
   - Create a PostgreSQL database
   - Update the `DATABASE_URL` in your `.env` file
   - Run database migrations:
   ```bash
   alembic upgrade head
   ```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Docs (Swagger UI)**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🔐 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Users
- `GET /users/me` - Get current user profile
- `GET /users/{id}` - Get user by ID
- `POST /users` - Create new user

### Posts
- `GET /posts` - Get all posts (with pagination)
- `GET /posts/{id}` - Get post by ID
- `POST /posts` - Create new post
- `PUT /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post

### Votes
- `POST /vote` - Vote on a post (like/unlike)

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `password`: Hashed password
- `created_at`: Account creation timestamp

### Posts Table
- `id`: Primary key
- `title`: Post title
- `content`: Post content
- `published`: Publication status
- `created_at`: Post creation timestamp
- `owner_id`: Foreign key to users table

### Votes Table
- `user_id`: Foreign key to users table
- `post_id`: Foreign key to posts table
- Composite primary key for user-post voting relationship

## 🔧 Configuration

The application uses a configuration system based on Pydantic settings. Key configuration options can be set through environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing secret
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## 🚀 Deployment

### Heroku Deployment
The project includes a `Procfile` for Heroku deployment:

```procfile
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT}
```

### Environment Variables for Production
Set these environment variables in your production environment:
- `DATABASE_URL`: Production PostgreSQL URL
- `SECRET_KEY`: Strong, unique secret key
- `PORT`: Port number (Heroku sets this automatically)

## 📁 Project Structure

```
fastapi_3/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── oauth2.py        # JWT authentication
│   └── utils.py         # Utility functions
├── routers/
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── user.py          # User management endpoints
│   ├── post.py          # Post management endpoints
│   └── vote.py          # Voting endpoints
├── alembic/              # Database migration files
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment configuration
└── README.md            # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/fastapi_3/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## 🙏 Acknowledgments

- FastAPI community for the excellent framework
- SQLAlchemy team for the powerful ORM
- Alembic contributors for database migration tools

---

**Made with ❤️ using FastAPI**
