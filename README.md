
# BlogWebApp

BlogWebApp is a modern, modular, and production-ready blog platform built with Django, Django REST Framework, Celery, and Docker. It supports user authentication, post and comment management, category organization, RESTful APIs, and robust background processing. The project is designed for easy local development and scalable deployment.

## Features

- **Django-based backend** with a custom user model
- **RESTful API** for all major resources (posts, categories, comments, users)
- **JWT and token authentication** (with email verification)
- **User registration, login, password reset, and profile management**
- **Blog post and category CRUD** (with permissions)
- **Comment system** (with permissions)
- **Admin panel** for managing all resources
- **Celery** for background tasks (e.g., email, token cleanup)
- **Docker Compose** for local and production environments
- **PostgreSQL** (production) and SQLite (development) support
- **Redis** for caching and Celery broker
- **Swagger and Redoc** API documentation
- **Captcha** for signup and password reset
- **Nginx** for static/media serving in production

## Project Structure

```
BlogWebApp/
├── core/
│   ├── account/      # User management, authentication, profile
│   ├── blog/         # Blog posts, categories
│   ├── comment/      # Comments on posts
│   ├── jwt_token/    # JWT token management
│   ├── BlogSite/     # Django project settings, URLs, celery config
│   ├── manage.py     # Django management script
│   └── ...
├── requirements.txt  # Python dependencies
├── docker-compose-dev.yml
├── docker-compose-prod.yml
├── dockerfiles/      # Dockerfiles for dev/prod
├── env/              # Environment variable files
├── default.conf      # Nginx config
└── ...
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- (For local dev) Python 3.12+

### Development Setup
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd BlogWebApp
   ```
2. **Copy and edit environment variables:**
   ```sh
   cp env/dev/.env.example env/dev/.env
   # Edit env/dev/.env as needed
   ```
3. **Build and start services:**
   ```sh
   docker-compose -f docker-compose-dev.yml up --build
   ```
4. **Access the app:**
   - Web: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - API docs: http://localhost:8000/swagger/ or /redoc/

### Production Setup
1. **Copy and edit production env:**
   ```sh
   cp env/prod/.env.example env/prod/.env
   # Edit env/prod/.env as needed
   ```
2. **Build and start services:**
   ```sh
   docker-compose -f docker-compose-prod.yml up --build -d
   ```
3. **Nginx serves static/media files and proxies to backend.**

## API Overview

- **Swagger UI:** `/swagger/`
- **Redoc:** `/redoc/`
- **Auth:** `/account/api/v1/` (signup, login, JWT, password, profile)
- **Posts:** `/posts/api/v1/posts/`
- **Categories:** `/categories/api/v1/categories/`
- **Comments:** `/posts/api/v1/posts/<post_id>/comments/`

## Main Apps & Modules

- **account:** Custom user model, registration, login, JWT, email verification, profile, password management, captcha
- **blog:** Posts, categories, permissions, API, admin
- **comment:** Comments on posts, API, permissions
- **jwt_token:** Secure token management for email verification and password reset
- **celery:** Background tasks (email, token cleanup)

## Testing

Run all tests (requires dev dependencies):
```sh
docker-compose -f docker-compose-dev.yml exec backend pytest
```

## License

This project is licensed under the terms of the [MIT License](./LICENSE).