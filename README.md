# MeetVo Backend

A robust backend API for the MeetVo application, built with Python, SQLAlchemy, and Alembic for database management. This backend provides authentication, user management, and session handling capabilities integrated with Clerk authentication service.

## 🏗️ Architecture

- **Framework**: Python with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production)
- **Migration Tool**: Alembic
- **Authentication**: Clerk integration
- **Environment**: Virtual environment with pip

## 📁 Project Structure

```
meetvo-backend/
├── db/
│   ├── __init__.py
│   ├── db.py                 # Database configuration and connection
│   ├── models.py             # SQLAlchemy models
│   └── migrations/
│       ├── env.py            # Alembic environment configuration
│       ├── script.py.mako    # Migration template
│       └── versions/         # Database migration files
├── alembic.ini               # Alembic configuration
├── dev.db                    # SQLite development database
└── venv/                     # Python virtual environment
```

## 🗄️ Database Models

### User Model
- **clerk_id**: Unique identifier from Clerk authentication
- **email**: User email address (unique)
- **email_verified**: Email verification status
- **image**: User profile image URL
- **created_at/updated_at**: Timestamps

### Session Model
- **expires_at**: Session expiration time
- **token**: Unique session token
- **ip_address**: Client IP address
- **user_agent**: Client user agent
- **user_id**: Foreign key to User

### Account Model
- **account_id**: Provider's account ID
- **provider_id**: Authentication provider (e.g., "google", "outlook")
- **access_token/refresh_token**: OAuth tokens
- **access_token_expires_at/refresh_token_expires_at**: Token expiration times
- **scope**: OAuth scope permissions
- **password**: For password-based accounts

### Verification Model
- **indentifier**: Verification identifier
- **value**: Verification value
- **expiresAt**: Verification expiration time
- **createdAt/updatedAt**: Timestamps

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- pip (Python package manager)
- Virtual environment support

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd meetvo-backend
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
   pip install sqlalchemy alembic python-dotenv psycopg2-binary
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=sqlite:///./dev.db
   # For production PostgreSQL:
   # DATABASE_URL=postgresql://username:password@localhost/dbname
   ```

### Database Setup

1. **Run migrations**
   ```bash
   alembic upgrade head
   ```

2. **Create new migration (when models change)**
   ```bash
   alembic revision --autogenerate -m "description of changes"
   alembic upgrade head
   ```

## 🔧 Configuration

### Database Configuration (`db/db.py`)
- Supports both SQLite and PostgreSQL
- Automatic connection pooling
- Environment-based configuration via `.env` file

### Alembic Configuration (`alembic.ini`)
- Migration scripts location: `db/migrations`
- Database URL from environment variables
- Automatic metadata detection from models

## 📊 Available Migrations

1. **2e2daba4b8e2**: Initial users table creation
2. **330a4c71ec26**: Sessions table creation
3. **ac89d4b7a095**: Users table for Clerk integration
4. **fefbcd8cd91d**: Accounts and verifications tables
5. **3e39573735bb**: Additional schema changes

## 🔐 Authentication Integration

The backend is designed to work with Clerk authentication:

- **User Management**: Clerk handles user authentication and provides `clerk_id`
- **Session Management**: Custom session tracking with IP and user agent
- **Account Linking**: Support for multiple OAuth providers
- **Token Management**: Secure storage of access and refresh tokens

## 🛠️ Development

### Running the Application
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run database migrations
alembic upgrade head

# Start your Python application server
python your_app.py
```

### Database Operations
```bash
# Create new migration
alembic revision --autogenerate -m "Add new feature"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## 📝 API Endpoints

*Note: API endpoints are not yet implemented. This backend provides the database foundation for future API development.*

## 🔒 Security Features

- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Token Management**: Secure storage of authentication tokens
- **Session Tracking**: IP address and user agent logging
- **Cascade Deletes**: Proper cleanup of related records

## 🧪 Testing

*Testing framework not yet implemented. Consider adding pytest for unit and integration tests.*

## 📦 Dependencies

### Core Dependencies
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Alembic**: Database migration tool
- **python-dotenv**: Environment variable management
- **psycopg2-binary**: PostgreSQL adapter

### Development Dependencies
- **Virtual Environment**: Isolated Python environment
- **pip**: Package management

## 🚀 Deployment

### Production Setup
1. **Database**: Switch to PostgreSQL
   ```env
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

2. **Environment Variables**: Configure production environment variables

3. **Migration**: Run migrations on production database
   ```bash
   alembic upgrade head
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Create and run migrations if database changes are needed
5. Test your changes
6. Submit a pull request

## 📄 License

*License information to be added*

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the migration history for database-related issues
- Review Alembic documentation for migration problems

---

**Note**: This backend is currently in development. API endpoints and additional features are planned for future releases.
