# Django Optimization

A Django REST API project for managing user profiles and products with categories. This project includes token-based authentication, API documentation with Swagger

## Installation

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd django-optimization
```

### 2. Create a Virtual Environment

```bash
python -m venv env
```

### 3. Activate the Virtual Environment

**On Linux/Mac:**
```bash
source env/bin/activate
```

**On Windows:**
```bash
env\Scripts\activate
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional)

To access the admin panel, create a superuser account:

```bash
python manage.py createsuperuser
```


## Running the Project

Start the development server:

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Important URLs

- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Swagger API Documentation**: http://127.0.0.1:8000/swagger/
- **API Base URL**: http://127.0.0.1:8000/api/

## Authentication

This API uses Token Authentication. To access protected endpoints:

1. Register a user or login to get an authentication token
2. Include the token in the request header:
   ```
   Authorization: Token <your-token-here>
   ```

## Testing

Run tests using pytest:

```bash
pytest
```

## Technologies Used

- **Django** - Web framework
- **Django REST Framework** - REST API toolkit
- **drf-yasg** - Swagger/OpenAPI documentation
- **SQLite** - Database
- **pytest** - Testing framework

