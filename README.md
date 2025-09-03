# 📺 Odysee Clone API (Flask)

This project is a backend API for an **Odysee-like video platform**, built with **Flask** and modern Python libraries.  
It provides **authentication, video management, user sessions, and media uploads** with a clean and scalable architecture.

---

## 🚀 Tech Stack

- [Flask](https://flask.palletsprojects.com/) – Web framework
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) – JWT-based authentication
- [Flask-Mail](https://pythonhosted.org/Flask-Mail/) – Email verification & notifications
- [Redis](https://redis.io/) – Token storage, caching, and session management
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/) – Password hashing
- [Flask-CORS](https://flask-cors.readthedocs.io/) – Cross-origin resource sharing
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) – Database migrations
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) – ORM for PostgreSQL
- [psycopg2-binary](https://www.psycopg.org/) – PostgreSQL adapter
- [flask-validators](https://pypi.org/project/flask-validators/) – Request validation
- [imagekitio](https://docs.imagekit.io/) – Media storage & CDN
- [marshmallow](https://marshmallow.readthedocs.io/) – Serialization & schema validation
- [python-dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management

---

## ⚙️ Features

✅ User registration & login (JWT Authentication)  
✅ Email verification with **Flask-Mail**  
✅ Password hashing with **Bcrypt**  
✅ Access & refresh token management with **Redis**  
✅ Video & image uploads with **ImageKit**  
✅ Secure APIs with input validation (flask-validators & marshmallow)  
✅ Role-based permissions (Admin/User)  
✅ PostgreSQL + SQLAlchemy ORM  
✅ Database migrations with **Alembic/Flask-Migrate**

## 🔑 Environment Variables

```env
# ==========================
# Application Configuration
# ==========================
# Configuration Mode => development, testing, staging, or production
CONFIG_MODE=development

# ==========================
# Database Configuration
# ==========================
# PostgreSQL Database URI
# Example: postgresql+psycopg2://user:password@host:port/database
DEVELOPMENT_DATABASE_URL=postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}

# ==========================
# JWT Configuration
# ==========================
JWT_SECRET_KEY=your-jwt-secret
JWT_COOKIE_SECURE=True
JWT_COOKIE_SAMESITE=Lax
JWT_ACCESS_TOKEN_EXPIRES=900        # 15 minutes
JWT_REFRESH_TOKEN_EXPIRES=604800    # 7 days

# ==========================
# Mail.ru SMTP Configuration
# ==========================
MAIL_SERVER=smtp.mail.ru
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_USERNAME=your-email@mail.ru
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@mail.ru

# ==========================
# Additional Email Configurations
# ==========================
MAIL_SUPPRESS_SEND=False  # Set True during testing to suppress sending emails
MAIL_DEBUG=False          # Enable debug mode if necessary
```

## ⚙️ Installation & Setup

1. Clone the repository, create and activate a virtual environment, install dependencies, configure the `.env` file (see Environment Variables section), run database migrations, ensure Redis is running, and finally start the Flask development server with:

```bash
git clone https://github.com/SomeOne1305/odysee-clone-api.git
cd odysee-clone-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run
```
